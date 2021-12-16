from odoo import api, models, fields, tools
from odoo.exceptions import UserError
import requests
import logging
_logger = logging.getLogger(__name__)
import json


class SaleConfirmLimit(models.TransientModel):

    _name='picking.order.wizard'

    # temp = fields.Char('Temp')
    delivery_boy = fields.Many2one('res.partner','Delivery Boy',domain="[('is_driver', '=', True),('status','=','available')]")
    sale_order = fields.Many2many('sale.order',string="Sale Orders",domain="[('driver_id', '!=', False)]")

    def assign_drivers_zipcode_wise(self):
        sale_orders = self.sale_order.ids
        if len(sale_orders) != 0 and self.delivery_boy:
            picking_orders = self.env['picking.order'].search([('sale_order','in',sale_orders)])
            for picking in picking_orders:
                picking.delivery_boy = self.delivery_boy.id
                picking.state = 'assigned'

                Param = self.env['res.config.settings'].sudo().get_values()
                if Param.get('whatsapp_instance_id') and Param.get('whatsapp_token'):
                    if picking.sale_order.partner_id.country_id.phone_code and picking.sale_order.partner_id.mobile:
                        url = 'https://api.chat-api.com/instance' + Param.get('whatsapp_instance_id') + '/sendMessage?token=' + Param.get('whatsapp_token')
                        headers = {
                            "Content-Type": "application/json",
                        }
                        whatsapp_msg_number = picking.sale_order.partner_id.mobile
                        whatsapp_msg_number_without_space = whatsapp_msg_number.replace(" ", "");
                        whatsapp_msg_number_without_code = whatsapp_msg_number_without_space.replace('+' + str(picking.sale_order.partner_id.country_id.phone_code), "")
                        msg = "Your order " + picking.delivery_boy.name + " driver has assigned."
                        tmp_dict = {
                            "phone": "+" + str(picking.sale_order.partner_id.country_id.phone_code) + "" + whatsapp_msg_number_without_code,
                            "body": msg

                        }
                        response = requests.post(url, json.dumps(tmp_dict), headers=headers)

                        if response.status_code == 201 or response.status_code == 200:
                            _logger.info("\nSend Message successfully")

                            mail_message_obj = self.env['mail.message']
                            comment = "fa fa-whatsapp"
                            body_html = tools.append_content_to_html('<div class = "%s"></div>' % tools.ustr(comment), msg)
                            # body_msg = self.convert_to_html(body_html)
                            mail_message_id = mail_message_obj.sudo().create({
                                'res_id': picking.id,
                                'model': 'picking.order',
                                'body': body_html,
                            })


                    else:
                        raise Warning('Please enter partner mobile number or select country for partner')
        else:
            raise UserError('Something went wrong. Please try again later')


    # @api.multi
    # def agent_exceed_limit(self):
    #     _logger.debug(' \n\n \t We can do some actions here\n\n\n')