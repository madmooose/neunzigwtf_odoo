from odoo import fields, models


class MediaGallery(models.Model):
    _name = "media.gallery"
    _description = "Media Gallery"

    name = fields.Char("Gallery Name", required=True)
    description = fields.Text()
    cover_image = fields.Binary()
    item_ids = fields.One2many("media.gallery.item", "gallery_id", string="Media Items")
