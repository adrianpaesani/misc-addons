# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking whatsapp integrations",
    "summary": "Integrate whatsapp with stock picking operations",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OpenNovaSoft/misc-addons",
    "author": "openNova",
    "license": "AGPL-3",
    "depends": ["base", "stock", "base_whatsapp"],
    "data": [
        "data/picking_whatsapp.xml",
        'views/stock_picking_view.xml',
        "wizards/wizard_stock_picking_view.xml"
        ],
    "development_status": "Production/Stable",        
    "installable": True,
}
