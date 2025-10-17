odoo.define("website_sale_order_line_note.note_widget", function (require) {
    "use strict";
    var publicWidget = require("web.public.widget");

    publicWidget.registry.WebsiteSaleOrderLineNote = publicWidget.Widget.extend({
        selector: ".oe_website_sale .oe_cart",
        events: {
            "change .js-note": "_onNoteChange",
        },

        /**
         * Handle note field change: send note to backend for the correct line.
         * @param {Event} ev - The change event triggered by the note input field.
         */
        _onNoteChange: function (ev) {
            var $input = $(ev.currentTarget);
            var note = $input.val();
            var lineId = $input.data("line-id");
            var productId = $input.data("product-id");
            var $row = $input.closest("tr");
            var quantity = parseFloat($row.find(".js_quantity").val()) || 1;

            this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    line_id: lineId,
                    product_id: productId,
                    set_qty: quantity,
                    note: note,
                },
            });
        },
    });
});
