from odoo import http
from odoo.http import request


class RocketLanding(http.Controller):
    @http.route("/", auth="public", website=True)
    def landing_page(self, **kwargs):
        return request.render("rocket.rocket_landing_template")
