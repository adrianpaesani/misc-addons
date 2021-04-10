# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Employee whatsapp integrations",
    "summary": "Integrate whatsapp with hr employee's",
    "version": "13.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/OpenNovaSoft/misc-addons",
    "author": "openNova",
    "license": "AGPL-3",
    "depends": ["base", "hr", "jitsi_meet", "base_whatsapp"],
    "data": [
        "data/employee_whatsapp.xml",
        'views/hr_employee_view.xml',
        "wizards/wizard_hr_employee_view.xml"
        ],
    "development_status": "Production/Stable",        
    "installable": True,
}
