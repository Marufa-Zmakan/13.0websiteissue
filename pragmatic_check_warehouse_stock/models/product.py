# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection(selection_add=[
        ('always_allow',
         'Show inventory on website and allow sales if enough stock at different location'),
    ])
    stock_buffer = fields.Float('Stock Buffer')

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        """Override this method to add forecasted qty in the
        virtual_available_formatted for displaying on the website."""
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(
                combination_info['product_id'])

            combination_info.update({
                # added forecasted quantity of all location.
                'virtual_available_formatted': product.virtual_available,
            })
        return combination_info


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_availability = fields.Selection(selection_add=[
        ('always_allow',
         'Show inventory on website and allow sales if enough stock at different location'),
    ])
