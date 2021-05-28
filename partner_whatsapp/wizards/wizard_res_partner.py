# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SendWhatsappPartner(models.TransientModel):
    _name = 'send.whatsapp.partner'
    _description = 'Envío de whatsapp'

    partner_id = fields.Many2one('res.partner', domain="[('parent_id','=',partner_id)]")

    def _default_default_message_id(self):
        default_message_id = self.env['on.whatsapp.template'].search([('category', '=', 'partner')])
        if default_message_id:
            return default_message_id[0]
        else:
            False
    
    default_messege_id = fields.Many2one('on.whatsapp.template', domain="[('category', '=', 'partner')]", default=_default_default_message_id)

    name = fields.Char(related='partner_id.name')
    mobile = fields.Char(related='partner_id.mobile',help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")

    message = fields.Text(string="Mensaje")
    format_visible_context = fields.Boolean(default=False)

    jitsi_link = fields.Char(string="Link Jitsi", readonly=True)

    @api.model
    def create(self, vals):
        vals['jitsi_link'] = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
        res = super(SendWhatsappPartner, self).create(vals)
        return res

    @api.onchange('default_messege_id')
    def _onchange_message(self):
        partner_uid = self.env['res.partner'].browse(self._context.get('uid'))
        partner_record = self.env['res.partner'].browse(self._context.get('active_id'))
        message = self.default_messege_id.template_message
        incluid_name = ''
        if not self.jitsi_link:
            self.jitsi_link = self.env['jitsi.meet'].sudo().create({'name':'Jitsi Meet'}).jitsi_link
        
        try:
            incluid_name = str(message).format(
                name=partner_record.name,
                sales_person=partner_uid.name,
                company=partner_uid.company_id.name,
                website=partner_uid.company_id.website,
                jitsi=self.jitsi_link)
        except Exception:
            raise ValidationError('Quick replies: parameter not allowed in this template, {link_preview} {item_product}')


        if message:
            self.message = incluid_name

    @api.model
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.format_visible_context = self.env.context.get('format_invisible', False)
        self.mobile = self.partner_id.mobile

    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    def sending_reset(self):
        partner_id = self.env['res.partner'].browse(self._context.get('active_id'))
        partner_id.update({
            'send_whatsapp': 'without_sending',
            })
        self.close_dialog()

    def sending_confirmed(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile, self.message, self.broadcast)

        if validation:
            self.env['on.whatsapp.mixin'].sending_confirmed(self.message)
            self.close_dialog()

    def sending_error(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile, self.message, self.broadcast)

        if validation:
            self.env['on.whatsapp.mixin'].sending_error()
            self.close_dialog()

    def send_whatsapp(self):
        validation = self.env['on.whatsapp.mixin'].send_validation_broadcast(self.mobile, self.message, self.broadcast)

        if validation:
            whatsapp_url = self.env['on.whatsapp.mixin'].send_whatsapp(self.mobile, self.message, self.broadcast)

            return {'type': 'ir.actions.act_url',
                    'url': whatsapp_url,
                    'param': "whatsapp_action",
                    'target': 'new',
                    }
