# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError


class EmployeeEobi(models.AbstractModel):
    _name = 'report.de_eobi_report.computation_report'
    _description = 'Employee Eobi Report'

    '''Find Purchase invoices between the date and find total outstanding amount'''

    def _get_report_values(self, docids, data=None):
        docs = self.env['eobi.wizard'].browse(self.env.context.get('active_id'))
        employees = self.env['hr.employee'].search([], limit=1)

        if docs.department_id and docs.location_id:
            employees = self.env['hr.employee'].search(
                [('department_id', '=', docs.department_id.id), ('work_location_id', '=', docs.location_id.id)])

        elif docs.location_id:
            employees = self.env['hr.employee'].search([('work_location_id', '=', docs.location_id.id)], )

        elif docs.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', docs.department_id.id)], )

                                           
        return {
            'docs': docs,
            'employees': employees,
        }












        #         accounting_entries = self.env['account.move.line'].search([('date', '>=', docs.date_from),('date', '<=', docs.date_to),('debit','!=',0.0)])
#         incom_tax_vals = []
#         for move in accounting_entries:


#         payslip = self.env['hr.employee'].search([('employee_id','=',docs.employee_type.id),
#                                                       ('date_from','=', date_from),('date_to','=', date_to)], limit=1)
#         for rule in payslip:
#                 if rule.code == 'INC01':
#                     tax_amount = rule.amount
#           incom_tax_vals.append({
#                 'date_from': move.date,
#                 'tot_net_wage': tax_amount,
#             })








