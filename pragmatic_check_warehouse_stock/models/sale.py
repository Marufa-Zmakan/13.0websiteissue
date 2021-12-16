# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        values = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        line_id = values.get('line_id')

        for line in self.order_line:
            if line.product_id.type == 'product' and line.product_id.inventory_availability in ['always_allow']:
                cart_qty = sum(self.order_line.filtered(lambda p: p.product_id.id == line.product_id.id).mapped('product_uom_qty'))
                if cart_qty > line.product_id.qty_available and (line_id == line.id):
                    qty = line.product_id.qty_available - cart_qty
                    new_val = super(SaleOrder, self)._cart_update(line.product_id.id, line.id, qty, 0, **kwargs)
                    values.update(new_val)

                    # Make sure line still exists, it may have been deleted in super()_cartupdate because qty can be <= 0
                    if line.exists() and new_val['quantity']:
                        line.warning_stock = _('You ask for %s products but only %s is available') % (cart_qty, new_val['quantity'])
                        values['warning'] = line.warning_stock
                    else:
                        self.warning_stock = _("Some products became unavailable and your cart has been updated. We're sorry for the inconvenience.")
                        values['warning'] = self.warning_stock
        return values
