# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import cx_Oracle

class HrUserAttendance(models.Model):
    _name = 'hr.user.attendance'
    _description = 'This is User Attendance'
    
    

    employee_id = fields.Many2one('hr.employee', string="Employee")
    is_mapped = fields.Boolean(string="Mapped Employee")
    company_id = fields.Many2one('res.company', string="Company")
    timestamp = fields.Datetime(string='Timestamp')
    device_id = fields.Char(string='Device ID')
    card_no = fields.Char(string="Card NO.")
    time = fields.Char(string="Stamp Time")
    attendance_date = fields.Date(string='Attendance Date')
    creation_date = fields.Char(string='Attendance Date')
    remarks = fields.Char(string='Remarks')
    updation_date = fields.Char(string='Updation Date')
    is_attedance_created = fields.Boolean(string="Attendance Posted")

    
    def action_attendace_validated(self, employeeslst, deltadays):        
        month_datetime = fields.date.today() - timedelta(deltadays)
        for month_date in range(deltadays):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('id', 'in', employeeslst)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    
    


    
    def action_view_attendance_data(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.8.191:1521/PROD')
        cur = conn.cursor()
        statement = """SELECT A.COMPANY_ID,
         A.OFFICE_EMP_ID,
         A.EMPLOYEE_ID,
         A.NAME,
         A.ATT_PERIOD,
         A.PERIOD_DATE,
         A.ATT_DATE,
         A.ATT_SHORT_DAY,
         A.IN_TIME,
         A.OUT_TIME,
         A.WORKED_HOURS,
         A.SHIFT_NAME,
         A.SHIFT_REST_DAY,
         A.SHIFT_START_TIME,
         A.SHIFT_END_TIME,
            A.PAYROLL_REMARKS
         || CASE
               WHEN (SELECT COUNT (COMM.APPLICANT_ID)
                       FROM XXHR.HR_COMMITMENT_SLIP_HEADER COMM
                      WHERE     COMM.APPLICANT_ID = A.EMPLOYEE_ID
                            AND COMM.CMTMT_TYPE = 'M'
                            AND A.ATT_DATE BETWEEN COMM.CMTMT_DATE
                                               AND COMM.CMTMT_DATE_TO) > 0
               THEN
                  '(F)'
               WHEN (SELECT COUNT (COMM.APPLICANT_ID)
                       FROM XXHR.HR_COMMITMENT_SLIP_HEADER COMM
                      WHERE     COMM.APPLICANT_ID = A.EMPLOYEE_ID
                            AND COMM.CMTMT_TYPE = 'S'
                            AND A.ATT_DATE = COMM.CMTMT_DATE) > 0
               THEN
                     '('
                  || TO_CHAR (
                        (SELECT COUNT (COMM.APPLICANT_ID)
                           FROM XXHR.HR_COMMITMENT_SLIP_HEADER COMM
                          WHERE     COMM.APPLICANT_ID = A.EMPLOYEE_ID
                                AND COMM.CMTMT_TYPE = 'S'
                                AND A.ATT_DATE = COMM.CMTMT_DATE))
                  || ' P)'
            END
            PAYROLL_REMARKS,
         A.TERMINAL,
         A.PAY_REM_TRIM
    FROM (SELECT e.company_id,
                 E.office_emp_id,
                 E.EMPLOYEE_ID,
                 E.name,
                 E.att_period,
                 TO_DATE ('01-' || E.att_period, 'DD-MON-RR') Period_date,
                 E.att_date,
                 E.att_short_day,
                 CASE
                    WHEN L.TIMEBASED_ATTENDANCE = 'Y'
                    THEN
                       CASE
                          WHEN E.ATT_DATE < L.TIMEBASED_ATTEND_DATE
                          THEN
                             TO_CHAR (E.in_time, 'HH24:MI:SS')
                          ELSE
                             TO_CHAR (E.in_time, 'DD-Mon-RR HH24:MI:SS')
                       END
                    ELSE
                       TO_CHAR (E.in_time, 'HH24:MI:SS')
                 END
                    in_time,
                 CASE
                    WHEN L.TIMEBASED_ATTENDANCE = 'Y'
                    THEN
                       CASE
                          WHEN E.ATT_DATE < L.TIMEBASED_ATTEND_DATE
                          THEN
                             TO_CHAR (E.out_time, 'HH24:MI:SS')
                          ELSE
                             TO_CHAR (E.out_time, 'DD-Mon-RR HH24:MI:SS')
                       END
                    ELSE
                       TO_CHAR (E.out_time, 'HH24:MI:SS')
                 END
                    out_time,
                 E.worked_hours,
                 E.shift_name,
                 E.shift_rest_day,
                 E.shift_start_time,
                 E.shift_end_time,
                 CASE
                    WHEN L.ATTENDANCE_POLICY = 'Y'
                    THEN
                       CASE
                          WHEN E.ATT_DATE < L.ATTENDANCE_POLICY_DATE
                          THEN
                             E.CONCLUSION
                          ELSE
                             E.payroll_remarks
                       END
                    ELSE
                       E.CONCLUSION
                 END
                    PAYROLL_REMARKS,
                 CASE
                    WHEN NVL (INSTR (e.machine_ip, ','), 0) = 0
                    THEN
                       (SELECT remarks
                          FROM machine_ip
                         WHERE ip_address = e.machine_ip)
                    ELSE
                          (SELECT remarks
                             FROM machine_ip
                            WHERE ip_address =
                                     SUBSTR (e.machine_ip,
                                             1,
                                             INSTR (e.machine_ip, ',') - 1))
                       || '/'
                       || (SELECT remarks
                             FROM machine_ip
                            WHERE ip_address =
                                     SUBSTR (e.machine_ip,
                                             INSTR (e.machine_ip, ',') + 2))
                 END
                    terminal,
                 LTRIM (RTRIM (E.payroll_remarks)) pay_rem_trim
            FROM xxhr.attendance_v E, xxhr.location l
           WHERE     e.company_id = :p_company_id
                 AND E.ATT_DATE BETWEEN :P_START_DATE AND :P_END_DATE
                 AND e.company_id = l.company_id
                 AND e.location_id = l.location_id --AND E.MACHINE_IP = I.IP_ADDRESS(+)
                                                  --&V_AND
         ) A
ORDER BY A.office_emp_id, A.att_date"""
        cur.execute(statement)
        attendances = cur.fetchall()
        raise UserError(str(attendances))


    def action_view_attendance_data_record(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.8.191:1521/PROD')
        cur = conn.cursor()
        statement = "select * from attend_data where att_date='08/04/2021'"
        cur.execute(statement)
        attendances = cur.fetchone()
        raise UserError(str(attendances))
    
      

    def action_attendace_validated_dcl(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',1)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    
    #   Rousch Pakistan Power Limited
    
   
    def action_attendace_validated_rousch(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',6)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })

                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
                                    
                                    
    
    #   Inspectest (Pvt) Limited
    
    
    def action_attendace_validated_ipl(self):        
        month_datetime = fields.date.today() - timedelta(3)
        for month_date in range(4):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',5)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)
    
    
    
    
    
        #   Gray Mackenzie Engineering Services W.L.L

    
    
    def action_attendace_validated_dmesw(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',7)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })

                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })

                                    
                                    
        #   Gray Mackenzie Engineering Services LLC

    
    
    def action_attendace_validated_gmesl(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',4)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)                                    
    
    
    
    
        #   Descon Technical Institute

    
    
    def action_attendace_validated_dti(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',8)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })

                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)
    
    
    
        #   Descon Power Solutions (Private) Limited

    
    
    def action_attendace_validated_dps(self):        
        month_datetime = fields.date.today() - timedelta(1)
        for month_date in range(2):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',3)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })

                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)
    
    
    
        #   Descon Oxychem Limited
    
    
    def action_attendace_validated_dol(self):        
        month_datetime = fields.date.today() - timedelta(4)
        for month_date in range(5):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',2)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)
    
    
    
        #   Altern Energy Limited

    
    
    def action_attendace_validated_ael(self):        
        month_datetime = fields.date.today() - timedelta(10)
        for month_date in range(11):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('company_id','=',9)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            attendance_list_in.update({
                                        'is_attedance_created' : True
                                        })
                   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    #                                 attendance.action_process_attendance(attendance.id)