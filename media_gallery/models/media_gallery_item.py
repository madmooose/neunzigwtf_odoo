from odoo import api, fields, models


class MediaGalleryItem(models.Model):
    _name = "media.gallery.item"
    _inherit = ["image.mixin"]
    _description = "Media Gallery Item"

    name = fields.Char("Title", required=True)
    attachment_id = fields.Many2one(
        "ir.attachment",
        string="Media File",
        required=True,
        ondelete="cascade",
    )
    file_type = fields.Char(compute="_compute_file_type", store=True)
    description = fields.Text()
    gallery_id = fields.Many2one("media.gallery")
    image_1920 = fields.Image("Preview", compute="_compute_image_1920", store=True)

    @api.depends("attachment_id")
    def _compute_file_type(self):
        for item in self:
            if item.attachment_id:
                mime_type = item.attachment_id.mimetype
                if mime_type.startswith("image/"):
                    item.file_type = "image"
                elif mime_type.startswith("video/"):
                    item.file_type = "video"
                elif mime_type.startswith("audio/"):
                    item.file_type = "audio"
                else:
                    item.file_type = "other"
            else:
                item.file_type = "other"

    @api.depends("attachment_id")
    def _compute_image_1920(self):
        for item in self:
            if item.attachment_id and item.file_type == "image":
                item.image_1920 = item.attachment_id.datas
            else:
                item.image_1920 = False
