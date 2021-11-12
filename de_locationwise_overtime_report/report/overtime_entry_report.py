import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class OvertimeEntery(models.AbstractModel):
    _name = 'report.de_locationwise_overtime_report.overtime_entery'
    _description = 'location wise'


    @api.model
    def _get_report_values(self,docids, data=None):
        docs = self.env['overtime.entery.wizard'].browse(self.env.context.get('active_id'))
        
        overtime_entries = []
        employees = self.env['hr.employee'].search([('work_location_id','=',docs.location_ids.ids)])
        raise UserError(str(employess))
        sr_no = 0
        for emp in employees:
            employees_ovt = self.env['hr.overtime.entry'].search([('employee_id','=', emp.id),('date', '>=', docs.date_from),('date', '<=', docs.date_to)])
            amount_sum = hours_sum = 0
            sr_no += 1
            for entry in employees_ovt:
                amount_sum += entry.amount
                hours_sum += entry.overtime_hours
                overtime_entries.append({
                    'location': emp.work_location_id.name,
                    'sr_no': sr_no,
                    'employee_id': emp.name,
                    'amount': amount_sum,
                    'hours_sum': hours_sum,
                    'arrears': ' ',
                    'tot_amount' amount_sum,
                })
        
        return {
            'overtime_entries': overtime_entries,
        }