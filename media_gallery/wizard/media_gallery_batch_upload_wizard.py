import base64
import os
import shutil
import zipfile

from odoo import _, fields, models, tools
from odoo.tools import logging

from odoo.addons.queue_job.delay import chain, group

_logger = logging.getLogger(__name__)


class MediaGalleryBatchUploadWizard(models.TransientModel):
    _name = "media.gallery.batch.upload.wizard"
    _description = "Batch Upload Media Items"

    zip_file = fields.Binary("ZIP File", required=True)
    zip_filename = fields.Char("ZIP Filename")
    gallery_id = fields.Many2one("media.gallery")
    extracted_path = fields.Char()

    # Helper for building the filestore path
    def _get_filestore_extract_path(self):
        filestore = tools.config.filestore(self.env.cr.dbname)
        path = os.path.join(filestore, "zip_extract", str(self.id))
        return path

    def action_upload(self):
        self.ensure_one()
        self.with_delay().job_extract_and_dispatch()

        return {"type": "ir.actions.act_window_close"}

    def job_extract_and_dispatch(self):
        self.ensure_one()
        if not self.zip_file:
            raise ValueError("No ZIP uploaded.")

        extract_path = self._get_filestore_extract_path()
        os.makedirs(extract_path, exist_ok=True)

        # --- Save ZIP into filestore ---
        zip_path = os.path.join(extract_path, self.zip_filename or "archive.zip")
        with open(zip_path, "wb") as f:
            f.write(base64.b64decode(self.zip_file))

        # --- Extract ZIP ---
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)

        # --- Build file list ---
        file_list = []
        for root, _dirs, files in os.walk(extract_path):
            for fname in files:
                file_list.append(os.path.join(root, fname))

        # Persist metadata
        self.write(
            {
                "extracted_path": extract_path,
            }
        )

        # ---------------------------------------------------------
        # Create a delayable object for the group fan-out pipeline
        # ---------------------------------------------------------
        # Collect jobs in a list using with_delay() wrappers
        jobs = []
        for fp in file_list:
            jobs.append(self.delayable().job_process_single_file(fp))

        # Chain: group all file jobs, then cleanup
        chain(
            group(*jobs),
            self.delayable().job_cleanup_all_files(),
        ).delay()

        return True

    def job_unpack_zip_file(self, zip_path, extract_path):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)
        return True

    def job_process_single_file(self, file_path, file_name=False, gallery_id=False):
        # Try to read as text (adapt for binary files)
        with open(file_path, "rb") as f:
            file_data = f.read()
        attachment = self.env["ir.attachment"].create(
            {
                "name": file_name or os.path.basename(file_path),
                "datas": base64.b64encode(file_data),
            }
        )
        # Create a record representing this file
        self.env["media.gallery.item"].create(
            {
                "name": file_name or _("Unknown File"),
                "gallery_id": gallery_id.id
                if hasattr(gallery_id, "id")
                else gallery_id,
                "attachment_id": attachment.id,
            }
        )
        # Return a queue.job recordset for chaining
        return True

    def job_cleanup_all_files(self):
        extract_path = self.extracted_path

        # Remove all extracted files
        if extract_path and os.path.exists(extract_path):
            try:
                shutil.rmtree(extract_path)
            except Exception:
                _logger.exception(
                    "Failed to cleanup extracted files at %s", extract_path
                )

        return True
