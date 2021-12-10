# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    ora_category_id = fields.Many2one('ora.expense.category', string='Expense Category')
    
    def action_check_attachment(self):
        for line in self:
            if line.ora_category_id.is_attachment=='required':
                attachments=self.env['ir.attachment'].search([('res_id','=',line.id),('res_model','=','hr.expense.sheet')])
                if not attachments:
                     raise UserError(_('Please Add Attachment! You are not allow to submit '+str(line.sheet_id.ora_category_id.name)+ ' Expense claim without attachment.'))    
    

class hr_expense(models.Model):
    _inherit = 'hr.expense'
    
    
    def action_draft(self):
        self.update({
            'state': 'draft'
        })
        self.sheet_id.reset_expense_sheets()
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'         

    
class UomUom(models.Model):
    _inherit = 'uom.uom'         
        
    
class hr_employee_public(models.Model):
    _inherit = 'hr.employee.public' 
    

class ProductProduct(models.Model):
    _inherit = 'product.product'    
    
class GradeDesignationline(models.Model):
    _inherit = 'grade.designation.line'     

  
class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'     
    
class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'     
           
    
class MailActivity(models.Model):
    _inherit = 'mail.activity'     