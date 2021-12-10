# # -*- coding: utf-8 -*-

from . import config
from . import update
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
import base64

def expense_page_content(flag = 0, expense=0):
    sheet = 0
    sheet_categ= 0
    if expense != 0:
        sheet = request.env['hr.expense.sheet'].sudo().search([('id','=',expense)])
        sheet_categ = sheet.ora_category_id.id
    managers = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
    employees = request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))])
    expense_categories = request.env['ora.expense.category'].sudo().search([])
    products = request.env['product.product'].sudo().search([('ora_category_id','=',sheet_categ)])
    emp_members = request.env['hr.employee.family'].sudo().search([('employee_id','=', employees.id)])
    company_info = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
    managers=employees.parent_id.name
    if sheet!=0:
        managers=sheet.employee_id.parent_id.name
        employees=sheet.employee_id
    return {
        'managers': managers,
        'employees' : employees,
        'products': products,
        'sheet': sheet if sheet!=0 else 0,
        'emp_members': emp_members,
        'employee_name': employees,
        'expense_types': expense_categories,
        'success_flag' : flag,
        'company_info': company_info,
    }

def paging(data, flag1 = 0, flag2 = 0):        
    if flag1 == 1:
        return config.list12
    elif flag2 == 1:
        config.list12.clear()
    else:
        k = []
        for rec in data:
            for ids in rec:
                config.list12.append(ids.id)        
        
class CreateApproval(http.Controller):
    @http.route('/expense/create/',type="http", website=True, auth='user')
    def expense_claim_create_template(self, **kw):
        return request.render("de_portal_expence.create_expense",expense_page_content()) 
          

    @http.route('/my/expense/save', type="http", auth="public", website=True)
    def create_expenses(self, **kw):
        expense_val = {
            'name': kw.get('description'),
            'ora_category_id': int(kw.get('cateory_id')),
            'employee_id': request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))]).id,
            'accounting_date':  fields.date.today(),
        }
        record = request.env['hr.expense.sheet'].sudo().create(expense_val)
        return request.render("de_portal_expence.create_expense_line", expense_page_content(expense=record.id) )
    
    @http.route('/my/expense/line/save', type="http", auth="public", website=True)
    def create_expense_line(self, **kw):
        expense_line = {
            'name': kw.get('description'),
            'reference': kw.get('reference'),
            'sheet_id':  int(kw.get('sheet_id')),
            'unit_amount': float(kw.get('amount')),
            'product_id': int(kw.get('product_id')),
            'sheet_id': int(kw.get('sheet_id')),
            'employee_id': request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))]).id,
            'date':  fields.date.today(),
        }
        record = request.env['hr.expense'].sudo().create(expense_line)
        if kw.get('member_id') !='blank':    
            record.update({
                'member_id': int(kw.get('member_id')),
            })
        if record.sheet_id.ora_category_id.has_vehicle=='optional':
            if kw.get('vehicle_name'): 
                record.update({
                    'vehicle_name': kw.get('vehicle_name'),
                })
        if record.sheet_id.ora_category_id.has_reading=='optional':        
            if kw.get('meter_reading'): 
                record.update({
                    'meter_reading': kw.get('meter_reading'),
                })
        if kw.get('attachment'):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment').filename
            file = kw.get('attachment')
            attachment_id = Attachments.sudo().create({
            'name': 'test',
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_id': record.id,
            'res_model': 'hr.expense', 
             'res_name': record.name,   
             })
            attachment_id = Attachments.sudo().create({
            'name': name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_id': record.sheet_id.id,
            'res_model': 'hr.expense.sheet', 
             'res_name': record.name,   
            })
          
        return request.redirect('/my/expense/%s'%(record.sheet_id.id)) 
    
    
    @http.route('/update/expense/line/save', type="http", auth="public", website=True)
    def action_update_expense_line(self, **kw):
        record = request.env['hr.expense'].sudo().search([('id','=', int(kw.get('expense_id')))])
        if kw.get('product_id')!='blank':
            record.update({
                'product_id': int(kw.get('product_id')),
            })
        if kw.get('member_id')!='blank':
            record.update({
                'member_id': int(kw.get('member_id')),
            })  
        record.update({
            'unit_amount': float(kw.get('amount')),
            'reference': kw.get('reference'),
            'name': kw.get('description'),
        })
        if record.sheet_id.ora_category_id.has_vehicle=='optional':
            if kw.get('vehicle_name'): 
                record.update({
                    'vehicle_name': kw.get('vehicle_name'),
                })
        if record.sheet_id.ora_category_id.has_reading=='optional':        
            if kw.get('meter_reading'): 
                record.update({
                    'meter_reading': kw.get('meter_reading'),
                })        
        if kw.get('attachment'):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment').filename
            file = kw.get('attachment')
            attachment_id = Attachments.sudo().create({
            'name': name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_id': record.id,
            'res_model': 'hr.expense', 
             'res_name': record.name,   
            })
            attachment_id = Attachments.sudo().create({
            'name': name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_id': record.sheet_id.id,
            'res_model': 'hr.expense.sheet', 
             'res_name': record.name,   
            })
            
            
        return request.redirect('/my/expense/%s'%(record.sheet_id.id)) 
    
    
    
    
   

class CustomerPortal(CustomerPortal):
    
    @http.route(['/action/reset/expense/<int:expense_id>'], type='http', auth="public", website=True)
    def action_reset_exepnse_line(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense.sheet'].sudo().browse(expense_id)
        recrd.reset_expense_sheets()
        try:
            expense_sudo = self._document_check_access('hr.expense.sheet', expense_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.redirect('/my/expense/%s'%(recrd.id)) 
    
    @http.route(['/action/vc/approval/<int:expense_id>'], type='http', auth="public", website=True)
    def action_add_vc_approval(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense.sheet'].sudo().browse(expense_id)
        if recrd.employee_id.company_id.chanceller_id:
            if recrd.employee_id.company_id.chanceller_id.user_id:
                vals ={
                    'user_id': recrd.employee_id.company_id.chanceller_id.user_id.id,
                    'request_id': recrd.approval_request_id.id,
                    'status': 'new',
                }
                approvers=request.env['approval.approver'].sudo().create(vals)
        try:
            expense_sudo = self._document_check_access('hr.expense.sheet', expense_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.render("de_portal_expence.re_expense_submited", {})
    
    
    
    @http.route(['/add/expense/line/<int:expense_id>'], type='http', auth="public", website=True)
    def action_add_expense_line(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense.sheet'].sudo().browse(expense_id)
        try:
            expense_sudo = self._document_check_access('hr.expense.sheet', expense_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.render("de_portal_expence.create_expense_line", expense_page_content(expense=expense_sudo.id))
    
    
    @http.route(['/action/submit/expense/<int:expense_id>'], type='http', auth="public", website=True)
    def action_expense_submit(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense.sheet'].sudo().browse(expense_id)
        recrd.action_submit_sheet()
        recrd.action_check_attachment()
        try:
            expense_sudo = self._document_check_access('hr.expense.sheet', expense_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.render("de_portal_expence.portal_my_expense", values)
    
    
    @http.route(['/delete/expense/line/<int:expense_id>'], type='http', auth="public", website=True)
    def action_expense_delete(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense'].sudo().browse(expense_id)
        sheet=recrd.sheet_id.id
        recrd.unlink()
        try:
            expense_sudo = self._document_check_access('hr.expense.sheet', sheet, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.render("de_portal_expence.portal_my_expense", values)
    
    
    @http.route(['/edit/expense/line/<int:expense_id>'], type='http', auth="public", website=True)
    def action_expense_edit_line(self,expense_id , access_token=None, **kw):
        recrd = request.env['hr.expense'].sudo().browse(expense_id)
        try:
            expense_sudo = self._document_check_access('hr.expense', expense_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        employees = request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))])
        values.update({
            'expense':expense_sudo,
            'sheet': expense_sudo.sheet_id,
            'emp_members': request.env['hr.employee.family'].sudo().search([('employee_id','=', employees.id)]),
            'products': request.env['product.product'].sudo().search([('ora_category_id','=',expense_sudo.sheet_id.ora_category_id.id)]),
            'managers': employees.parent_id.name,
            'employee_name': employees,
        })
        return request.render("de_portal_expence.update_expense_line", values)
    
    
    
    
    @http.route(['/expense/accept/<int:expense_id>'], type='http', auth="public", website=True)
    def accept_approval(self,expense_id ,**kw):
        id=expense_id
        recrd = request.env['hr.expense'].sudo().browse(id)
        recrd.action_approve()
        approvals_page = CustomerPortal()
        return approvals_page.portal_my_expenses()
        
    @http.route(['/expense/reject/<int:expense_id>'], type='http', auth="public", website=True)
    def reject_approval(self,expense_id ,**kw):
        id=expense_id
        recrd = request.env['hr.expense'].sudo().browse(id)
        recrd.action_refuse()
        approvals_page = CustomerPortal()
        return approvals_page.portal_my_expenses()   
        
    @http.route(['/app/expense/accept/<int:expense_id>'], type='http', auth="public", website=True)
    def expense_accept(self,expense_id , access_token=None, **kw):
        id=expense_id
        record = request.env['hr.expense'].sudo().browse(id)
        record.action_refuse()
        try:
            expense_sudo = self._document_check_access('hr.expense', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._expense_get_page_view_values(expense_sudo, **kw) 
        return request.render("de_portal_expence.portal_my_expense", values)
        
        
    
    
    

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'expense_count' in counters:
            values['expense_count'] = request.env['hr.expense'].search_count([('employee_id.user_id', '=', http.request.env.context.get('uid') )])
        return values
  
    def _expense_get_page_view_values(self,expense, access_token = None, **kwargs):
        company_info = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
        employee =  request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))])
        values = {
            'page_name' : 'expense',
            'employee_name': employee,
            'managers': employee.parent_id.name,
            'expense' : expense,
            'company_info': company_info,
        }
        return self._get_page_view_values(expense, access_token, values, 'my_expenses_history', False, **kwargs)

    @http.route(['/my/expenses', '/my/expenses/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_expenses(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                         search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': _('Default'), 'order': 'id asc'},
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name desc' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
        
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['draft', 'submit','approve','done','post','cancel'])]},
            'draft': {'label': _('Draft'), 'domain': [('state', '=', 'draft')]},
            'submit': {'label': _('Submitted'), 'domain': [('state', '=', 'submit')]},  
            'approve': {'label': _('Approved'), 'domain': [('state', '=', 'approve')]},
            'done': {'label': _('Posted'), 'domain': [('state', '=', 'done')]}, 
            'post': {'label': _('Paid'), 'domain': [('state', '=', 'post')]},
            'cancel': {'label': _('Cancel'), 'domain': [('state', '=', 'cancel')]},
        }
           
        searchbar_inputs = {
            'id': {'input': 'id', 'label': _('Search in No#')},
            'name': {'input': 'name', 'label': _('Search in Name')},
            'employee_id.name': {'input': 'employee_id.name', 'label': _('Search in Employee')}, 
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        expense_groups = request.env['hr.expense.sheet'].search([])

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
#         domain = []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('employee_id.name', 'all'):
                search_domain = OR([search_domain, [('employee_id.name', 'ilike', search)]])
            if search_in in ('state', 'all'):
                search_domain = OR([search_domain, [('state', 'ilike', search)]])
            domain += search_domain
 
        expense_count = request.env['hr.expense.sheet'].search_count(domain)

        pager = portal_pager(
            url="/my/expenses",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'seissuesarch_in': search_in, 'search': search},
            total=expense_count,
            page=page,
            step=self._items_per_page
        )

        _expenses = request.env['hr.expense.sheet'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_expenses_history'] = _expenses.ids[:100]

        grouped_expenses = [_expenses]
                
        paging(0,0,1)

        paging(grouped_expenses)
        company_info = request.env['res.users'].search([('id','=',http.request.env.context.get('uid'))])
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_expenses': grouped_expenses,
            'page_name': 'expense',
            'default_url': '/my/expenses',
            'pager': pager,
            'company_info': company_info,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("de_portal_expence.portal_my_expenses", values)

   
    @http.route(['/my/expense/<int:expense_id>'], type='http', auth="user", website=True)
    def portal_my_expense(self, expense_id, access_token=None, **kw):
        values = []
        active_user = http.request.env.context.get('uid')
        expense_sudo = request.env['hr.expense.sheet'].sudo().search([('id','=',expense_id)])      
        values = self._expense_get_page_view_values(expense_sudo,access_token, **kw) 
        return request.render("de_portal_expence.portal_my_expense", values)

