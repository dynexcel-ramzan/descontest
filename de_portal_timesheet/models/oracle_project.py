# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import cx_Oracle
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def action_fetch_oracle_project(self):
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.7.152:1523/test2')
        cur = conn.cursor()
        statement = "select * from XX_APPS_IPL_PROJECTS"
        cur.execute(statement)
        projects = cur.fetchall()
        raise UserError(str(projects))

