# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectTeam(models.Model):
    _name = 'project.team'
    _description = 'Project Team'

    name = fields.Char("Team Name", required=True)
    member_ids = fields.Many2many('res.users', string="Team Members", required=True)
    project_ids = fields.One2many('project.project', 'team_id', string="Projects")

    def write(self, vals):
        res = super(ProjectTeam, self).write(vals)
        if vals.get('member_ids'):
            team_members_partner_id = self.member_ids.mapped('partner_id.id')
            for project in self.project_ids:
                partners_present = project.message_partner_ids.ids
                project.message_unsubscribe(partner_ids=partners_present)
                project.message_subscribe(
                    partner_ids=team_members_partner_id
                )
        return res