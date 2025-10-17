from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MediaGalleryItem(models.Model):
    _name = "media.gallery.item"
    _inherit = ["image.mixin"]
    _description = "Media Gallery Item"

    name = fields.Char("Title", required=True)
    file = fields.Binary("Media File")
    file_type = fields.Selection(
        [
            ("image", "Image"),
            ("video", "Video"),
            ("audio", "Audio"),
            ("other", "Other"),
        ],
        string="Type",
        default="image",
    )
    description = fields.Text()
    gallery_id = fields.Many2one("media.gallery", string="Gallery", required=True)

    @api.constrains("file", "image_1920")
    def _check_file_or_image(self):
        for item in self:
            if bool(item.file) == bool(item.image_1920):
                raise ValidationError(
                    _(
                        "You must set either Media File or Image, but not both or neither."
                    )
                )
