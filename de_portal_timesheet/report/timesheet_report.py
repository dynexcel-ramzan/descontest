# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime , date
from datetime import date, datetime, timedelta


class HrTimesheetReport(models.AbstractModel):
    _name = 'report.de_portal_timesheet.timesheet_report'
    _description = 'Timesheet Report'
    
    
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.timesheet.report'].browse(self.env.context.get('active_id'))
        wizarddocs = self.env['timesheet.reprot.wizard'].browse(self.env.context.get('active_id'))
        project = self.env['project.project'].search([], limit=1)
        date_from = fields.Date.today()
        date_to = fields.Date.today()
        if not wizarddocs:
            project = self.env['project.project'].search([('id','=',data['project'])], limit=1)
            date_from = datetime.strptime(str(data['start_date']), "%Y-%m-%d")
            date_to = datetime.strptime(str(data['end_date']), "%Y-%m-%d")
        if wizarddocs:
            project = self.env['project.project'].search([('id','=',wizarddocs.project_id.id)], limit=1)
            date_from = wizarddocs.date_from
            date_to = wizarddocs.date_to
            
        days = (date_to - date_from).days + 1
        employees = []
        timesheet_list = []
        timesheet_report = self.env['hr.timesheet.report'].search([('project_id','=', project.id)], limit=1)
        for day in range(days): 
            start_date_from = date_from + timedelta(day)
            attendance_present = ' '
            report_line = self.env['hr.timesheet.report.line'].search([('project_id','=', project.id)], limit=1)
            if report_line:
                timesheet_report = report_line.timesheet_repo_id
                employees.append(report_line.employee_id.id)
                  
        uniq_employee_list =  set(employees)
        employees = self.env['hr.employee'].search([('id','in',uniq_employee_list)])
        return {
            'project': project,
            'employees': employees,
            'timesheet_report': timesheet_report,
            'days': days,
            'docs':docs,
            'docs_date_from': date_from,
            'docs_date_to': date_to,
            'date_from': date_from.strftime('%d %B %y'),
            'date_to': date_to.strftime('%d %B %y') ,
           }

    
    
