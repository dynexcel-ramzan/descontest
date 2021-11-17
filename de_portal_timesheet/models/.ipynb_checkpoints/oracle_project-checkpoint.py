# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
# import cx_Oracle
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class ProjectProject(models.Model):
    _inherit = 'project.project'

    ora_project_id = fields.Integer(string='ORA Project id')

    def action_fetch_oracle_project(self):
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        statement = "select * from XX_APPS_IPL_PROJECTS where status='APPROVED' and enabled='Y'"
        cur.execute(statement)
        projects = cur.fetchall()
        # raise UserError(str(projects))
        for prj in projects:
            prj_value = {
                 'ora_project_id': prj[0],
                'name': prj[1]+' ('+str(prj[2])+') ',
            }
            project = self.env['project.project'].sudo().create(prj_value)
            client_value = {
                'name': prj[4] + ' (' + str(prj[3]) + ') ',
            }
            client = self.env['res.ora.client'].sudo().create(client_value)