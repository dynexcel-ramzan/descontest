from odoo import models, fields, api, _
from datetime import datetime
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError 
import math
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
  
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

    
class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    is_overtime = fields.Boolean(string="Approved Overtime")
    company_id = fields.Many2one(related='employee_id.company_id')
    rounded_hours = fields.Float(string='Rounded Work Hours', compute='_compute_rounded_worked_hours',  readonly=True)
    
    @api.depends('check_in', 'check_out')
    def _compute_rounded_worked_hours(self):
        for attendance in self:
            if attendance.check_out and attendance.check_in:
                delta = attendance.check_out - attendance.check_in
                extra_time = 0
                actual_time = delta.total_seconds() / 3600.0
                timein_hours = math.floor(actual_time)
                round_timein_seconds = timein_hours * 3600.0
                extra_seconds = delta.total_seconds() - round_timein_seconds
                if extra_seconds >= 1800:
                    extra_time = 1800
                else:
                    extra_time = 0
                final_delta = round_timein_seconds + extra_time   
                attendance.rounded_hours = final_delta / 3600.0
            else:
                attendance.rounded_hours = False
                
                
                
                
    
    
    
    @api.depends('check_in')
    def _compute_date(self):
        for line in self:
            if line.check_in:
                date = line.check_in
                attendance_date = date.strftime('%Y-%m-%d')
                self.date = attendance_date
                
                
                
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
    
    
    
        
        
    def cron_create_overtime(self):
        attendances=self.env['hr.attendance'].search([('employee_id.allow_overtime','=',True),('is_overtime','=',False)])

