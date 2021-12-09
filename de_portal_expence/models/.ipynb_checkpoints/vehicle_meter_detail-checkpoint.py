# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class VehicleMeterDetail(models.Model):
    _name = 'vehicle.meter.detail'
    _description = 'Vehicle Meter Detail'
    
    name = fields.Char(string='Name', required=True)
    vehicle_name = fields.Char(string='Vehicle Name')
    meter_reading = fields.Integer(string='Meter Reading', required=True)
    company_id  = fields.Many2one('res.company', string='Company')
    employee_id = fields.Many2one('hr.employee', string='Employee')

