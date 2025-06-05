# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


{
    "name": "website_sale_order_line_note",
    "summary": "Note on sale order line in portal",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "website": "https://www.ziemlichoptimal.de",
    "author": "Niels Göttsch,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_order_line_note",
        "sale_product_configurator",
        "website_sale"
    ],
    "data": [
        "views/templates.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_order_line_note/static/src/js/website_sale_order_line_note.js",
            "website_sale_order_line_note/static/src/js/website_sale.js",
        ]
    },
    "demo": [],
    "qweb": [],
}
