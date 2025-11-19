from odoo import _, api, fields, models


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

    def _get_default_title(self):
        return _("Untitled")

    name = fields.Char("Title", required=True, default=_get_default_title)
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
        VISIBILITY_SELECTION,
        compute="_compute_visibility",
        store=True,
        tracking=True,
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

    def action_deny(self):
        # BDD2: Deny photo, set state to denied
        for rec in self:
            rec.state = "denied"

    @api.depends("subject_ids", "subject_ids.visibility")
    def _compute_visibility(self):
        """
        BDD3: Compute visibility based on subject/user settings.
        """
        for item in self:
            visibility = [subj.visibility for subj in item.subject_ids]
            if visibility:
                if all(v == "public" for v in visibility):
                    item.visibility = "public"
                elif any(v is False for v in visibility):
                    item.visibility = "own"
                elif any(v == "own" for v in visibility):
                    item.visibility = "own"
                elif any(v == "users" for v in visibility):
                    item.visibility = "users"
            else:
                item.visibility = "public"

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

    def action_open_add_file_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "media.gallery.add.file.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {},
        }
