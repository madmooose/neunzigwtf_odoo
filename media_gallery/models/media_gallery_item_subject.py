from odoo import fields, models


class MediaGalleryItemSubject(models.Model):
    _name = "media.gallery.item.subject"
    _description = "Media Gallery Item Subject"
    _rec_name = "user_id"

    item_id = fields.Many2one("media.gallery.item", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")
    visibility = fields.Selection(
        [
            ("public", "Public"),
            ("users", "Users"),
            ("own", "Own"),
        ],
    )

    _sql_constraints = [
        (
            "item_user_unique",
            "unique(item_id, user_id)",
            "Each user can only be a subject once per item!",
        ),
    ]

    def set_visibility(self, visibility):
        for record in self:
            if record.user_id.id == self.env.user.id:
                record = record.sudo()
            record.visibility = visibility
