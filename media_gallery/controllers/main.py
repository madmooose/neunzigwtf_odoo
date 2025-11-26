from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class MediaItemPortalControler(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        user = request.env.user
        values = super()._prepare_home_portal_values(counters)
        if "media_item_count" in counters:
            media_item_count = (
                request.env["media.item"].ssearch_count(self._prepare_item_domain(user))
                if request.env["media.item"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
            values["media_item_count"] = media_item_count
        if "media_item_approval_count" in counters:
            media_item_approval_count = (
                request.env["media.item"].ssearch_count(
                    self._prepare_item_domain(user, approval=True)
                )
                if request.env["media.item"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
            values["media_item_approval_count"] = media_item_approval_count
        return values

    def _prepare_item_domain(self, user, approval=False):
        if approval:
            return [
                ("subject_id.user_id", "=", user.id),
            ]
        else:
            return [
                "|",
                ("user_id", "=", user.id),
                ("subject_id.user_id", "=", user.id),
                ("state", "=", "approved"),
            ]

    @http.route("/my/gallery", type="http", auth="public", website=True)
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


class MediaGalleryController(http.Controller):
    def _prepare_gallery_domain(self, gallery_id):
        return [
            ("gallery_id", "=", gallery_id),
            ("file_type", "=", "image"),
            ("state", "=", "approved"),
        ]

    @http.route("/gallery", type="http", auth="public", website=True)
    def portal_media_gallery_list(self, **kw):
        all_galleries = request.env["media.gallery"].search([])
        galleries = all_galleries.filtered(lambda g: g.item_ids)
        values = {
            "page_name": "media_gallery",
            "galleries": galleries,
        }
        return request.render(
            "media_gallery.media_gallery_list_template",
            values,
        )

    @http.route("/gallery/<int:gallery>", type="http", auth="public", website=True)
    def portal_media_gallery_detail(self, gallery, **kw):
        gallery_id = int(gallery)
        gallery = request.env["media.gallery"].browse(gallery_id)
        media_items = request.env["media.gallery.item"].search(
            self._prepare_gallery_domain(gallery_id)
        )
        values = {
            "page_name": "media_gallery",
            "gallery": gallery,
            "media_items": media_items,
        }
        return request.render(
            "media_gallery.media_gallery_detail_template",
            values,
        )

    @http.route("/gallery/item/<int:item_id>", type="http", auth="public", website=True)
    def portal_media_gallery_item(self, item_id, **kw):
        item_id = int(item_id)
        item = request.env["media.gallery.item"].browse(item_id)
        gallery_items = request.env["media.gallery.item"].search(
            self._prepare_gallery_domain(item.gallery_id.id)
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
            "media_gallery.media_gallery_item_template",
            values,
        )
