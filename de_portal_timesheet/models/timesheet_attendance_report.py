# -*- coding: utf-8 -*-
import base64
import hashlib
import itertools
import logging
import mimetypes
import os
import re
from collections import defaultdict
import uuid
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, ValidationError, MissingError, UserError
from odoo.tools import config, human_size, ustr, html_escape
from odoo.tools.mimetypes import guess_mimetype
import pandas as pd
from csv import DictReader
from csv import DictWriter
import csv

class PortalTimesheet(models.Model):
    _name = 'hr.timesheet.report'
    _description = 'Hr Timesheet Report'
    _rec_name = 'partner_id'
   
    
    partner_id = fields.Many2one('res.partner', string='Client',  required=True)
    project_id = fields.Many2one('project.project', string='Project',  required=True)
    incharge_id = fields.Many2one('hr.employee', string='Incharge',  required=True)
    date_from = fields.Date(string='Date From')
    date_to  = fields.Date(string='Date To')
    timesheet_attendance_ids = fields.One2many('hr.timesheet.report.line', 'timesheet_repo_id',string='Timesheet Lines')
    total_duration = fields.Float(string='Total Days', compute='_compute_total_days')
    entry_attachment_id = fields.Many2many('ir.attachment', relation="files_rel_hr_timesheet_report",
                                           column1="doc_id",
                                           column2="entry_attachment_id",
                                           string="Entry Attachment")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
         ],
        readonly=True, string='Status', default='draft')


    @api.depends('timesheet_attendance_ids')
    def _compute_total_days(self):
        for line in self:
            days = 0
            for pline in line.timesheet_attendance_ids:
                days += pline.total_days
            line.update({
                'total_duration': days
            })

    def action_submit(self):
        for line in self:
            line.update({
                'state': 'submitted',
            })

    def action_approved(self):
        for line in self:
            line.update({
                'state': 'approved',
            })

    def action_refuse(self):
        for line in self:
            line.update({
                'state': 'refused',
            })
    
class PortalTimesheetLine(models.Model):
    _name = 'hr.timesheet.report.line'
    _description = 'Hr Timesheet Report Line'
   
    timesheet_repo_id = fields.Many2one('hr.timesheet.report', string='Timesheet Report')
    employee_id = fields.Many2one('hr.employee', string='Employee',  required=True)
    project_id = fields.Many2one('project.project', string='Project')
    date_from = fields.Date(string='Date From')
    date_to  = fields.Date(string='Date To')
    total_days = fields.Float(string='Days', compute='_compute_line_total_days')



    @api.depends('date_from','date_to')
    def _compute_line_total_days(self):
        for line in self:
            line.update({
                'total_days': (line.date_to - line.date_from).days + 1
            })
    
    
    

