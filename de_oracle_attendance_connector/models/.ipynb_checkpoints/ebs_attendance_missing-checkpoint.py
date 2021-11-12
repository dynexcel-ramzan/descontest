# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime


class HrAttendance(models.Model):
    _name = 'ebs.attendance.missing'
    _description = 'EBS Attendance Missing'
    
    
    work_location_id = fields.Many2one('hr.work.location', string='Work Location')
    execution_time = fields.Float(string='Execution Time')
    company_id = fields.Many2one('res.company', string='Company')
    
    
    
    

