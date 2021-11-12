from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeRetirement(models.TransientModel):
    _name = 'employee.retirement'
    _description = 'Employee Retirement'

    employee_type_ids = fields.Many2many('employee.type', string='Employee`s Type')
    location_ids = fields.Many2many('hr.work.location', string='Location')
    grade_type_ids = fields.Many2many('grade.type', string='Grade Type')
    department_ids = fields.Many2many('hr.department', string='Department')
    company_ids = fields.Many2many('res.company', string='Companies')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    

    def action_generate_pdf(self):
        data = {
            'employee_type_ids': self.employee_type_ids.ids,
            'department_ids': self.department_ids.ids,
            'location_ids': self.location_ids.ids,
            'grade_type_ids': self.grade_type_ids.ids,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'company_ids': self.company_ids.ids}
        return self.env.ref('de_hr_employee_report.action_report_employee_retirement').report_action(self, data=data)

