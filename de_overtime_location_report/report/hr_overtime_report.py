# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OvertimeReport(models.AbstractModel):
    _name = 'report.de_overtime_location_report.overtime_report'
    _description = 'Hr Overtime Report'

    
    
    
    def _get_report_values(self, docids, data=None):
        overtime_entries = []
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        amount_sum = hours_sum = 0
        sr_no = 1
        
        for location in docs.location_ids:
            tot_amount_sum = tot_hours_sum = 0
            employees = self.env['hr.employee'].search([('work_location_id','=',location.id)])

            for emp in employees:
                employees_ovt = self.env['hr.overtime.entry'].search([('employee_id','=', emp.id),('date', '>=', docs.date_from),('date', '<=', docs.date_to)])
                amount_sum = hours_sum = 0
                for entry in employees_ovt:
                    amount_sum += entry.amount
                    hours_sum += entry.overtime_hours
                    tot_amount_sum += entry.amount
                    tot_hours_sum += entry.overtime_hours
                if   amount_sum > 0:  
                    overtime_entries.append({
                        'location': ' ',
                        'sr_no': sr_no,
                        'employee_id': emp.name,
                        'employee_no': emp.emp_number,
                        'amount': amount_sum,
                        'hours_sum': hours_sum,
                        'arrears': ' ',
                        'tot_amount': amount_sum,
                    })
                    
                    sr_no += 1
            overtime_entries.append({
                        'location': location.name,
                        'sr_no': ' ',
                        'employee_id': ' ',
                        'employee_no': ' ',
                        'amount': tot_amount_sum,
                        'hours_sum': tot_hours_sum,
                        'arrears': ' ',
                        'tot_amount': tot_amount_sum,
                    })

        return {
            'docs': docs,
            'overtime_entries': overtime_entries,
        }
