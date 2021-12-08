# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TimesheetReportWizard(models.TransientModel):
    _name = "timesheet.reprot.wizard"
    _description = "Timesheet Report wizard"

    project_id = fields.Many2one('project.project', string='Project', required=True)
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    
    
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to','project_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from', 'date_to','project_id'])[0])
        return self.env.ref('de_portal_timesheet.timesheet_report').report_action(self, data=data, config=False)
    

