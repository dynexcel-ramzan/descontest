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
from csv import DictReader
from csv import DictWriter
import csv
from odoo import models, fields, api, _
from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

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
    approval_request_id = fields.Many2one('approval.request', string="Approval")
    category_id = fields.Many2one(related='incharge_id.timesheet_categ_id')


    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % (self.partner_id.name, self.project_id.name)


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
            line.action_create_approval_request_timesheet()
            line.update({
                'state': 'submitted',
            })

    def action_create_approval_request_timesheet(self):
        approver_ids = []
        request_list = []
        for line in self:
            check_in = False
            check_out = False
            if line.date_from:
                check_in = line.date_from + relativedelta(hours=+ 5)
            if line.date_to:
                check_out = line.date_to + relativedelta(hours=+ 5)
            if line.category_id:
                request_list.append({
                    'name': str(line.partner_id.name),
                    'request_owner_id': line.incharge_id.user_id.id,
                    'category_id': line.category_id.id,
                    'timesheet_id': line.id,
                    'reason': 'Project '+str(line.project_id.name)+ "\n" +' Date From: ' + str(check_in) + "\n" + ' Date To: ' + str(
                        check_out) + "\n" + "\n" + "\n" + ' Client:   ' + str(line.partner_id.name) + "\n",
                    'request_status': 'new',
                })
                approval_request_id = self.env['approval.request'].create(request_list)
                approval_request_id._onchange_category_id()
                approval_request_id.action_confirm()
                approval_request_id.action_date_confirm_update()
                line.approval_request_id = approval_request_id.id


    def action_approve(self):
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
            tot_days = 0
            if  line.date_to and line.date_from:
                tot_days = (line.date_to - line.date_from).days + 1
            line.update({
                'total_days': tot_days,
            })
    
    
    
