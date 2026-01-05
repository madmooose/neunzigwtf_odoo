{
    "name": "Portal Media Gallery",
    "version": "16.0.1.4.1",
    "category": "Website",
    "summary": "Allows portal users to view and manage media files",
    "author": "madmooose",
    "website": "https://www.ziemlichoptimal.de",
    "depends": ["base", "mail", "portal", "website", "queue_job"],
    "data": [
        "security/media_gallery_security.xml",
        "security/ir.model.access.csv",
        "wizard/media_gallery_batch_upload_wizard_views.xml",
        "wizard/media_gallery_add_file_wizard_views.xml",
        "views/media_gallery_views.xml",
        "views/media_gallery_item_views.xml",
        "views/media_gallery_templates.xml",
        "views/media_gallery_portal_templates.xml",
        "views/media_gallery_menus.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "media_gallery/static/src/js/portal_gallery_nav.esm.js",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
