import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _
from datetime import datetime
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError 
import math
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class HrOvertimeAllocate(models.TransientModel):
    _name = 'hr.overtime.allocate'
    _description = 'Hr Overtime Allocate Wizard'

    date_start = fields.Date(string='Date From')
    date_end = fields.Date(string='Date To')
    

    
    
    def get_normal_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Normal Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
            if work_location:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                if not overtime_type:
                    if employee_company:
                        overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company)], limit=1)
                        if not overtime_type:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
                        
        return overtime_type
    
    
    
    def get_gazetted_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Gazetted Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1) 
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1) 

                if work_location: 
                    overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                    if not overtime_type:
                        if employee_company:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company)], limit=1)
                            if not overtime_type:
                                overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1)    

                        
        return overtime_type
    
    
    
        
    def get_rest_days_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Rest Day Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)
                if work_location:
                    overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                    if not overtime_type:
                        if employee_company:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company)], limit=1)
                            if not overtime_type:
                                overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)    

                        
        return overtime_type
    
    
    
        
        
    def action_create_overtime(self):
        employees = self.env['hr.employee'].search([('allow_overtime','=',True),('id','!=',3653)], order='id asc')
        for employee in employees:
            employee_company = employee.company_id.id
            work_location = employee.work_location_id.id
            day_min_ovt = 0
            day_max_ovt = 0
            month_min_ovt = 0
            month_max_ovt = 0
            overtime_rule = self.env['hr.overtime.rule'].search([('company_id','=',employee.company_id.id)])
            for rule in overtime_rule:
                if rule.rule_period == 'day' and rule.rule_type == 'minimum':
                    day_min_ovt = rule.hours
                elif rule.rule_period == 'day' and rule.rule_type == 'maximum':
                    day_max_ovt = rule.hours
                elif rule.rule_period == 'month' and rule.rule_type == 'minimum':
                    month_min_ovt = rule.hours
                elif rule.rule_period == 'month' and rule.rule_type == 'maximum':
                    month_max_ovt = rule.hours
            month_ovt_hours = 0
            month_total_hours = 0
            attendance_ids = []
            date_of_execution_start = self.date_start
            date_of_execution_end = self.date_end
            employee_attendance = self.env['hr.attendance'].search([('is_overtime','=',False),('employee_id','=',employee.id),('att_date','>=',date_of_execution_start),('att_date','<=',date_of_execution_end)])
            for attendance in employee_attendance:
                overtime_request = self.env['hr.overtime.request'].search([('employee_id','=', employee.id),('date','>=',attendance.check_in),('date','<=',attendance.check_out)])
                ovt_hours = 0
                for ovt_req in overtime_request:
                    ovt_hours  = ovt_hours + ovt_req.overtime_hours
                if ovt_hours <= month_max_ovt:
                    overtime_limit = 0
                    if employee.shift_id.hours_per_day:
                        overtime_limit = attendance.rounded_hours - employee.shift_id.hours_per_day
                    else:
                        overtime_limit = attendance.rounded_hours - 8
                    request_date = attendance.att_date
                    if attendance.check_in:
                        request_date = attendance.check_in
                    ovt_request_date = attendance.att_date.strftime('%Y-%m-%d')
                    # get normal overtime type
                    overtime_type = self.get_normal_overtime_type(employee_company, work_location)

                    for gazetted_day in attendance.shift_id.global_leave_ids:
                        gazetted_date_from = gazetted_day.date_from +relativedelta(hours=+5)
                        gazetted_date_to = gazetted_day.date_to +relativedelta(hours=+5)
                        if str(attendance.att_date.strftime('%y-%m-%d')) >= str(gazetted_date_from.strftime('%y-%m-%d')) and str(attendance.att_date.strftime('%y-%m-%d')) <= str(gazetted_date_to.strftime('%y-%m-%d')):
                            # get gazetted overtime type
                            overtime_type = self.get_gazetted_overtime_type(employee_company, work_location)

                    shift_schedule_lines = self.env['hr.shift.schedule.line'].search([('employee_id','=', attendance.employee_id.id),('rest_day','=',True),('date','=',attendance.att_date)])

                    for rest_day in shift_schedule_lines:
                        if rest_day.rest_day==True:
                            # get Rest Days overtime type
                            overtime_type = self.get_rest_days_overtime_type(employee_company, work_location)

                    if overtime_type.type == 'rest_day':
                        if overtime_limit < 0 and attendance.rounded_hours > 0:
                            vals = {
                                        'employee_id': employee.id,
                                        'company_id': employee.company_id.id,
                                        'date':  ovt_request_date,
                                        'date_from': attendance.check_in,
                                        'date_to': attendance.check_out,
                                        'hours': attendance.rounded_hours,
                                        'overtime_hours': 0,
                                        'actual_ovt_hours': attendance.rounded_hours,
                                        'overtime_type_id': overtime_type.id,
                                    }
                            overtime_lines = self.env['hr.overtime.request'].create(vals)
                            attendance.update({
                                'is_overtime': True
                            })

                        elif overtime_limit > 0:
                            vals = {
                                        'employee_id': employee.id,
                                        'company_id': employee.company_id.id,
                                        'date':  ovt_request_date,
                                        'date_from': attendance.check_in,
                                        'date_to': attendance.check_out,
                                        'hours': attendance.rounded_hours,
                                        'actual_ovt_hours': attendance.rounded_hours,
                                        'overtime_hours': overtime_limit,
                                        'overtime_type_id': overtime_type.id,
                                    }
                            overtime_lines = self.env['hr.overtime.request'].create(vals)
                            attendance.update({
                                'is_overtime': True
                            })


                    elif overtime_type.type == 'gazetted':
                        if overtime_limit < 0 and attendance.rounded_hours > 0:
                            vals = {
                                        'employee_id': employee.id,
                                        'company_id': employee.company_id.id,
                                        'date':  ovt_request_date,
                                        'date_from': attendance.check_in,
                                        'date_to': attendance.check_out,
                                        'hours': attendance.rounded_hours,
                                        'actual_ovt_hours': attendance.rounded_hours,
                                        'overtime_hours': 0,
                                        'overtime_type_id': overtime_type.id,
                                    }
                            overtime_lines = self.env['hr.overtime.request'].create(vals)
                            attendance.update({
                                'is_overtime': True
                            })

                        elif overtime_limit > 0:
                            vals = {
                                        'employee_id': employee.id,
                                        'company_id': employee.company_id.id,
                                        'date':  ovt_request_date,
                                        'date_from': attendance.check_in,
                                        'date_to': attendance.check_out,
                                        'hours': attendance.rounded_hours,
                                        'actual_ovt_hours': attendance.rounded_hours,
                                        'overtime_hours': overtime_limit,
                                        'overtime_type_id': overtime_type.id,
                                    }
                            overtime_lines = self.env['hr.overtime.request'].create(vals)
                            attendance.update({
                                'is_overtime': True
                            })
                    else:
                        if overtime_limit > day_min_ovt:
                            month_ovt_hours = month_ovt_hours +  overtime_limit

                            if overtime_limit > 0:
                                vals = {
                                        'employee_id': employee.id,
                                        'company_id': employee.company_id.id,
                                        'date':  ovt_request_date,
                                        'date_from': attendance.check_in,
                                        'date_to': attendance.check_out,
                                        'hours': attendance.rounded_hours,
                                        'overtime_hours': overtime_limit,
                                        'actual_ovt_hours': overtime_limit,
                                        'overtime_type_id': overtime_type.id,
                                     }
                                overtime_lines = self.env['hr.overtime.request'].create(vals)
                                attendance.update({
                                   'is_overtime': True
                                })
