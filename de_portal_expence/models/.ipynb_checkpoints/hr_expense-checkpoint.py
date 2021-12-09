# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    member_id = fields.Many2one('hr.employee.family', string='Dependent', domain="[('employee_id','=',employee_id)]")
    meter_reading = fields.Float(string='Meter Reading')
    vehicle_name = fields.Char(string='Vehicle Name')
    
    
    @api.constrains('meter_reading')
    def _check_meter_reading(self):
        for line in self:
            if line.meter_reading > 0.0 and line.employee_id.vehicle_id:
                if line.employee_id.opening_reading < line.meter_reading:
                    current_reading = line.meter_reading - line.employee_id.opening_reading    
                    if current_reading > line.employee_id.vehicle_id.meter_reading:
                        pass
                    else:
                        raise UserError(_('You Vehicle meter reading does not reach to limit. Current Reading ' +str(current_reading)+' Difference with opening balance less than limit! '+str(line.employee_id.vehicle_id.meter_reading)+' your previous opening reading is '+str(line.employee_id.opening_reading)))
                else:
                    raise UserError(_('You are entering reading '+str(line.meter_reading)+' less than your previous opening reading is '+str(line.employee_id.opening_reading)))