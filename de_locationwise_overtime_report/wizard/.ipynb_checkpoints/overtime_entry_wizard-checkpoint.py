from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OvertimeEntryWizard(models.Model):

    _name = 'overtime.location.wizard'
    _description = 'Overtime Location Wizard'
    
    date_form = fields.Date(string='Date form', required=True)
    date_to = fields.Date(string='Date to', required=True)
    location_ids = fields.Many2many('hr.work.location', string='Location')
    department_ids = fields.Many2many('hr.department', string='department')
    
    def print_report(self):
        data = {}
        data['form'] = self.read(['date_form', 'date_to','location_ids'])[0]
        return self._print_report(data)

    def _print_report(self,data):

        data = {}
        return self.env.ref('de_locationwise_overtime_report.open_locationwise_report_data').report_action(self, data=data, config=False)