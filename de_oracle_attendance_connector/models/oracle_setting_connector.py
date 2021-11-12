# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError
import cx_Oracle
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)



class OracleSettingConnector(models.Model):
    _name = 'oracle.setting.connector'
    _description = 'Oracle Database Instance'
    _order = "name desc"

    name = fields.Char(string='Instance Name', required=True)
    host = fields.Char(string="Host", required=True)
    port = fields.Char(string="Port", required=True)
    user = fields.Char(string="User Name", required=True)
    password = fields.Char(string="Password", required=True)
    db_name = fields.Char(string="Oracle Database", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('close', 'Close')],
        readonly=False, string='State', index=True , default='draft')
    device_line_ids = fields.One2many('oracle.device.line', 'instance_id' ,string='Device Line', required=False) 
    attendance_count_lines = fields.One2many('oracle.attendance.count', 'instance_id' ,string='Count Line', required=False)
    count_date_from  = fields.Date(string='Count Date From')
    
    
    @api.onchange('count_date_from')
    def onchange_count_date(self):
        if  self.count_date_from:
            if self.count_date_from > fields.date.today():
                raise UserError('Not Allow to enter date greater than currenct date! '+str(fields.date.today()))
            
    def action_process_attendance_count(self):
        self.attendance_count_lines.unlink()
        if not self.count_date_from:
            raise UserError('Please select Count Date From inside Count Attendance tab!')
        delta_days = (fields.date.today() -  self.count_date_from).days 
        for att_line in range(delta_days):
            date_execution = fields.date.today() - timedelta(att_line)
            statement = """select count(*) from attend_data where atten_date=sysdate-"""+str(att_line)+""""""
            self.env.cr.execute(statement)
            date_execution_count = self.env.cr.fetchall()
            vals= {
                'date': date_execution,
                'ora_att_count': date_execution_count,
                'instance_id': self.id,
            }
            attendnace_count_line = self.env['oracle.attendance.count'].create(vals)
            
            

    def action_active(self):
        self.write({
            'state': 'active'
        })

    def try_connection(self):
        try:
            tusername = self.user
            tpasswrd = self.password
            thost = self.host
            tport = self.port
            tinstance = self.db_name
            conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.8.191:1521/PROD')
            cur = conn.cursor()
            if conn:
                self.write({
                    'state': 'active'
                })
            if conn:
                raise ValidationError('Successfully Connected')



        except Exception as e:
            raise ValidationError(e)


    def action_view_attendance_data(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.8.191:1521/PROD')
        cur = conn.cursor()
        statement = 'select count(*) from attend_data p where p.creation_date >= cast(getdate() as Date)'
        cur.execute(statement)
        attendances = cur.fetchall()
        raise UserError(str(attendances))


    def action_get_attendance_data(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.8.191:1521/PROD')
        cur = conn.cursor()
        statement = "select p.att_time AS timestamp, p.mac_number AS machine, p.card_no AS card, p.att_date AS attendance_date, p.creation_date AS creation_date, p.remarks AS remarks, p.updation_date AS updation_date from attend_data p where p.creation_date >=sysdate-1 and p.mac_number not in (48,49)"
        cur.execute(statement)
        attendances = cur.fetchall()  
        for attendance in attendances:
            ebs_timestamp1 = attendance[6].strftime("%Y-%m-%d %H:%M:%S")
            ebs_timestamp = datetime.strptime(ebs_timestamp1, '%Y-%m-%d %H:%M:%S') - relativedelta(hours =+ 5)
            ebs_attendance_data1 =  ebs_timestamp.strftime('%Y-%m-%d')
            ebs_attendance_data = datetime.strptime(ebs_attendance_data1, '%Y-%m-%d')
            duplicate_attendance = user_attendance.search([('card_no','=',attendance[2]),('time','=',attendance[0]),('attendance_date','=',ebs_attendance_data)], limit=1)
            if not duplicate_attendance:
                
                employee = self.env['hr.employee'].search([('barcode','=',attendance[2])], limit=1)
                timestamdata = attendance[6]
                timestamp1 = timestamdata.strftime("%Y-%m-%d %H:%M:%S")
                timestamp = datetime.strptime(timestamp1, '%Y-%m-%d %H:%M:%S') - relativedelta(hours =+ 5)
                attendance_data1 =  attendance[3]
                attendance_data = datetime.strptime(timestamp1, '%Y-%m-%d %H:%M:%S')
                timedata = attendance[0]
                time = timedata
                vals = {
                 'timestamp': timestamp,
                 'device_id': attendance[1],
                 'employee_id': employee.id,
                 'card_no': attendance[2],
                 'attendance_date': attendance_data,
                 'creation_date': attendance[4],
                 'company_id': employee.company_id.id,
                 'remarks': attendance[5],
                 'time':  attendance[0],
                 'updation_date': attendance[6],
                 }
                user_attendance= self.env['hr.user.attendance'].create(vals)

        


class OracleSettingConnectorLine(models.Model):
    _name = 'oracle.device.line'
    _description = 'Oracle Attendance Device'
    _order = "device_id desc"
    _rec_name='device_id'

    device_id = fields.Many2one('hr.device.attendance',string='Device', required=True)
    mode = fields.Selection([('check_in', 'Check In'), 
                             ('check_out', 'Check Out'),
                             ('both', 'Both'),
                            ], string="Device Mode", required=True)
    company_id = fields.Many2one('res.company',string='Company', required=False)
    instance_id = fields.Many2one('oracle.setting.connector',string='Connector', required=False)

    
class AttendanceLine(models.Model):
    _name = 'oracle.attendance.count'
    _description = 'Oracle Attendance Count'
    _order = "date desc"
    _rec_name='date'

    date = fields.Date(string='Date')
    ora_att_count = fields.Char(string='Attendance Count')
    instance_id = fields.Many2one('oracle.setting.connector',string='Connector', required=False)
    




