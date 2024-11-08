# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import fields, Command
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form


class TestProjectExtension(TransactionCase):

    def setUp(self):
        super(TestProjectExtension, self).setUp()

        # Create a test user
        self.user_1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1',
        })

        # Create another test user
        self.user_2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2',
        })

        # Create a project team and add user_1 as a member
        self.team = self.env['project.team'].create({
            'name': 'Test Team',
            'member_ids': [(6, 0, [self.user_1.id])]
        })

        # Create a project and assign it to the team
        self.project = self.env['project.project'].create({
            'name': 'Test Project',
            'team_id': self.team.id
        })

        # Create tasks for the project
        self.task_this_week = self.env['project.task'].create({
            'name': 'This Week Task',
            'project_id': self.project.id,
            'user_id': self.user_1.id,
            'date_deadline': fields.Date.today()
        })
        self.task_last_week = self.env['project.task'].create({
            'name': 'Last Week Task',
            'project_id': self.project.id,
            'user_id': self.user_1.id,
            'date_deadline': (fields.Date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        })

    def test_team_membership(self):
        """Test that only team members can access the project."""
        # Check that user_1 (team member) can access the project
        project_accessible = self.project.with_user(self.user_1.id).exists()
        self.assertTrue(project_accessible, "Team member should have access to the project.")

        # Check that user_2 (not a team member) cannot access the project
        project_accessible = self.project.with_user(self.user_2.id).exists()
        self.assertFalse(project_accessible, "Non-team member should not have access to the project.")

    def test_dashboard_task_count(self):
        """Test the task count filters on the dashboard."""

        # Get task counts by different filters
        tasks_this_week = self.env['project.task'].search_count([
            ('project_id', '=', self.project.id),
            ('date_deadline', '>=', fields.Date.today())
        ])

        tasks_last_week = self.env['project.task'].search_count([
            ('project_id', '=', self.project.id),
            ('date_deadline', '>=', (fields.Date.today() - timedelta(days=7)).strftime('%Y-%m-%d')),
            ('date_deadline', '<', fields.Date.today())
        ])

        # Check if the filters return correct counts
        self.assertEqual(tasks_this_week, 1, "There should be 1 task for this week.")
        self.assertEqual(tasks_last_week, 1, "There should be 1 task for last week.")

    def test_assignee_filter(self):
        """Test task filtering by assignee in the dashboard."""
        # Filter tasks assigned to user_1
        tasks_for_user_1 = self.env['project.task'].search_count([
            ('user_id', '=', self.user_1.id),
            ('project_id', '=', self.project.id)
        ])

        # Check if the assignee filter returns correct count
        self.assertEqual(tasks_for_user_1, 2, "User 1 should have 2 tasks.")