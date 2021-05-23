# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Customer invoice whatsapp integrations",
    "summary": "Integrate whatsapp with customer invoice",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OpenNovaSoft/misc-addons",
    "author": "openNova",
    "license": "AGPL-3",
    "depends": ["base", "account", "base_whatsapp"],
    "data": [
        "data/invoice_whatsapp.xml",
        'views/account_invoice_view.xml',
        "wizards/wizard_account_invoice_view.xml"
        ],
    "development_status": "Production/Stable",        
    "installable": True,
}
