# -*- coding: utf-8 -*-

import base64

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class HrPayslips(models.Model):
    _inherit = 'hr.payslip'
    
    
    
    @api.onchange('employee_id', 'struct_id', 'date_from', 'date_to')
    def _onchange_employee(self):        
        for payslip in self:            
            if (not payslip.employee_id) or (not payslip.date_from) or (not payslip.date_to):
                return

            employee = payslip.employee_id
            date_from = payslip.date_from
            date_to = payslip.date_to

            payslip.company_id = employee.company_id
            if not payslip.contract_id or payslip.employee_id != payslip.contract_id.employee_id: # Add a default contract if not already defined
                contracts = employee._get_contracts(date_from, date_to)

                if not contracts or not contracts[0].structure_type_id.default_struct_id:
                    payslip.contract_id = False
                    payslip.struct_id = False
                    return
                payslip.contract_id = contracts[0]
                payslip.struct_id = contracts[0].structure_type_id.default_struct_id

            lang = employee.sudo().address_home_id.lang or payslip.env.user.lang
            context = {'lang': lang}
            payslip_name = payslip.struct_id.payslip_name or _('Salary Slip')
            del context

            payslip.name = '%s - %s - %s' % (
                payslip_name,
                payslip.employee_id.name or '',
                format_date(self.env, payslip.date_from, date_format="MMMM y", lang_code=lang)
            )

            if date_to > date_utils.end_of(fields.Date.today(), 'month'):
                payslip.warning_message = _(
                    "This payslip can be erroneous! Work entries may not be generated for the period from %(start)s to %(end)s.",
                    start=date_utils.add(date_utils.end_of(fields.Date.today(), 'month'), days=1),
                    end=date_to,
                )
            else:
                payslip.warning_message = False 

            work_day_line = []    
            work_days = 0
            work_hours = 0 
            
            """
              Employee Attendance Days
            """ 
            emp_attendance = self.env['hr.attendance'].sudo().search([('employee_id','=', employee.id),('att_date','>=', date_from),('att_date','<=', date_to)])
            previous_date = fields.date.today()
            work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','WORK100')], limit=1)
            for attendance in emp_attendance:
                if attendance.check_out and attendance.check_in:
                    new_date = attendance.att_date
                    if new_date != previous_date:
                        daily_leave = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','<=', attendance.att_date),('request_date_to','>=',  attendance.att_date),('state','in',('validate','confirm'))])
                        if daily_leave.number_of_days == 0.5:
                            work_days += 0.5
                            work_hours += attendance.worked_hours / 2
                            
                        elif  daily_leave.number_of_days == 0.25:
                            work_days += 0.75
                            att_hours = attendance.worked_hours / 4 
                            work_hours += attendance.worked_hours - att_hours
                        else:     
                            work_days += 1
                            work_hours += attendance.worked_hours 
                    previous_date = attendance.att_date
            work_day_line.append((0,0,{
               'work_entry_type_id' : work_entry_type.id ,
               'name': work_entry_type.name ,
               'sequence': work_entry_type.sequence ,
               'number_of_days' : work_days ,
               'number_of_hours' : work_hours ,
            }))
                      
            """
              Employee Timoff by Timeoff type wise
            """ 
            
            leave_type = []
            
            total_leave_days = 0
            emp_leaves = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('date_from','>=', date_from),('date_to','<=', date_to),('state','=','validate'),('holiday_status_id.is_rest_day','=',False)])
            previous_date = fields.date.today()
            leave_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','LEAVE100')], limit=1)
            for leave in emp_leaves: 
                leave_type.append(leave.holiday_status_id.id)
            uniq_leave_type = set(leave_type)
            for timeoff_type in uniq_leave_type:
                leave_work_days = 0
                leaves_work_hours = 0 
                emp_leaves_type = self.env['hr.leave'].sudo().search([('holiday_status_id','=', timeoff_type),('employee_id','=', employee.id),('date_from','>=', date_from),('date_to','<=', date_to),('state','=','validate')])
                for timeoff in emp_leaves_type:
                    attendance_exist = self.env['hr.attendance'].sudo().search([('employee_id','=', employee.id),('att_date','>=', timeoff.request_date_from),('att_date','<=', timeoff.request_date_to)])
                    if not attendance_exist:
                        leave_work_days += timeoff.number_of_days
                        total_leave_days += timeoff.number_of_days
                    if timeoff.number_of_days < 1:
                        leave_work_days += timeoff.number_of_days
                        total_leave_days += timeoff.number_of_days 
                timeoff_vals = self.env['hr.leave.type'].sudo().search([('id','=',timeoff_type)], limit=1) 
                
                timeoff_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=',timeoff_vals.name)], limit=1)
                if not timeoff_work_entry_type:
                    vals = {
                        'name': timeoff_vals.name,
                        'code': timeoff_vals.name,
                        'round_days': 'NO',
                    }
                    work_entry = self.env['hr.work.entry.type'].sudo().create(vals)
                timeoff_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=',timeoff_vals.name)], limit=1)

                work_day_line.append((0,0,{
                   'work_entry_type_id' : timeoff_work_entry_type.id,
                   'name': timeoff_work_entry_type.name,
                   'sequence': timeoff_work_entry_type.sequence,
                   'number_of_days' : leave_work_days,
                   'number_of_hours' : leave_work_days * employee.shift_id.hours_per_day ,
                }))               
                
            """
              Employee Absent Days
            """ 
            absent_work_days_initial = 0
            delta = date_from - date_to
            total_days = abs(delta.days)
            for i in range(0, total_days + 1):
                absent_work_days_initial = absent_work_days_initial + 1
            rest_days_initial = 0
            gazetted_days_count = 0
            absent_work_days = 0
            shift_contract_lines = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','>=',date_from),('date','<=',date_to),('state','=','posted')])
            for shift_line in shift_contract_lines:
                if shift_line.first_shift_id:
                    for gazetted_day in shift_line.first_shift_id.global_leave_ids:
                        gazetted_date_from = gazetted_day.date_from +relativedelta(hours=+5)
                        gazetted_date_to = gazetted_day.date_to +relativedelta(hours=+5)
                        if str(shift_line.date.strftime('%y-%m-%d')) >= str(gazetted_date_from.strftime('%y-%m-%d')) and str(shift_line.date.strftime('%y-%m-%d')) <= str(gazetted_date_to.strftime('%y-%m-%d')):
                            gattendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=',shift_line.date)])
                            gdaily_leave = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','<=', shift_line.date),('request_date_to','>=', shift_line.date),('state','in',('validate','confirm'))]) 
                            if gattendance:
                                pass
                            elif gdaily_leave:
                                is_rest_day = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',shift_line.date),('state','=','posted'),('rest_day','=',True)])
                                if not is_rest_day:
                                    gazetted_days_count += 1
                            else:
                                is_rest_day = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',shift_line.date),('state','=','posted'),('rest_day','=',True)])
                                if not is_rest_day:
                                    gazetted_days_count += 1 
                else:
                    current_shift = employee.shift_id
                    if not current_shift:
                        current_shift = self.env['resource.calendar'].sudo().search([('company_id','=', employee.company_id.id)], limit=1)
                    if not current_shift:
                        current_shift = self.env['resource.calendar'].sudo().search([], limit=1)

                    for gazetted_day in current_shift.global_leave_ids:
                        gazetted_date_from = gazetted_day.date_from +relativedelta(hours=+5)
                        gazetted_date_to = gazetted_day.date_to +relativedelta(hours=+5)
                        if str(shift_line.date.strftime('%y-%m-%d')) >= str(gazetted_date_from.strftime('%y-%m-%d')) and str(shift_line.date.strftime('%y-%m-%d')) <= str(gazetted_date_to.strftime('%y-%m-%d')):
                            gattendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=',shift_line.date)])
                            gdaily_leave = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','<=', shift_line.date),('request_date_to','>=', shift_line.date),('state','in',('validate','confirm'))]) 
                            if gattendance:
                                pass
                            elif gdaily_leave:
                                is_rest_day = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',shift_line.date),('state','=','posted'),('rest_day','=',True)])
                                if not is_rest_day:
                                    gazetted_days_count += 1
                            else:
                                is_rest_day = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',shift_line.date),('state','=','posted'),('rest_day','=',True)])
                                if not is_rest_day:
                                    gazetted_days_count += 1
                if shift_line.rest_day == True:
                    exist_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=',shift_line.date)], limit=1)
                    if  exist_attendance.check_in and exist_attendance.check_out:
                        pass
                    else:
                        rest_days_initial += 1  

            gazetted_day_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','Gazetted Days')], limit=1)
            
            if not gazetted_day_work_entry_type:
                vals = {
                    'name': 'Gazetted Days',
                    'code': 'Gazetted Days',
                    'round_days': 'NO',
                }
                work_entry = self.env['hr.work.entry.type'].sudo().create(vals)  
            gazetted_day_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','Gazetted Days')], limit=1)                       
            work_day_line.append((0,0,{
                   'work_entry_type_id' : gazetted_day_work_entry_type.id,
                   'name': gazetted_day_work_entry_type.name,
                   'sequence': gazetted_day_work_entry_type.sequence,
                   'number_of_days' : gazetted_days_count,
                   'number_of_hours' : gazetted_days_count * employee.shift_id.hours_per_day ,
            }))   
            
            """
              Rest Day 
            """
            rest_day_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','Rest Day')], limit=1)
            
            if not rest_day_work_entry_type:
                vals = {
                    'name': 'Rest Day',
                    'code': 'Rest Day',
                    'round_days': 'NO',
                }
                work_entry = self.env['hr.work.entry.type'].sudo().create(vals)  
            rest_day_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','Rest Day')], limit=1)    
            work_day_line.append((0,0,{
               'work_entry_type_id' : rest_day_work_entry_type.id,
               'name': rest_day_work_entry_type.name,
               'sequence': rest_day_work_entry_type.sequence,
               'number_of_days' : rest_days_initial ,
               'number_of_hours' : rest_days_initial * employee.shift_id.hours_per_day ,
            }))
            absent_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','ABSENT100')], limit=1)
            if not absent_work_entry_type:
                vals = {
                    'name': 'Absent Days',
                    'code': 'ABSENT100',
                    'round_days': 'NO',
                }
                work_entry = self.env['hr.work.entry.type'].sudo().create(vals)
            apply_leave_days = 0    
            emp_leaves_apply = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('date_from','>=', date_from),('date_to','<=', date_to),('state','=','validate')]) 
            for leave_apply in emp_leaves_apply:
                apply_leave_days += leave_apply.number_of_days
            
            absent_work_days = absent_work_days_initial - (gazetted_days_count + rest_days_initial + total_leave_days + work_days)
            absent_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','ABSENT100')], limit=1)
            
            work_day_line.append((0,0,{
               'work_entry_type_id' : absent_work_entry_type.id,
               'name': absent_work_entry_type.name,
               'sequence': absent_work_entry_type.sequence,
               'number_of_days' : absent_work_days if absent_work_days > 0.0 else 0,
               'number_of_hours' : (absent_work_days if absent_work_days > 0.0 else 0) * employee.shift_id.hours_per_day ,
            }))
            

            if not payslip.worked_days_line_ids:
                payslip.worked_days_line_ids = work_day_line


    