# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date, datetime, timedelta
from itertools import groupby


class EmployeeRetirementPDF(models.AbstractModel):
    _name = 'report.de_hr_employee_report.employee_retirement_pdf'
    _description = 'Employee Retirement PDF Report'

    def _get_report_values(self, docids, data):
        type_employee = self.env['employee.type'].search([('id', 'in', data['employee_type_ids'])])
        employee_type = []
        for rec in type_employee:
            employee_type.append(rec.name)
        #raise UserError(employee_type)
        em_type = ','.join(employee_type)
        department = self.env['hr.department'].search([('id', 'in', data['department_ids'])])
        departments = []
        for rec in department:
            departments.append(rec.name)
        
        #raise UserError(departments)
        dep = ','.join(departments)
        
        location = self.env['hr.work.location'].search([('id', 'in', data['location_ids'])])
        locations = []
        for rec in location:
            locations.append(rec.name)
        loc = ','.join(locations)
        
        grade_type = self.env['grade.type'].search([('id', 'in', data['grade_type_ids'])])
        g_type = []
        for rec in grade_type:
            g_type.append(rec.name)

        gr_type = ','.join(g_type)
        
        company_ids = self.env['res.company'].search([('id', 'in', data['company_ids'])])
        companyids = []
        for rec in company_ids:
            companyids.append(rec.name)
        company = ','.join(companyids)
        #raise UserError(company)
        
        employees = []
        if employee_type and departments and locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        
        elif employee_type and departments and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif employee_type and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif employee_type and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                            ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif employee_type and departments and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif employee_type and departments and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif employee_type and locations and g_type and companyids:
            
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif departments and locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                            ('employee_id.grade_type', 'in', g_type),

                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif departments and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif departments and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif employee_type:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type)
                                                              
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif employee_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif locations:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations)
                                                              
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        
                
        
        elif departments and companyids:
            
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif departments:
            active_contract = self.env['hr.contract'].search([
                                                            ('employee_id.department_id', 'in',departments)
                                                              
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        elif g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                            ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif g_type:
            active_contract = self.env['hr.contract'].search([
                                                            ('employee_id.grade_type', 'in', g_type)
                                                              
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        elif companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                year = contract.employee_id.birthday.year
                year = year + 60
                month = contract.employee_id.birthday.month
                date = contract.employee_id.birthday.day
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
        
        else:
            active_contract = self.env['hr.contract'].search([
                                                              ('state', '=', 'open')
                                                              ])
            for contract in active_contract:
                emp_code = contract.employee_id.emp_number
                name = contract.employee_id.name
                dep_name = contract.employee_id.department_id.name
                emp_type = contract.employee_id.emp_type
                g_type = contract.employee_id.grade_type.name
                doj = contract.employee_id.date
                retirement_age = contract.company_id.retirement_age
                if contract.employee_id.birthday:
                    year = contract.employee_id.birthday.year
                    year = year + 60
                    month = contract.employee_id.birthday.month
                    date = contract.employee_id.birthday.day
                else:
                    year = None
                    month = None
                    date = None
                retirement_date = str(year) + '/' + str(month) + '/' + str(date)
                #company = contract.company_id.name
                

                employee_dict = {}
                employee_dict['emp_code'] = emp_code
                employee_dict['name'] = name
                employee_dict['dep_name'] = dep_name
                employee_dict['emp_type'] = emp_type
                employee_dict['g_type'] = g_type
                employee_dict['doj'] = doj
                employee_dict['retirement_age'] = retirement_age
                employee_dict['retirement_date'] = retirement_date
                #employee_dict['company'] = company
                

                employees.append(employee_dict)
                
        #raise UserError(active_contract.ids)
        #raise UserError(employees.ids)
            
        return {
            'doc_ids': self.ids,
            'doc_model': 'employee.retirement',
            'data': data,
            'location': loc,
            'employee_type': em_type,
            'department': dep,
            'grade_type': gr_type,
            'active_contract': active_contract,
            'company_name':company,
            'start_date':data['start_date'],
            'end_date':data['end_date'],
            'employees':employees
        }
