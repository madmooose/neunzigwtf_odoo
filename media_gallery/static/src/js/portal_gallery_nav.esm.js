/**
 * Odoo Portal Media Gallery Navigation
 * Handles left/right arrow navigation and swipe for gallery item view.
 */
odoo.define("media_gallery.portal_gallery_nav", function (require) {
    var publicWidget = require("web.public.widget");

    publicWidget.registry.PortalGalleryNav = publicWidget.Widget.extend({
        selector: ".o_portal_media_gallery_item",
        start: function () {
            this._onKeyDown = this._onKeyDown.bind(this);
            document.addEventListener("keydown", this._onKeyDown);
            this._initSwipe();
            return this._super.apply(this, arguments);
        },
        destroy: function () {
            document.removeEventListener("keydown", this._onKeyDown);
            this._removeSwipe();
            return this._super.apply(this, arguments);
        },
        _onKeyDown: function (e) {
            if (e.key === "ArrowLeft") {
                var prev = document.getElementById("prev-btn");
                if (prev) {
                    window.location = prev.href;
                }
            }
            if (e.key === "ArrowRight") {
                var next = document.getElementById("next-btn");
                if (next) {
                    window.location = next.href;
                }
            }
        },
        _initSwipe: function () {
            this._touchStartX = null;
            this._touchEndX = null;
            this._touchHandler = this._onTouch.bind(this);
            this.el.addEventListener("touchstart", this._touchHandler, {passive: true});
            this.el.addEventListener("touchend", this._touchHandler, {passive: true});
        },
        _removeSwipe: function () {
            this.el.removeEventListener("touchstart", this._touchHandler);
            this.el.removeEventListener("touchend", this._touchHandler);
        },
        _onTouch: function (e) {
            if (e.type === "touchstart") {
                this._touchStartX = e.changedTouches[0].screenX;
            } else if (e.type === "touchend") {
                this._touchEndX = e.changedTouches[0].screenX;
                this._handleSwipe();
            }
        },
        _handleSwipe: function () {
            if (this._touchStartX !== null && this._touchEndX !== null) {
                var diff = this._touchStartX - this._touchEndX;
                if (Math.abs(diff) > 50) {
                    // Swipe threshold
                    if (diff > 0) {
                        // Swipe left
                        var next = document.getElementById("next-btn");
                        if (next) {
                            window.location = next.href;
                        }
                    } else {
                        // Swipe right
                        var prev = document.getElementById("prev-btn");
                        if (prev) {
                            window.location = prev.href;
                        }
                    }
                }
            }
            this._touchStartX = null;
            this._touchEndX = null;
        },
    });

    return publicWidget.registry.PortalGalleryNav;
});
