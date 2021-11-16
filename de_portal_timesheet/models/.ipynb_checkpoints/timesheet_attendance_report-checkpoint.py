# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PortalTimesheet(models.Model):
    _name = 'hr.timesheet.report'
    _description = 'Hr Timesheet Report'
   
    
    partner_id = fields.Many2one('res.partner', string='Partner',  required=True)
    project_id = fields.Many2one('project.project', string='Project',  required=True)
    date_from = fields.Date(string='Date From')
    date_to  = fields.Date(string='Date To')
    timesheet_attendance_ids = fields.One2many('hr.timesheet.report.line', 'timesheet_repo_id',string='Timesheet Lines')
    total_duration = fields.Float(string='Total Days')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
         ],
        readonly=True, string='Status', default='draft')
    approval_request_id = fields.Many2one('approval.request', string="Approval")
    category_id = fields.Many2one(related='employee_id.category_id')
    
    
class PortalTimesheetLine(models.Model):
    _name = 'hr.timesheet.report.line'
    _description = 'Hr Timesheet Report Line'
   
    timesheet_repo_id = fields.Many2one('hr.timesheet.report', string='Timesheet Report')
    employee_id = fields.Many2one('hr.employee', string='Employee',  required=True)
    project_id = fields.Many2one('project.project', string='Project')
    date_from = fields.Date(string='Date From')
    date_to  = fields.Date(string='Date To')
    total_days = fields.Float(string='Days')
    
    
    

