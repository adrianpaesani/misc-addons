# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SendWhatsappEmployee(models.TransientModel):
    _name = 'send.whatsapp.employee'
    _description = 'Enviar whatsapp a empleado'

    employee_id = fields.Many2one('hr.employee')
    default_message_id = fields.Many2one('on.whatsapp.template', domain="[('category', '=', 'employee')]")

    name = fields.Char(related='employee_id.name')
    mobile_phone = fields.Char(related='employee_id.mobile_phone',help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")

    message = fields.Text(string="Mensaje")
    format_visible_context = fields.Boolean(default=False)

    jitsi_link = fields.Char(string="Link Jitsi", readonly=True)

    @api.model
    def create(self, vals):
        vals['jitsi_link'] = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
        res = super(SendWhatsappEmployee, self).create(vals)
        return res

    @api.onchange('default_message_id')
    def _onchange_message(self):
        employee_record = self.env['hr.employee'].browse(self._context.get('active_id'))
        message = self.default_message_id.template_message
        incluid_name = ''
        if not self.jitsi_link:
            self.jitsi_link = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
    
        incluid_name = str(message).format(
            name=employee_record.name,
            company=employee_record.company_id.name,
            website=employee_record.company_id.website,
            jitsi=self.jitsi_link)

        if message:
            self.message = incluid_name

    @api.model
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.format_visible_context = self.env.context.get('format_invisible', False)
        self.mobile_phone = self.employee_id.mobile_phone

    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    def sending_reset(self):
        employee_id = self.env['hr.employee'].browse(self._context.get('active_id'))
        employee_id.update({
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
