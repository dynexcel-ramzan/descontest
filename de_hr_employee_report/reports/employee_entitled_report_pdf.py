# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date


class EmployeeEntitledPDF(models.AbstractModel):
    _name = 'report.de_hr_employee_report.employee_entitled_pdf'
    _description = 'Employee OT Entitled PDF Report'

    def _get_report_values(self, docids, data):
        
        type_employee = self.env['employee.type'].search([('id', 'in', data['employee_type_ids'])])
        employee_type = []
        for rec in type_employee:
            employee_type.append(rec.name)
        
        em_type = ','.join(employee_type)
        grade_type = self.env['grade.type'].search([('id', 'in', data['grade_type_ids'])])
        g_type = []
        for rec in grade_type:
            g_type.append(rec.name)

        gr_type = ','.join(g_type)
        
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
        
        company_ids = self.env['res.company'].search([('id', 'in', data['company_ids'])])
        companyids = []
        for rec in company_ids:
            companyids.append(rec.name)
        company = ','.join(companyids)
        
        employees = []
        if employee_type and departments and locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
        
        
        elif employee_type and departments and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
        elif employee_type and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
        elif employee_type and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
        elif employee_type and departments and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
        elif employee_type and departments and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif employee_type and locations and g_type and companyids:
            
            active_contract = self.env['hr.contract'].search([('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
        
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
        elif departments and locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif departments and locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif departments and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.department_id', 'in',departments),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif locations and g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif employee_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif locations and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        
        elif departments and companyids:
            
            active_contract = self.env['hr.contract'].search([('employee_id.department_id', 'in',departments),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
                    
                    
        elif g_type and companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.grade_type', 'in', g_type),
                                                              ('employee_id.company_id', 'in', companyids)
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
        
        elif employee_type:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.emp_type', 'in', employee_type)
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
        
        elif locations:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.work_location_id', 'in',locations)
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
        
        elif departments:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.department_id', 'in',departments)
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
        
        elif companyids:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.company_id', 'in', companyids)
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
        
        elif g_type:
            active_contract = self.env['hr.contract'].search([
                                                              ('employee_id.grade_type', 'in', g_type)
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
        
        else:
            active_contract = self.env['hr.contract'].search([
                                                              ('state', '=', 'open')
                                                              
                                                              ])
            for contract in active_contract:
                ot_entitled = contract.employee_id.allow_overtime
                #raise UserError(ot_entitled)
                if ot_entitled == True:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'Y'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    employees.append(employee_dict)
                
                elif ot_entitled == False:
                    emp_code = contract.employee_id.emp_number
                    name = contract.employee_id.name
                    dep_name = contract.employee_id.department_id.name
                    emp_type = contract.employee_id.emp_type
                    g_type = contract.employee_id.grade_type.name
                    ot_entitled = 'N'
                    location = contract.employee_id.work_location_id.name
                    
                    employee_dict = {}
                    employee_dict['emp_code'] = emp_code
                    employee_dict['name'] = name
                    employee_dict['dep_name'] = dep_name
                    employee_dict['emp_type'] = emp_type
                    employee_dict['g_type'] = g_type
                    employee_dict['ot_entitled'] = ot_entitled
                    employee_dict['location'] = location
                    employee_dict['employee_status'] = 'On Roll'
                    
                    
                    employees.append(employee_dict)
        
        
                    
        
        #raise UserError(active_contract.ids)
        #raise UserError(len(employees))
        
            
                    
        return {
            'doc_ids': self.ids,
            'doc_model': 'employee.entitled',
            'data': data,
            'employee_type': em_type,
            'location':loc,
            'grade_type': gr_type,
            'department': dep,
            'company_name':company,
            'active_contract': active_contract,
            'employees':employees,
        }
