from odoo import http
from odoo.http import request


class MediaGalleryPortal(http.Controller):
    @http.route(
        ["/my/gallery", "/my/gallery/<int:gallery_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_media_gallery(self, gallery_id=None, **kw):
        domain = [("portal_user_id", "=", request.env.user.partner_id.id)]
        if gallery_id:
            domain += [("gallery_id", "=", gallery_id)]
        media_items = request.env["media.gallery.item"].search(domain)
        galleries = request.env["media.gallery"].search(
            [("portal_user_id", "=", request.env.user.partner_id.id)]
        )
        return request.render(
            "media_gallery.portal_media_gallery_template",
            {
                "media_items": media_items,
                "galleries": galleries,
                "active_gallery_id": gallery_id,
            },
        )
