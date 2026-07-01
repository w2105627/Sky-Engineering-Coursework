

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=255)),
                ('user_password', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('employee_email', models.CharField(max_length=255, unique=True)),
                ('employee_role', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Employee',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_description', models.CharField(max_length=255)),
                ('skill_name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'Skill',
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('audit_log_id', models.AutoField(primary_key=True, serialize=False)),
                ('audit_timestamp', models.DateTimeField()),
                ('audit_details', models.CharField(max_length=255)),
                ('action_type', models.CharField(blank=True, max_length=255, null=True)),
                ('entity_id', models.IntegerField(blank=True, null=True)),
                ('entity_type', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='core.appuser')),
            ],
            options={
                'db_table': 'AuditLog',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=255)),
                ('department_head', models.ForeignKey(blank=True, db_column='department_head_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_departments', to='core.employee')),
            ],
            options={
                'db_table': 'Department',
            },
        ),
        migrations.AddField(
            model_name='appuser',
            name='employee',
            field=models.OneToOneField(blank=True, db_column='employee_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_user', to='core.employee'),
        ),
        migrations.CreateModel(
            name='MeetingInstance',
            fields=[
                ('meeting_id', models.AutoField(primary_key=True, serialize=False)),
                ('meeting_date', models.DateTimeField()),
                ('meeting_description', models.CharField(max_length=255)),
                ('created_by_user', models.ForeignKey(db_column='created_by_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='created_meetings', to='core.appuser')),
            ],
            options={
                'db_table': 'MeetingInstance',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('disbanded_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('development_focus', models.CharField(blank=True, max_length=255, null=True)),
                ('software_owned', models.CharField(blank=True, max_length=255, null=True)),
                ('concurrent_projects', models.IntegerField(blank=True, null=True)),
                ('team_wiki', models.CharField(blank=True, max_length=255, null=True)),
                ('workstream', models.CharField(blank=True, max_length=255, null=True)),
                ('standup_time', models.DateTimeField(blank=True, null=True)),
                ('department', models.ForeignKey(db_column='department_id', on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='core.department')),
                ('team_leader', models.ForeignKey(blank=True, db_column='team_leader_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_teams', to='core.employee')),
            ],
            options={
                'db_table': 'Team',
            },
        ),
        migrations.CreateModel(
            name='MeetingTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(db_column='meeting_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_links', to='core.meetinginstance')),
                ('team', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='meeting_links', to='core.team')),
            ],
            options={
                'db_table': 'MeetingTeam',
            },
        ),
        migrations.AddField(
            model_name='meetinginstance',
            name='teams',
            field=models.ManyToManyField(related_name='meetings', through='core.MeetingTeam', to='core.team'),
        ),
        migrations.CreateModel(
            name='Dependencies',
            fields=[
                ('dependency_id', models.AutoField(primary_key=True, serialize=False)),
                ('dependency_type', models.CharField(max_length=255)),
                ('downstream_team', models.ForeignKey(db_column='downstream_team_id', on_delete=django.db.models.deletion.CASCADE, related_name='downstream_dependencies', to='core.team')),
                ('upstream_team', models.ForeignKey(db_column='upstream_team_id', on_delete=django.db.models.deletion.CASCADE, related_name='upstream_dependencies', to='core.team')),
            ],
            options={
                'db_table': 'Dependencies',
            },
        ),
        migrations.CreateModel(
            name='TeamContact',
            fields=[
                ('team_contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_email', models.CharField(blank=True, max_length=255, null=True)),
                ('slack_channel', models.CharField(blank=True, max_length=255, null=True)),
                ('team_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('team', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='core.team')),
            ],
            options={
                'db_table': 'TeamContact',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_join_date', models.DateTimeField()),
                ('left_team_date', models.DateTimeField(blank=True, null=True)),
                ('team_role', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(db_column='employee_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.employee')),
                ('team', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.team')),
            ],
            options={
                'db_table': 'TeamMember',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', through='core.TeamMember', to='core.employee'),
        ),
        migrations.CreateModel(
            name='TeamRepo',
            fields=[
                ('repo_id', models.AutoField(primary_key=True, serialize=False)),
                ('codebase_link', models.CharField(blank=True, max_length=255, null=True)),
                ('versioning_approach', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('jira_board_link', models.CharField(blank=True, max_length=255, null=True)),
                ('jira_project_name', models.CharField(blank=True, max_length=255, null=True)),
                ('agile_practices', models.CharField(blank=True, max_length=255, null=True)),
                ('team', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='core.team')),
            ],
            options={
                'db_table': 'TeamRepo',
            },
        ),
        migrations.CreateModel(
            name='TeamSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(db_column='skill_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_skill_links', to='core.skill')),
                ('team', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_skill_links', to='core.team')),
            ],
            options={
                'db_table': 'TeamSkill',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='skills',
            field=models.ManyToManyField(related_name='teams', through='core.TeamSkill', to='core.skill'),
        ),
        migrations.AddConstraint(
            model_name='meetingteam',
            constraint=models.UniqueConstraint(fields=('team', 'meeting'), name='unique_team_meeting'),
        ),
        migrations.AddConstraint(
            model_name='dependencies',
            constraint=models.CheckConstraint(condition=models.Q(('downstream_team', models.F('upstream_team')), _negated=True), name='dependencies_not_self'),
        ),
        migrations.AddConstraint(
            model_name='dependencies',
            constraint=models.UniqueConstraint(fields=('downstream_team', 'upstream_team', 'dependency_type'), name='unique_team_dependency_type'),
        ),
        migrations.AddConstraint(
            model_name='teammember',
            constraint=models.UniqueConstraint(fields=('employee', 'team'), name='unique_employee_team_membership'),
        ),
        migrations.AddConstraint(
            model_name='teamskill',
            constraint=models.UniqueConstraint(fields=('team', 'skill'), name='unique_team_skill'),
        ),
    ]
