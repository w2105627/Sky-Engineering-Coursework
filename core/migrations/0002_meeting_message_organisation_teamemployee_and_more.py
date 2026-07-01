
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('meeting_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('meeting_date', models.DateTimeField()),
                ('meeting_description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Meeting',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.CharField(max_length=255)),
                ('message_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Sent', 'Sent'), ('Draft', 'Draft'), ('Read', 'Read')], default='Sent', max_length=30)),
            ],
            options={
                'db_table': 'Message',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('organisation_id', models.AutoField(primary_key=True, serialize=False)),
                ('organisation_name', models.CharField(max_length=255, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Organisation',
            },
        ),
        migrations.CreateModel(
            name='TeamEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_join_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('left_team_date', models.DateTimeField(blank=True, null=True)),
                ('team_role', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'TeamEmployee',
            },
        ),
        migrations.RenameModel(
            old_name='Dependencies',
            new_name='Dependency',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='meetinginstance',
            name='created_by_user',
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='meetinginstance',
            name='teams',
        ),
        migrations.RemoveConstraint(
            model_name='meetingteam',
            name='unique_team_meeting',
        ),
        migrations.RemoveConstraint(
            model_name='teammember',
            name='unique_employee_team_membership',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='development_focus',
            new_name='responsibilities',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='software_owned',
            new_name='team_description',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='team_wiki',
            new_name='team_mission',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='employee_role',
        ),
        migrations.RemoveField(
            model_name='team',
            name='concurrent_projects',
        ),
        migrations.RemoveField(
            model_name='team',
            name='standup_time',
        ),
        migrations.RemoveField(
            model_name='team',
            name='workstream',
        ),
        migrations.RemoveField(
            model_name='teamcontact',
            name='team_phone',
        ),
        migrations.RemoveField(
            model_name='teamrepo',
            name='agile_practices',
        ),
        migrations.RemoveField(
            model_name='teamrepo',
            name='jira_board_link',
        ),
        migrations.RemoveField(
            model_name='teamrepo',
            name='jira_project_name',
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='action_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='audit_details',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='audit_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='team',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='teams', through='core.TeamSkill', to='core.skill'),
        ),
        migrations.AlterField(
            model_name='team',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Paused', 'Paused'), ('Disbanded', 'Disbanded')], default='Active', max_length=20),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='created_by_user',
            field=models.ForeignKey(db_column='created_by_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='created_meetings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='team',
            field=models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='core.team'),
        ),
        migrations.AddField(
            model_name='message',
            name='author_user',
            field=models.ForeignKey(db_column='author_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='recipient_user',
            field=models.ForeignKey(db_column='recipient_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='organisation',
            field=models.ForeignKey(db_column='organisation_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.organisation'),
        ),
        migrations.AddField(
            model_name='teamemployee',
            name='employee',
            field=models.ForeignKey(db_column='employee_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.employee'),
        ),
        migrations.AddField(
            model_name='teamemployee',
            name='team',
            field=models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', through='core.TeamEmployee', to='core.employee'),
        ),
        migrations.DeleteModel(
            name='AppUser',
        ),
        migrations.RemoveField(
            model_name='meetingteam',
            name='meeting',
        ),
        migrations.RemoveField(
            model_name='meetingteam',
            name='team',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='team',
        ),
        migrations.AddConstraint(
            model_name='teamemployee',
            constraint=models.UniqueConstraint(fields=('employee', 'team'), name='unique_employee_team_membership'),
        ),
        migrations.DeleteModel(
            name='MeetingInstance',
        ),
        migrations.DeleteModel(
            name='MeetingTeam',
        ),
        migrations.DeleteModel(
            name='TeamMember',
        ),
    ]
