# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_overtime_location_report(models.Model):
#     _name = 'de_overtime_location_report.de_overtime_location_report'
#     _description = 'de_overtime_location_report.de_overtime_location_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
