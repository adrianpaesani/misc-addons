# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SendWhatsappSale(models.TransientModel):
    _name = 'send.whatsapp.sale'
    _description = 'Enviar whatsapp a contacto'

    partner_id = fields.Many2one('res.partner')
    default_message_id = fields.Many2one('on.whatsapp.template', domain="[('category', '=', 'sale')]")

    name = fields.Char(related='partner_id.name')
    mobile_phone = fields.Char(related='partner_id.mobile',help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")

    message = fields.Text(string="Mensaje")
    format_visible_context = fields.Boolean(default=False)

    @api.onchange('default_message_id')
    def _onchange_message(self):
        sale_order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        message = self.default_message_id.template_message
        url_preview = sale_order_id.url_link_sale()

        try:
            incluid_name = str(message).format(
                name=sale_order_id.partner_id.name,
                sales_person=sale_order_id.user_id.name,
                company=sale_order_id.company_id.name,
                website=sale_order_id.company_id.website,
                document_name=sale_order_id.name,
                link_preview=url_preview, )

        except Exception:
            raise ValidationError('Parámetro no permitido en esta plantilla')

        if message:
            self.message = incluid_name

    @api.model
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.format_visible_context = self.env.context.get('format_invisible', False)
        self.mobile_phone = self.partner_id.mobile

    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    def sending_reset(self):
        # partner_id = self.env['res.partner'].browse(self._context.get('active_id'))
        self.partner_id.update({
            'send_whatsapp': 'without_sending',
            })
        self.close_dialog()

    def sending_confirmed(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile_phone, self.message, self.broadcast)

        if validation:
            self.env['on.whatsapp.mixin'].sending_confirmed(self.message)
            self.close_dialog()

    def sending_error(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile_phone, self.message, self.broadcast)

        if validation:
            self.env['on.whatsapp.mixin'].sending_error()
            self.close_dialog()

    def send_whatsapp(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile_phone, self.message, self.broadcast)

        if validation:
            whatsapp_url = self.env['on.whatsapp.mixin'].send_whatsapp(self.mobile_phone, self.message, self.broadcast)

            return {'type': 'ir.actions.act_url',
                    'url': whatsapp_url,
                    'param': "whatsapp_action",
                    'target': 'new',
                    }
