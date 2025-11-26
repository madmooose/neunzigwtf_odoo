from odoo import fields, models


class MediaGallery(models.Model):
    _name = "media.gallery"
    _description = "Media Gallery"

    name = fields.Char("Gallery Name", required=True)
    description = fields.Text()
    cover_image = fields.Binary()
    item_ids = fields.One2many("media.gallery.item", "gallery_id", string="Media Items")

    def action_open_add_file_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "media.gallery.add.file.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_gallery_id": self.id,
            },
        }
