# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api
from random import choice

def create_hash():
    size = 32
    values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    h = ''
    h = h.join([choice(values) for i in range(size)])
    return h

class JitsiMeet(models.Model):
    _name = 'jitsi.meet'
    _description = 'Jitsi meet'

    name = fields.Char(string="name", default="jitsi meet")
    jitsi_link = fields.Char(string="Link Jitsi", readonly=True)
    hash = fields.Char('Hash')

    @api.model
    def create(self, vals):
        vals['hash'] = create_hash()
        config_url =  self.env['ir.config_parameter'].sudo().get_param('jitsi_meet.jitsi_event_url',default='https://meet.jit.si/')
        vals['jitsi_link'] = config_url + vals['hash']
        res = super(JitsiMeet, self).create(vals)
        return res