# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CRM',
    'version': '1.8',
    'category': 'CRM/E.SH',
    'sequence': 15,
    'summary': 'CRM',
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base_setup',
        'base',
    ],
    'data': [
        'security/crm_call_center_security.xml',
        'security/ir.model.access.csv',
        'views/person_view.xml',
        'views/source_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    # 'assets': {
    # },
    'license': 'LGPL-3',
}
