# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectTeam(models.Model):
    _name = 'project.team'
    _description = 'Project Team'

    name = fields.Char("Team Name", required=True)
    member_ids = fields.Many2many('res.users', string="Team Members")
    project_ids = fields.One2many('project.project', 'team_id', string="Projects")