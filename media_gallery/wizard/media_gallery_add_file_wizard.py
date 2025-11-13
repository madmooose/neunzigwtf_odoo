from odoo import fields, models


class MediaGalleryAddFileWizard(models.TransientModel):
    _name = "media.gallery.add.file.wizard"
    _description = "Add File to Media Gallery Wizard"

    gallery_id = fields.Many2one("media.gallery", string="Gallery", required=True)
    name = fields.Char("Title", required=True)
    attachment = fields.Binary("File", required=True)
    filename = fields.Char()
    description = fields.Text()

    def action_add_file(self):
        self.ensure_one()
        attachment = self.env["ir.attachment"].create(
            {
                "name": self.filename or self.name,
                "datas": self.attachment,
                "res_model": "media.gallery.item",
            }
        )
        self.env["media.gallery.item"].create(
            {
                "name": self.name,
                "gallery_id": self.gallery_id.id,
                "attachment_id": attachment.id,
                "description": self.description,
                "image_1920": attachment.datas
                if attachment.mimetype.startswith("image/")
                else False,
            }
        )
        return {"type": "ir.actions.act_window_close"}
