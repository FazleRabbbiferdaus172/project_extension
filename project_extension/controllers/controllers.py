# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectExtension(http.Controller):
#     @http.route('/project_extension/project_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_extension/project_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_extension.listing', {
#             'root': '/project_extension/project_extension',
#             'objects': http.request.env['project_extension.project_extension'].search([]),
#         })

#     @http.route('/project_extension/project_extension/objects/<model("project_extension.project_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_extension.object', {
#             'object': obj
#         })
