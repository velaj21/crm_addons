# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import re

from odoo.exceptions import ValidationError

ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class Source(models.Model):
    _name = 'source.source'
    _description = 'Source'

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Each name must be unique.'),
    ]

    name = fields.Char(string='Source Name', required=True)
    ips_from_source_ids = fields.One2many('source.ip', 'source_id', string='Source IP Addresses')


class SourceIp(models.Model):
    _name = 'source.ip'
    _description = 'Source IP'
    # _rec_name = 'ip_value'

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Each IP must be unique.'),
    ]

    name = fields.Char(string='IP Value', required=True)
    source_id = fields.Many2one('source.source', string='Source')

    @api.constrains('name')
    def _check_name(self):
        if self.name:
            if re.match(ip_pattern, self.name) is None:
                raise ValidationError("Invalid email address format")


class Person(models.Model):
    _name = "person.person"
    _description = "Person"

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Each name must be unique.'),
    ]

    # Description
    name = fields.Char(string="Name", required=True)

    notes = fields.Text(string="Comments")
    responsible_person = fields.Many2one(comodel_name="res.users", string="Checker")

    phone_number_id = fields.One2many(comodel_name="phone.number", inverse_name="person_id", string="Phone Numbers")
    person_email_id = fields.One2many(comodel_name="person.email", inverse_name="person_id", string="Emails")

    # def _get_name(self):
    #     name = [f'{rec.name}/{rec.number}' for rec in self]
    #     return name

    # def copy(self, default=None):
    #     raise UserError("You can't duplicate!")


class PhoneNumber(models.Model):
    _name = 'phone.number'
    _description = 'Phone Number'

    _sql_constraints = [
        ('phone_number_uniq', 'unique (phone_number, person_id)', 'Each phone number must be unique.'),
    ]

    phone_number = fields.Char(string='Phone Number', required=True)
    person_id = fields.Many2one('person.person', string='Person', required=True)
    source = fields.Many2one('source.source', string='Source', required=True)

    def name_get(self):
        """ Override name_get method to return an appropriate configuration wizard
        name, and not the generated name."""
        return [(rec.id, f'{rec.phone_number}/{rec.source}') for rec in self]


class PersonEmail(models.Model):
    _name = 'person.email'
    _description = 'Emails'

    _sql_constraints = [
        ('email_uniq', 'unique (email, person_id)', 'Each email must be unique.'),
    ]

    email = fields.Char(string='Email', required=True)
    person_id = fields.Many2one('person.person', string='Person', required=True)
    source = fields.Many2one('source.source', string='Source', required=True)

    @api.constrains('email')
    def _check_email(self):
        if self.email:
            if re.match(email_pattern, self.email) is None:
                raise ValidationError("Invalid email address format")

    def name_get(self):
        """ Override name_get method to return an appropriate configuration wizard
        name, and not the generated name."""
        return [(rec.id, f'{rec.email}/{rec.source}') for rec in self]
