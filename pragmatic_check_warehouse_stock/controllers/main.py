from odoo import http
from odoo.http import request
# Import the class
from odoo.addons.sale.controllers.variant import VariantController


# Inherit in your custom class
class CustomVariantController(VariantController):

    @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        combination = request.env[
            'product.template.attribute.value'].browse(combination)

        product_id = request.env[
            'product.product'].sudo().browse(int(product_id))
        # if product_id:
        #     product_data = product_id.qty_available
        # else:
        #     product_data = 0
        pricelist = self._get_pricelist(pricelist_id)
        ProductTemplate = request.env['product.template']
        if 'context' in kw:
            ProductTemplate = ProductTemplate.with_context(**kw.get('context'))
        product_template = ProductTemplate.browse(int(product_template_id))
        res = product_template._get_combination_info(
            combination, int(product_id or 0), int(add_qty or 1), pricelist)
        if 'parent_combination' in kw:
            parent_combination = request.env[
                'product.template.attribute.value'].browse(kw.get('parent_combination'))
            if not combination.exists() and product_id:
                product = request.env[
                    'product.product'].browse(int(product_id))
                if product.exists():
                    combination = product.product_template_attribute_value_ids
            res.update({
                'is_combination_possible': product_template._is_combination_possible(combination=combination, parent_combination=parent_combination),
            })

        res.update({
            # 'qty_available': product_data,
            'stock_buffer': product_id.stock_buffer,
        })

        return res
