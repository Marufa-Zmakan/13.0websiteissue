# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection(selection_add=[
        ('always_allow',
         'Show inventory on website and allow sales if enough stock at different location'),
    ])
    stock_buffer = fields.Float('Stock Buffer')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_availability = fields.Selection(selection_add=[
        ('always_allow',
         'Show inventory on website and allow sales if enough stock at different location'),
    ])
