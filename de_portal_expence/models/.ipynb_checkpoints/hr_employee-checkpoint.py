# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    vehicle_id = fields.Many2one('vehicle.meter.detail', string='Vehicle Meter')
    opening_reading = fields.Float(string='Opening Reading')
    

