from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    team_id = fields.Many2one('project.team', string="Project Team")
    privacy_visibility = fields.Selection(default='followers', readonly=True)