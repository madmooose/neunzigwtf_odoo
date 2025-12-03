import base64
import io
import zipfile

from odoo import _, fields, models
from odoo.exceptions import UserError


class MediaGalleryBatchUploadWizard(models.TransientModel):
    _name = "media.gallery.batch.upload.wizard"
    _description = "Batch Upload Media Items"

    zip_file = fields.Binary("ZIP File", required=True)
    zip_filename = fields.Char("ZIP Filename")
    gallery_id = fields.Many2one("media.gallery")

    def action_upload(self):
        self.ensure_one()
        if not self.zip_file:
            raise UserError(_("Please upload a ZIP file."))
        try:
            zip_data = base64.b64decode(self.zip_file)
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
                for name in zf.namelist():
                    if name.endswith("/"):
                        continue
                    file_data = zf.read(name)
                    attachment = self.env["ir.attachment"].create(
                        {
                            "name": name,
                            "datas": base64.b64encode(file_data),
                            "mimetype": "application/octet-stream",
                        }
                    )
                    self.env["media.gallery.item"].create(
                        {
                            "name": name,
                            "attachment_id": attachment.id,
                            "gallery_id": self.gallery_id.id or False,
                        }
                    )
        except Exception as e:
            raise UserError(_("Error processing ZIP file: %s") % e) from e
        return {"type": "ir.actions.act_window_close"}
