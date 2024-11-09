# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import fields, Command
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form
from odoo.exceptions import AccessError


class TestProjectExtension(TransactionCase):

    def setUp(self):
        super(TestProjectExtension, self).setUp()


        self.group_project_manager = self.env.ref('project.group_project_manager').id
        self.group_project_user = self.env.ref('project.group_project_user').id
        # Create a test user
        self.user_1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1',
            'groups_id': [Command.set([self.group_project_manager])],
        })

        # Create another test user
        self.user_2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2',
            'groups_id': [Command.set([self.group_project_user])],
        })

        self.user_3 = self.env['res.users'].create({
            'name': 'User 3',
            'login': 'user3',
            'groups_id': [Command.set([self.group_project_user])],
        })

        # Create a project team and add user_1 as a member
        self.team = self.env['project.team'].create({
            'name': 'Test Team',
            'member_ids': [(6, 0, [self.user_1.id, self.user_3.id])]
        })

        self.PROJECT = self.env['project.project']

        # Create a project and assign it to the team
        self.project = self.env['project.project'].with_user(self.user_1.id).create({
            'name': 'Test Project',
            'team_id': self.team.id,
            'privacy_visibility': 'followers',
        })

        # Create tasks for the project
        self.task_this_week = self.env['project.task'].create({
            'name': 'This Week Task',
            'project_id': self.project.id,
            'user_ids': [Command.link(self.user_1.id)],
            'date_deadline': fields.Date.today()
        })
        self.task_last_week = self.env['project.task'].create({
            'name': 'Last Week Task',
            'project_id': self.project.id,
            'user_ids': [Command.link(self.user_1.id)],
            'date_deadline': (fields.Date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        })

    def test_project_default_team_is_selected(self):
        project_1 = self.PROJECT.with_user(self.user_1.id).create({
            'name': 'Visibility Project'
        })
        self.assertEqual(project_1.team_id.id, self.team.id)


    def test_created_project_has_visibility_followers_by_default(self):
        visibility_project = self.PROJECT.create({
            'name': 'Visibility Project',
            'team_id': self.team.id,
        })
        self.assertEqual(visibility_project.privacy_visibility, 'followers')

    def test_project_visibility_can_not_be_changed_from_ui(self):
        visibility_project = self.PROJECT.create({
            'name': 'Visibility Project write',
            'team_id': self.team.id,
        })
        with self.assertRaises(AssertionError):
            project_form = Form(visibility_project, 'project.edit_project')
            project_form.privacy_visibility = 'employees'
            project = project_form.save()

        self.assertEqual(visibility_project.privacy_visibility, 'followers', "From ui, should not be changeable")

        visibility_project.with_user(self.user_1).write({'privacy_visibility': 'employees'})
        self.assertEqual(visibility_project.privacy_visibility, 'employees', "From backend, should be changeable")

    def test_team_membership(self):
        """Test that only team members can access the project."""
        # Check that user_1 (team member) can access the project
        project_accessible_user_1 = self.PROJECT.browse(self.project.id).with_user(self.user_1.id)
        self.assertTrue(project_accessible_user_1.read(), "Team member 1 should have access to the project.")

        project_accessible_by_user_3 = self.PROJECT.browse(self.project.id).with_user(self.user_3.id)
        self.assertTrue(project_accessible_by_user_3.read(), "Team members 3 should have access to the project.")

        project_accessible_by_user_2 = self.PROJECT.browse(self.project.id).with_user(self.user_2.id)
        with self.assertRaises(AccessError, msg="%s should not be able to read the project" % self.user_2.name):
            project_accessible_by_user_2.read()
