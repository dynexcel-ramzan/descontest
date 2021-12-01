# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OvertimeReport(models.AbstractModel):
    _name = 'report.de_department_wise_ot_report.overtime_report'
    _description = 'Employee Overtime Report Deparmtent Wise'

    
    
    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['department.wise.wizard'].browse(self.env.context.get('active_id'))
        
        
        return {
            'docs': docs,
        }