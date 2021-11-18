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
    _name = 'report.de_employee_eobi_report.computation_report'
    _description = 'Employee Eobi Report'

    '''Find Purchase invoices between the date and find total outstanding amount'''

    def _get_report_values(self, docids, data=None):
        docs = self.env['employee.eobi.wizard'].browse(self.env.context.get('active_id'))
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






