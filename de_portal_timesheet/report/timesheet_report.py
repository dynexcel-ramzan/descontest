# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrTimesheetReport(models.AbstractModel):
    _name = 'report.de_portal_timesheet.timesheet_report'
    _description = 'Timesheet Report'
    
    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        project = self.env['project.project'].search([('id','=',data['project'])], limit=1)
        date_from = datetime.strptime(str(data['start_date']), "%Y-%m-%d")
        date_to = datetime.strptime(str(data['end_date']), "%Y-%m-%d")
        days = (date_to - date_from).days + 1
        for day in range(days): 
            start_date_from = date_from + timedelta(day)
            
            report_line = self.env['hr.timesheet.report.line'].search([('date_from','>=', start_date_from),('date_to','<=', start_date_from)], limit=1)
            if report_line:
                attendance= self.env['hr.attendance'].search([('employee_id','=',report_line.employee_id.id),('att_date','=',start_date_from)])
                if attendance:
                    
           
        return {
            'project': project,
            'date_from': date['start_date'].strftime('%d %B %y'),
            'date_to': data['end_date'].strftime('%d %B %y') ,
           }
