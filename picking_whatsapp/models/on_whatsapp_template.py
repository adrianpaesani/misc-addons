# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class WhatsappTemplate(models.Model):
    _inherit = 'on.whatsapp.template'

    category = fields.Selection(selection_add=[('picking', 'Transferencias')])
