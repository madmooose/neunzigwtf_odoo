{
    "name": "Portal Media Gallery",
    "version": "16.0.1.0.0",
    "category": "Website",
    "summary": "Allows portal users to view and manage media files",
    "author": "madmooose",
    "website": "https://www.ziemlichoptimal.de",
    "depends": ["base", "portal", "website"],
    "data": [
        "security/media_gallery_security.xml",
        "security/ir.model.access.csv",
        "views/media_gallery_views.xml",
        "views/media_gallery_item_views.xml",
        "views/media_gallery_menus.xml",
        "views/media_gallery_portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "media_gallery/static/src/css/media_gallery.css",
            "media_gallery/static/src/js/media_gallery.js",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
