# -*- coding: utf-8 -*-
# from odoo import http


# class DeLongServiceAward(http.Controller):
#     @http.route('/de_long_service_award/de_long_service_award/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_long_service_award/de_long_service_award/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_long_service_award.listing', {
#             'root': '/de_long_service_award/de_long_service_award',
#             'objects': http.request.env['de_long_service_award.de_long_service_award'].search([]),
#         })

#     @http.route('/de_long_service_award/de_long_service_award/objects/<model("de_long_service_award.de_long_service_award"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_long_service_award.object', {
#             'object': obj
#         })
