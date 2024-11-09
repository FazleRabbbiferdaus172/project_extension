# -*- coding: utf-8 -*-

from odoo import fields, models, api, tools


class TaskAssigneeProjectReport(models.Model):
    _name = "task.assignee.project.report"
    _auto = False

    # name = fields.Char()
    task_id = fields.Many2one('project.task', string='Task', readonly=True)
    assignee_id = fields.Many2one('res.users', string='Assignee', readonly=True)
    team_id = fields.Many2one('project.team', string='Team', readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True)
    is_closed = fields.Boolean("Closing Stage", readonly=True)
    date_end = fields.Datetime(string='Ending Date', readonly=True)
    create_date = fields.Datetime(string='Creation Date', readonly=True)

    def _query(self):
        _query = """
        SELECT
            pt.id as id,
            pt.id as task_id,
            pt.is_closed as is_closed,
            pt.date_end as date_end,
            pt.create_date as create_date,
            task_user.id as assignee_id,
            ptut.id as team_id,
            pp.id as project_id
        FROM
            project_task AS pt
        LEFT JOIN
            project_project AS pp ON pt.project_id = pp.id
        JOIN
            project_task_user_rel AS ptu_rel on ptu_rel.task_id = pt.id
        JOIN
            res_users AS task_user on ptu_rel.user_id = task_user.id
        LEFT JOIN project_team_res_users_rel AS team_user_rel ON team_user_rel.res_users_id = task_user.id
        LEFT JOIN project_team AS ptut on team_user_rel.project_team_id = ptut.id
        """
        return _query

    @property
    def _table_query(self):
        return self._query()

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))