# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale whatsapp integrations",
    "summary": "Integrate whatsapp with Sale App",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OpenNovaSoft/misc-addons",
    "author": "openNova",
    "license": "AGPL-3",
    "depends": ["base", "sale", "base_whatsapp"],
    "data": [
        "data/sale_whatsapp.xml",
        'views/sale_order_view.xml',
        "wizards/wizard_sale_order_view.xml"
        ],
    "development_status": "Production/Stable",        
    "installable": True,
}
