from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class MediaGalleryPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "media_gallery_count" in counters:
            media_gallery_count = (
                request.env["media.gallery"].search_count([("item_count", "!=", 0)])
                if request.env["media.gallery"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
            values["media_gallery_count"] = media_gallery_count
        return values


class MediaGalleryPortalController(http.Controller):
    @http.route("/my/gallery", type="http", auth="user", website=True)
    def portal_media_gallery_list(self, **kw):
        galleries = request.env["media.gallery"].search([("item_count", "!=", 0)])
        values = {
            "page_name": "media_gallery",
            "galleries": galleries,
        }
        return request.render(
            "media_gallery.portal_media_gallery_list_template",
            values,
        )

    @http.route("/my/gallery/<int:gallery_id>", type="http", auth="user", website=True)
    def portal_media_gallery_detail(self, gallery_id, **kw):
        gallery = request.env["media.gallery"].browse(gallery_id)
        media_items = request.env["media.gallery.item"].search(
            [("gallery_id", "=", gallery_id), ("file_type", "=", "image")]
        )
        values = {
            "page_name": "media_gallery",
            "gallery": gallery,
            "media_items": media_items,
        }
        return request.render(
            "media_gallery.portal_media_gallery_detail_template",
            values,
        )

    @http.route(
        "/my/gallery/item/<int:item_id>", type="http", auth="user", website=True
    )
    def portal_media_gallery_item(self, item_id, **kw):
        item = request.env["media.gallery.item"].browse(item_id)
        gallery_items = request.env["media.gallery.item"].search(
            [("gallery_id", "=", item.gallery_id.id), ("file_type", "=", "image")]
        )
        item_ids = [i.id for i in gallery_items]
        idx = item_ids.index(item_id) if item_id in item_ids else -1
        prev_id = item_ids[idx - 1] if idx > 0 else None
        next_id = item_ids[idx + 1] if idx < len(item_ids) - 1 else None
        values = {
            "page_name": "media_gallery",
            "gallery": item.gallery_id if item.gallery_id else None,
            "item": item,
            "prev_id": prev_id,
            "next_id": next_id,
        }
        return request.render(
            "media_gallery.portal_media_gallery_item_template",
            values,
        )
