odoo.define("website_sale_order_line_note.sale_product_configurator", function (require) {
    "use strict";

    var ProductConfiguratorMixin = require("sale_product_configurator.ProductConfiguratorMixin");
    var publicWidget = require("web.public.widget");

    publicWidget.registry.ProductConfigurator = publicWidget.Widget.extend(ProductConfiguratorMixin, {
        selector: ".oe_website_sale",
        events: _.extend({}, publicWidget.Widget.prototype.events, {
            'change input[name="note"]': "_onChangeNote",
        }),

        /**
         * @private
         * @param {Event} ev
         */
        _onChangeNote: function (ev) {
            var $input = $(ev.currentTarget);
            var lineId = $input.data("line-id");
            var productId = $input.data("product-id");
            var note = $input.val();

            this._rpc({
                route: "/shop/cart/update",
                params: {
                    line_id: lineId,
                    product_id: productId,
                    note: note,
                },
            }).then(function (result) {
                if (result) {
                    window.location.reload();
                }
            });
        },
    });
});