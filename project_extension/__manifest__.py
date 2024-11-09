# -*- coding: utf-8 -*-
{
    'name': "Project Extension",

    'summary': """
        Project Extension with features for assigning teams to a project.
        """,

    'description': """
        Project Extension with features for assigning teams to a project.
            Features:
                - Create Teams.
                - Assign teams to projects.
                - Dashboard.
                
        Feature description:
            1. Team can be created by project managers from the menu "root > Project > Teams. Members can be added to the team from form view.
            2. Projects are only visible to the "projects users" that are part of the assigned team of that project. 
            3. Project manages are considered admin of project module and has access to all project regardless. 
            2. Dashboard is accessible "Root > Dashboard > Project"
            3. Dashboard shows 2 tables 
                - Project task count table: open tasks count of each project and assigned team
                - Assignee task table: Assigned task of each user
            4. Dashboard has 2 filters that takes effect on the 2nd table
                - Period filter can be used to view task for each period of last 7, 30, 90, 185, 365 days and last 3 years.
                - Assignee filter can be used to view task for each assigned project and assigned team
    """,

    'author': "Fazle Rabbi Ferdaus",

    'category': 'Uncategorized',
    'version': '0.0.1',

    'depends': ['project', 'spreadsheet_dashboard'],
    'installable': True,
    'application': True,
    # always loaded
    'data': [
        "data/dashboard.xml",
        'security/ir.model.access.csv',
        'views/views_project.xml',
        'report/task_assignee_project_report_view.xml'
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
