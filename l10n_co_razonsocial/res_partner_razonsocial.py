# -*- encoding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) Odoo Colombia (Community).
# Author        David Arnold (devCO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# #############################################################################

from odoo import models, fields, api, _


class ResPartnerRazonsocial(models.Model):
    _inherit = 'res.partner'

    @api.depends(
        'legal_entity_name',
        'firstname',
        'middlename',
        'first_lastname',
        'second_lastname'
    )
    def _copy_values(self):
        for partner in self:
            title = partner.title.shortcut and ' ' + partner.title.shortcut or ''
            if partner.company_type == 'company':
                name = partner.legal_entity_name and partner.legal_entity_name or ''
                partner.name = name + title
            elif partner.company_type == 'person':
                s1 = partner.firstname and partner.firstname + ' ' or ''
                s2 = partner.middlename and partner.middlename + ' ' or ''
                s3 = partner.first_lastname and partner.first_lastname + ' ' or ''
                s4 = partner.second_lastname and partner.second_lastname or ''
                partner.legal_denomination = s1 + s2 + s3 + s4 + title
                partner.name = s1 + s2 + s3 + s4 + title
            else:
                partner.legal_denomination = ''
                partner.name = 'Unknown'

    name = fields.Char(
        string=u'Nombre',readonly=True, default=" "
    )
    
    legal_entity_name = fields.Char(
        company_type={
            'company': [('required', True)],
            'person': [('invisible', True)],
            False: [('invisible', True)]
        }
    )
    
    legal_denomination = fields.Char(
        string=u'Legal Name',
        readonly=True,
        store=True,
        compute='_copy_values'
    )
    
    firstname = fields.Char('Primer Nombre',
        company_type={
            'person': [('required', True)],
            'company': [('invisible', True)],
            False: [('invisible', True)]
        }
    )
    middlename = fields.Char('Segundo Nombre',
        company_type={
            'company': [('invisible', True)],
            False: [('invisible', True)]
        }
    )
    first_lastname = fields.Char('Primer Apellido',
        company_type={
            'person': [('required', True)],
            'company': [('invisible', True)],
            False: [('invisible', True)]
        }
    )
    second_lastname = fields.Char('Segundo Apellido',
        company_type={
            'company': [('invisible', True)],
            False: [('invisible', True)]
        }
    )
    
    # Override from res.partner
    def onchange_type(self, company_type):
        value = {}
        value['title'] = False
        if company_type == 'company':
            value['use_parent_address'] = False
            domain = {'title': [('domain', '=', 'partner')]}
        else:
            domain = {'title': [('domain', '=', 'contact')]}
            value['state'] = False
        return {'value': value, 'domain': domain}
