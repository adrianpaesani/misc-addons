# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SendWhatsappPicking(models.TransientModel):
    _name = 'send.whatsapp.picking'
    _description = 'Enviar whatsapp a contacto'

    partner_id = fields.Many2one('res.partner')
    default_message_id = fields.Many2one('on.whatsapp.template', domain="[('category', '=', 'picking')]")

    name = fields.Char(related='partner_id.name')
    mobile_phone = fields.Char(related='partner_id.mobile',help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")

    message = fields.Text(string="Mensaje")
    format_visible_context = fields.Boolean(default=False)

    # jitsi_link = fields.Char(string="Link Jitsi", readonly=True)

    # @api.model
    # def create(self, vals):
    #     # vals['jitsi_link'] = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
    #     res = super(SendWhatsappEmployee, self).create(vals)
    #     return res

    @api.model
    def default_get(self, field_names):
        defaults = super(
            SendWhatsappPicking, self).default_get(field_names)
        # self.partner_id = self.env['stock.picking'].browse(self.env.context['active_id']).partner_id
        defaults['partner_id'] = self.env['stock.picking'].browse(self.env.context['active_id']).partner_id.id
        # import pdb; pdb.set_trace()
        return defaults

    @api.onchange('default_message_id')
    def _onchange_message(self):
        # employee_record = self.env['hr.employee'].browse(self._context.get('active_id'))
        partner_record = self.partner_id
        message = self.default_message_id.template_message
        incluid_name = ''
        # if not self.jitsi_link:
        #     self.jitsi_link = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
    
        incluid_name = str(message).format(
            name=partner_record.name,
            company=partner_record.company_id.name,
            website=partner_record.company_id.website)

        if message:
            self.message = incluid_name

    @api.model
    @api.onchange('partner_id')
    def _onchange_employee_id(self):
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