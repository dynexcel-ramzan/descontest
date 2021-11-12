from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeOtEntitled(models.TransientModel):
    _name = 'employee.entitled'
    _description = 'Employee OT Entitled'

    employee_type_ids = fields.Many2many('employee.type', string='Employee`s Type')
    location_ids = fields.Many2many('hr.work.location', string='Location')
    grade_type_ids = fields.Many2many('grade.type', string='Grade Type')
    department_ids = fields.Many2many('hr.department', string='Department')
    company_ids = fields.Many2many('res.company', string='Companies')

    def action_generate_pdf(self):
        data = {
            'employee_type_ids': self.employee_type_ids.ids,
            'department_ids': self.department_ids.ids,
            'location_ids': self.location_ids.ids,
            'grade_type_ids': self.grade_type_ids.ids,
            'company_ids': self.company_ids.ids}
        return self.env.ref('de_hr_employee_report.action_report_employee_entitled').report_action(self, data=data)

