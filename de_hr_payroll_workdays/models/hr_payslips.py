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
                format_date(self.env, payslip.date_to, date_format="MMMM y", lang_code=lang)
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
                        if daily_leave:
                            for dleave in daily_leave:
                                if dleave.number_of_days == 0.5:
                                    work_days += 0.5
                                    work_hours += attendance.worked_hours / 2

                                elif  dleave.number_of_days == 0.25:
                                    work_days += 0.75
                                    att_hours = attendance.worked_hours / 4
                                    work_hours += attendance.worked_hours - att_hours
                                else:
                                    if (attendance.shift_id.hours_per_day - 1.5) > attendance.worked_hours and (attendance.worked_hours > 0.0):
                                        work_days += 0.5
                                        work_hours += attendance.worked_hours/2
                                    else:
                                        if (attendance.worked_hours > (attendance.shift_id.hours_per_day - 1.5)):
                                            work_days += 1
                                            work_hours += attendance.worked_hours
                        else:
                            if (attendance.shift_id.hours_per_day - 1.5) > attendance.worked_hours and (attendance.worked_hours > (attendance.shift_id.hours_per_day/2)):
                                work_days += 0.5
                                work_hours += attendance.worked_hours/2
                            else:
                                if (attendance.worked_hours > (attendance.shift_id.hours_per_day - 1.5)):
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
            emp_leaves = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','>=', date_from),('request_date_to','<=', date_to),('state','=','validate'),('holiday_status_id.is_rest_day','=',False)])
            last_day_leaves = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','=', date_to),('state','=','validate'),('holiday_status_id.is_rest_day','=',False)], limit=1)
            start_day_leaves = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','<=', date_from),('request_date_to','>=', date_from),('state','=','validate'),('holiday_status_id.is_rest_day','=',False)])        
            start_in_leaves = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','>=', date_from),('request_date_from','<=', date_to),('request_date_to','>=', date_to),('state','=','validate'),('holiday_status_id.is_rest_day','=',False)])
            previous_date = fields.date.today()
            leave_work_entry_type = self.env['hr.work.entry.type'].sudo().search([('code','=','LEAVE100')], limit=1)
            for lastleave in last_day_leaves: 
                leave_type.append(lastleave.holiday_status_id.id)
            for start_in in start_in_leaves: 
                leave_type.append(start_in.holiday_status_id.id)
            for leave in emp_leaves: 
                leave_type.append(leave.holiday_status_id.id)
            for startleave in start_day_leaves: 
                leave_type.append(startleave.holiday_status_id.id)
            uniq_leave_type = set(leave_type)
            for timeoff_type in uniq_leave_type:
                leave_work_days = 0
                leaves_work_hours = 0 
                emp_leaves_type = self.env['hr.leave'].sudo().search([('holiday_status_id','=', timeoff_type),('employee_id','=', employee.id),('request_date_from','>=', date_from),('request_date_to','<=', date_to),('state','=','validate')])
                last_emp_leaves_type = self.env['hr.leave'].sudo().search([('holiday_status_id','=', timeoff_type),('employee_id','=', employee.id),('request_date_from','=', date_to),('state','=','validate')], limit=1)
                start_day_leaves_type = self.env['hr.leave'].sudo().search([('holiday_status_id','=', timeoff_type),('employee_id','=', employee.id),('request_date_from','<=', date_from),('request_date_to','>=', date_from),('state','=','validate')], limit=1)
                start_day_in_leaves_type = self.env['hr.leave'].sudo().search([('holiday_status_id','=', timeoff_type),('employee_id','=', employee.id),('request_date_from','>=', date_from),('request_date_from','<=', date_to),('request_date_to','>=', date_to),('state','=','validate')], limit=1)
                if start_day_in_leaves_type:
                    if start_day_in_leaves_type.number_of_days <= 1:
                        leave_work_days += start_day_in_leaves_type.number_of_days
                        total_leave_days += start_day_in_leaves_type.number_of_days
                    else:
                        unsettle_day_in_count = 0
                        uniq_in_diff = (date_to - start_day_in_leaves_type.request_date_from).days+1
                        unsettle_day_in_date = start_day_in_leaves_type.request_date_from
                        for unsettle_in_day in range(uniq_in_diff):
                            unsettle_day_in_date = unsettle_day_in_date + timedelta(1)
                            is_unrest_in_day=self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=',employee.id),('date','=',unsettle_day_in_date)], limit=1)  
                            if is_unrest_in_day:
                                if is_unrest_in_day.rest_day==True: 
                                    unsettle_day_in_count += 1
                                elif is_unrest_in_day.first_shift_id:
                                    is_ungazetted_in_day=self.env['shift.gazetted.line'].sudo().search([('shift_id','=',is_unrest_in_day.first_shift_id.id),('date','=',unsettle_day_in_date)], limit=1)
                                    if is_ungazetted_in_day:
                                        unsettle_day_in_count += 1
                        leave_work_days += (uniq_in_diff - unsettle_day_in_count)
                        total_leave_days += (uniq_in_diff - unsettle_day_in_count)
                if start_day_leaves_type:
                    if start_day_leaves_type.number_of_days <= 1:
                        leave_work_days += start_day_leaves_type.number_of_days
                        total_leave_days += start_day_leaves_type.number_of_days
                    else:
                        unsettle_day_count = 0
                        uniq_diff = (date_from - start_day_leaves_type.request_date_from).days+1
                        unsettle_day_date = start_day_leaves_type.request_date_from
                        for unsettle_day in range(uniq_diff):
                            unsettle_day_date = unsettle_day_date + timedelta(1)
                            is_unrest_day=self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=',employee.id),('date','=',unsettle_day_date)], limit=1)  
                            if is_unrest_day:
                                if is_unrest_day.rest_day==True: 
                                    unsettle_day_count += 1
                                elif is_unrest_day.first_shift_id:
                                    is_ungazetted_day=self.env['shift.gazetted.line'].sudo().search([('shift_id','=',is_unrest_day.first_shift_id.id),('date','=',unsettle_day_date)], limit=1)
                                    if is_ungazetted_day:
                                        unsettle_day_count += 1
                        leave_work_days += start_day_leaves_type.number_of_days - (uniq_diff - unsettle_day_count)
                        total_leave_days += start_day_leaves_type.number_of_days - (uniq_diff - unsettle_day_count)    
                if last_emp_leaves_type:
                    if last_emp_leaves_type.number_of_days < 1:
                        leave_work_days += last_emp_leaves_type.number_of_days
                        total_leave_days += last_emp_leaves_type.number_of_days
                    else:
                        leave_work_days += 1
                        total_leave_days += 1
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
            emp_leaves_apply = self.env['hr.leave'].sudo().search([('employee_id','=', employee.id),('request_date_from','>=', date_from),('request_date_to','<=', date_to),('state','=','validate')]) 
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


    