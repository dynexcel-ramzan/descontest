# -*- coding: utf-8 -*-
# from odoo import http


# class DeTaxCreditForm(http.Controller):
#     @http.route('/de_tax_credit_form/de_tax_credit_form/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_tax_credit_form/de_tax_credit_form/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_tax_credit_form.listing', {
#             'root': '/de_tax_credit_form/de_tax_credit_form',
#             'objects': http.request.env['de_tax_credit_form.de_tax_credit_form'].search([]),
#         })

#     @http.route('/de_tax_credit_form/de_tax_credit_form/objects/<model("de_tax_credit_form.de_tax_credit_form"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_tax_credit_form.object', {
#             'object': obj
#         })
