# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrOvertimeWizard(models.TransientModel):
    _name = "hr.overtime.wizard"
    _description = "Overtime Report wizard"

    date_from = fields.Date(string='Date form', required=True)
    date_to = fields.Date(string='Date to', required=True)
    location_ids = fields.Many2many('hr.work.location', string='Location')
    department_ids = fields.Many2many('hr.department', string='department')
    

    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to','location_ids','department_ids'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from', 'date_to','location_ids','department_ids'])[0])
        return self.env.ref('de_overtime_location_report.open_hr_report_wizard_action').report_action(self, data=data, config=False)