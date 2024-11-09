from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _get_user_ids_domain(self):
        domain = [('share', '=', False), ('active', '=', True)]
        if not self.env.is_admin() and not self.env.is_system() and not self.env.user.has_group('project.group_project_manager'):
            if self.team_id:
                domain += [('id', 'in', self.team_id.member_ids.ids)]
            elif self.project_id and self.project_id.team_id:
                domain += [('id', 'in', self.project_id.team_id.member_ids.ids)]
            else:
                domain += [('id', 'in', [self.env.user.id])]
        return domain

    team_id = fields.Many2one(related="project_id.team_id")
    user_ids = fields.Many2many(domain=lambda self: self._get_user_ids_domain())