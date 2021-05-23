# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import urllib
import html2text
from odoo import http, models, fields, api, tools, _
from odoo.http import request

_logger = logging.getLogger(__name__)

class ConvertHtmlText(object):

    def convert_html_to_text(result_txt):
        capt = b'%s' % (result_txt)
        convert_byte_to_str = capt.decode('utf-8')
        return html2text.html2text(convert_byte_to_str)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def url_link_invoice(self):

        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        return format_url
        
    def send_whatsapp_step(self):

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.invoice',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                            'default_partner_id': self.partner_id.id, 
                            'format_invisible': True
                            },
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'account.move',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'force_email': False,
            }

        # subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail_mt_note')
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[],
                                            message_type='notification', partner_ids=[], subtype_xmlid=None)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(AccountInvoice, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res