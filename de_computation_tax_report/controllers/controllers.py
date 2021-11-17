# -*- coding: utf-8 -*-
# from odoo import http


# class DeComputationTaxReport(http.Controller):
#     @http.route('/de_computation_tax_report/de_computation_tax_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_computation_tax_report/de_computation_tax_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_computation_tax_report.listing', {
#             'root': '/de_computation_tax_report/de_computation_tax_report',
#             'objects': http.request.env['de_computation_tax_report.de_computation_tax_report'].search([]),
#         })

#     @http.route('/de_computation_tax_report/de_computation_tax_report/objects/<model("de_computation_tax_report.de_computation_tax_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_computation_tax_report.object', {
#             'object': obj
#         })
