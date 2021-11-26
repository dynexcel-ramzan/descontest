# # -*- coding: utf-8 -*-
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from datetime import datetime, date
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
import base64
import binascii
import json
import ast

def timesheet_page_content(flag=0):
    projects = request.env['project.project'].sudo().search([('ora_enabled','=', True),('ora_close_date','>=',fields.date.today()),('ora_status','=','approved')])
    employees = request.env['hr.employee'].sudo().search([])
    partners = request.env['res.ora.client'].sudo().search([])
    company_info = request.env['res.users'].sudo().search([('id', '=', http.request.env.context.get('uid'))])
    employee_name = employees
    return {
        'projects': projects,
        'partners': partners,
        'employees': employees,
        'success_flag': flag,
        'company_info': company_info
    }

def timesheet_line_page_content(project,datefrom,dateto):
    uprojects = request.env['project.project'].sudo().search([('id','=',project)])
    employees = request.env['hr.employee'].sudo().search([('timesheet_incharge_id.user_id','=',http.request.env.context.get('uid'))])
    upartner = request.env['res.ora.client'].search([('id','=',uprojects.ora_client_id.id)])
    company_info = request.env['res.users'].sudo().search([('id', '=', http.request.env.context.get('uid'))])
    return {
        'partner': upartner,
        'project': uprojects,
        'emps': employees,
        'datefrom': datefrom,
         'dateto': dateto,
        'company_info': company_info
    }


class CreateTimesheet(http.Controller):

    @http.route('/timesheet/create/', type="http", website=True, auth='user')
    def timesheet_create_template(self, **kw):
        return request.render("de_portal_timesheet.project_timesheet_template", timesheet_page_content())

    @http.route('/project/timesheet/next', type="http", auth="public", website=True)
    def project_timesheet_next_forms(self, **kw):
        project = int(kw.get('project_id'))
        datefrom = kw.get('date_from')
        dateto = kw.get('date_to')
        return request.render("de_portal_timesheet.portal_create_timesheet_report_lines", timesheet_line_page_content(project,datefrom,dateto))

    @http.route('/project/timesheet/line/save', type="http", auth="public", website=True)
    def project_timesheet_submit_forms(self, **kw):
        vals = {
            'incharge_id': request.env['hr.employee'].sudo().search([('user_id','=', http.request.env.context.get('uid'))]).id,
            'partner_id': int(kw.get('partner_id')),
            'project_id': int(kw.get('project_id')),
            'date_from': kw.get('docsdate_from'),
             'date_to': kw.get('docsdate_to'),
        }
        sheet_report = request.env['hr.timesheet.report'].sudo().create(vals)
        timesheet_attendance_list = ast.literal_eval(kw.get('timesheet_attendance_vals'))
        count = 0
        for ptime in timesheet_attendance_list:
            count += 1
            if count > 1:
                line_vals = {
                    'timesheet_repo_id': sheet_report.id,
                    'project_id': int(kw.get('project_id')),
                    'employee_id': int(ptime['employee']),
                    'date_from': ptime['datefrom'],
                    'date_to': ptime['dateto'],
                }
                record_lines = request.env['hr.timesheet.report.line'].sudo().create(line_vals)
        sheet_report.action_submit()
        return request.render("de_portal_timesheet.ptimesheet_submited", {})


class CustomerPortal(CustomerPortal):


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ptimesheet_count' in counters:
            values['ptimesheet_count'] = request.env['hr.timesheet.report'].search_count(
                [('incharge_id.user_id', '=', http.request.env.context.get('uid'))])
        return values

    def _ptimesheet_get_page_view_values(self, ptimesheet, next_id=0, pre_id=0, ptimesheet_user_flag=0, access_token=None,
                                      **kwargs):
        company_info = request.env['res.users'].search([('id', '=', http.request.env.context.get('uid'))])
        values = {
            'page_name': 'ptimesheet',
            'ptimesheet': ptimesheet,
            'current_date': fields.date.today(),
            'ptimesheet_user_flag': ptimesheet_user_flag,
            'next_id': next_id,
            'company_info': company_info,
            'pre_id': pre_id,
        }
        return self._get_page_view_values(ptimesheet, access_token, values, 'my_ptimesheet_history', False, **kwargs)

    @http.route(['/project/timesheets', '/project/timesheet/page/<int:page>'], type='http', auth="user", website=True)
    def portal_project_timesheets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                           search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'incharge_id': {'label': _('Incharge'), 'order': 'incharge_id desc'},
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'),
            'domain': [('state', 'in', ['draft', 'submitted', 'refused', 'approved'])]},
            'draft': {'label': _('To Submit'), 'domain': [('state', '=', 'draft')]},
            'submitted': {'label': _('Cancelled'), 'domain': [('state', '=', 'submitted')]},
            'refused': {'label': _('To Approve'), 'domain': [('state', '=', 'refused')]},
            'approved': {'label': _('Refused'), 'domain': [('state', '=', 'approved')]},
        }
        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Employee')},
            'id': {'input': 'id', 'label': _('Search in Ref#')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        ptimesheet_groups = request.env['hr.timesheet.report'].search([])

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

            # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            domain += search_domain
        domain += [('incharge_id.user_id', '=', http.request.env.context.get('uid'))]
        ptimesheet_count = request.env['hr.timesheet.report'].search_count(domain)

        # pager
        pager = portal_pager(
            url="/project/timesheets",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in, 'search': search},
            total=ptimesheet_count,
            page=page,
            step=self._items_per_page
        )

        _ptimesheet = request.env['hr.timesheet.report'].sudo().search(domain, order=order, limit=self._items_per_page,
                                                         offset=pager['offset'])
        request.session['my_ptimesheet_history'] = _ptimesheet.ids[:100]

        grouped_ptimesheets = [_ptimesheet]

        company_info = request.env['res.users'].search([('id', '=', http.request.env.context.get('uid'))])
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_ptimesheets': grouped_ptimesheets,
            'page_name': 'ptimesheets',
            'default_url': '/project/timesheets',
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
        return request.render("de_portal_timesheet.portal_project_timesheets", values)

    @http.route(['/project/timesheet/<int:timesheet_id>'], type='http', auth="user", website=True)
    def portal_project_timesheet(self, timesheet_id, access_token=None, **kw):
        try:
            timesheet_sudo = self._document_check_access('hr.timesheet.report', timesheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        next_id = 0
        pre_id = 0
        timesheet_user_flag = 0
        values = self._ptimesheet_get_page_view_values(timesheet_sudo, next_id, pre_id, access_token, **kw)
        return request.render("de_portal_timesheet.portal_project_timesheet", values)

    @http.route(['/project/timesheet/print/<int:timesheet_id>'], type='http', auth="user", website=True)
    def portal_project_timesheet_print(self, timesheet_id, access_token=None, **kw):
        report_type = 'pdf'
        try:
            timesheet_sudo = self._document_check_access('hr.timesheet.report', timesheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=timesheet_sudo, report_type=report_type,
                                     report_ref='de_portal_timesheet.timehseet_attendance_report', download=True)




