

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_employee_employee_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='dependency',
            name='unique_team_dependency_type',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='audit_log_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='department_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='dependency',
            old_name='dependency_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='employee_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='meeting',
            old_name='meeting_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='organisation',
            old_name='organisation_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='skill',
            old_name='skill_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='team_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='teamcontact',
            old_name='team_contact_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='teamrepo',
            old_name='repo_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='dependency',
            name='dependency_type',
        ),
        migrations.RemoveField(
            model_name='auditlog',
            name='entity_id',
        ),
        migrations.RemoveField(
            model_name='auditlog',
            name='entity_type',
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teamcontact',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teamemployee',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teamrepo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teamskill',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='core.team'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='action_type',
            field=models.CharField(choices=[('CREATE_TEAM', 'Create team'), ('EDIT_TEAM', 'Edit team'), ('DELETE_TEAM', 'Delete team')], max_length=30),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='audit_details',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='audit_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_departments', to='core.employee'),
        ),
        migrations.AlterField(
            model_name='department',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.organisation'),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='downstream_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downstream_dependencies', to='core.team'),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='upstream_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upstream_dependencies', to='core.team'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='created_by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_meetings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='core.team'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='core.department'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_teams', to='core.employee'),
        ),
        migrations.AlterField(
            model_name='teamcontact',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='core.team'),
        ),
        migrations.AlterField(
            model_name='teamemployee',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.employee'),
        ),
        migrations.AlterField(
            model_name='teamemployee',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', to='core.team'),
        ),
        migrations.AlterField(
            model_name='teamrepo',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='core.team'),
        ),
        migrations.AlterField(
            model_name='teamskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_skill_links', to='core.skill'),
        ),
        migrations.AlterField(
            model_name='teamskill',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_skill_links', to='core.team'),
        ),
        migrations.AddConstraint(
            model_name='dependency',
            constraint=models.UniqueConstraint(fields=('downstream_team', 'upstream_team'), name='unique_team_dependency'),
        ),
        migrations.AlterModelTable(
            name='auditlog',
            table=None,
        ),
        migrations.AlterModelTable(
            name='department',
            table=None,
        ),
        migrations.AlterModelTable(
            name='dependency',
            table=None,
        ),
        migrations.AlterModelTable(
            name='employee',
            table=None,
        ),
        migrations.AlterModelTable(
            name='meeting',
            table=None,
        ),
        migrations.AlterModelTable(
            name='message',
            table=None,
        ),
        migrations.AlterModelTable(
            name='organisation',
            table=None,
        ),
        migrations.AlterModelTable(
            name='skill',
            table=None,
        ),
        migrations.AlterModelTable(
            name='team',
            table=None,
        ),
        migrations.AlterModelTable(
            name='teamcontact',
            table=None,
        ),
        migrations.AlterModelTable(
            name='teamemployee',
            table=None,
        ),
        migrations.AlterModelTable(
            name='teamrepo',
            table=None,
        ),
        migrations.AlterModelTable(
            name='teamskill',
            table=None,
        ),
    ]
