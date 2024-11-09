from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def _default_team_id(self):
        team_id = self.env['project.team'].search([('member_ids', 'in', [self.env.user.id])], limit=1)
        return team_id.id if team_id else False

    def _get_team_domain(self):
        domain = []
        if not self.env.is_admin() and not self.env.is_system() and not self.env.user.has_group('project.group_project_manager'):
            domain = [('member_ids', 'in', [self.env.user.id])]
        return domain

    team_id = fields.Many2one('project.team', string="Assigned Team", required=True, default=_default_team_id,
                              domain=lambda self: self._get_team_domain())
    privacy_visibility = fields.Selection(default='followers', readonly=True)


    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)
        for project in projects:
            team_members_partner_id = project.team_id.member_ids.mapped('partner_id.id')
            project.message_subscribe(
                partner_ids=team_members_partner_id
            )
        return projects

    def write(self, vals):
        res = super(Project, self).write(vals)
        if vals.get('team_id'):
            partners_present = self.message_partner_ids.ids
            self.message_unsubscribe(partner_ids=partners_present)
            team_members_partner_id = self.team_id.member_ids.mapped('partner_id.id')
            self.message_subscribe(
                partner_ids=team_members_partner_id
            )
        return res