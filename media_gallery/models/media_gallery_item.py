from odoo import api, fields, models


class MediaGalleryItem(models.Model):
    _name = "media.gallery.item"
    _inherit = ["image.mixin", "mail.thread", "mail.activity.mixin"]
    _description = "Media Gallery Item"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    ]

    VISIBILITY_SELECTION = [
        ("public", "Public"),
        ("users", "Users"),
        ("own", "Own"),
    ]

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

    state = fields.Selection(
        STATE_SELECTION, default="draft", required=True, tracking=True
    )
    visibility = fields.Selection(
        VISIBILITY_SELECTION, default="own", required=True, tracking=True
    )
    subject_ids = fields.One2many(
        "media.gallery.item.subject",
        "item_id",
    )

    def can_portal_user_see(self, user):
        """
        Returns True if the given portal user (res.users) can see this photo, according to BDD1.
        """
        self.ensure_one()
        if self.state in ("draft", "denied"):
            return False
        if self.state == "approved":
            if self.visibility in ("public", "users"):
                return True
            if self.visibility == "own":
                # Check if user is in subject_ids
                return any(subj.user_id.id == user.id for subj in self.subject_ids)
        return False

    def action_approve(self):
        # BDD2: Approve photo, set state to approved
        for rec in self:
            rec.state = "approved"
            # If no subjects, set visibility to public
            if not rec.subject_ids:
                rec.visibility = "public"

    def action_deny(self):
        # BDD2: Deny photo, set state to denied
        for rec in self:
            rec.state = "denied"

    @api.onchange("subject_ids")
    def _onchange_subjects_or_visibilities(self):
        """
        BDD3: Update visibility based on subject/user settings.
        """
        for rec in self:
            vis = [subj.visibility for subj in rec.subject_ids]
            if vis:
                if all(v == "public" for v in vis):
                    rec.visibility = "public"
                elif any(v == "own" for v in vis):
                    rec.visibility = "own"
                elif any(v == "users" for v in vis):
                    rec.visibility = "users"

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
