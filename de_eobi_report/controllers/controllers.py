# -*- coding: utf-8 -*-
# from odoo import http


# class DeEobiReport(http.Controller):
#     @http.route('/de_eobi_report/de_eobi_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_eobi_report/de_eobi_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_eobi_report.listing', {
#             'root': '/de_eobi_report/de_eobi_report',
#             'objects': http.request.env['de_eobi_report.de_eobi_report'].search([]),
#         })

#     @http.route('/de_eobi_report/de_eobi_report/objects/<model("de_eobi_report.de_eobi_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_eobi_report.object', {
#             'object': obj
#         })
