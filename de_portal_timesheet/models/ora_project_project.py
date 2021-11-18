# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
# import cx_Oracle
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
# import cx_Oracle

class ORAProjectProject(models.Model):
    _name = 'ora.project.project'
    _description= 'ORA Project'
    
    name = fields.Char(string='Description', required=True)
    code = fields.Char(string='Code', required=True)
    client_id = fields.Many2one('res.ora.client', string='Client')
    ora_record_id = fields.Integer(string='Ora Record Id')

    def _action_fetch_oracle_project(self):
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        statement = "select p.id as id, p.code as code, p.descr as des, p.customer_name as cust_name, p.customer_number as cust_number  from XX_APPS_IPL_PROJECTS p where p.status='APPROVED' and p.enabled='Y' and p.customer_name is not null"
        cur.execute(statement)
        projects = cur.fetchall()
        for prj in projects:
            duplicate_rec = self.env['ora.project.project'].search([('ora_record_id','=',prj[0])])
            if not duplicate_rec:
                ora_clinet = self.env['res.ora.client'].search([('code','=',prj[4])])
                if not ora_clinet:
                    vals={
                        'name': prj[3],
                        'code': prj[4],
                    }
                    ora_clinet = self.env['res.ora.client'].create(vals)
                client_value = {
                    'name': prj[2],
                    'code':  prj[1],
                    'ora_record_id': prj[0],
                    'client_id': ora_clinet.id,
                }
                client = self.env['ora.project.project'].sudo().create(client_value)

