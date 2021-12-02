# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepartmentWise(models.Model):
    _inherit = 'hr.work.location'
    
    location_ids = fields.Many2many('long.service.wizard', string='Location Wizard')
    
    
    
    
class DepartmentWise(models.Model):
    _inherit = 'hr.department'
    
    department_ids = fields.Many2many('long.service.wizard', string='Department Wizard')