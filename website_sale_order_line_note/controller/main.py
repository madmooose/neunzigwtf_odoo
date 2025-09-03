from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleLineNote(WebsiteSale):
    @http.route()
    def cart_update_json(self, note=None, **kw):
        response = super().cart_update_json(**kw)
        line_id = kw.get("line_id")
        if line_id and note is not None:
            order_line = request.env["sale.order.line"].sudo().browse(int(line_id))
            if order_line.exists():
                order_line.write({"note": note})
        return response
