# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OvertimeReport(models.AbstractModel):
    _name = 'report.de_employee_service_award.long_service_report'
    _description = 'Employee Overtime Report Deparmtent Wise'

    
    def _get_date(self,doc_date,employee_date):
        
        rdelta = relativedelta(doc_date, employee_date)
        return str(rdelta.years)+"Y-"+str(rdelta.months)+"M-"+str(rdelta.days)+"D"
    
    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['long.service.wizard'].browse(self.env.context.get('active_id'))
        
        
        return {
            'docs': docs,
            'get_date':self._get_date
        }