# Author : w2105627
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.utils import timezone


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.organisation_name


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    full_name = models.CharField(max_length=255)
    employee_email = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.full_name

    @classmethod
    def create_for_user(cls, user, full_name):
        return cls.objects.create(
            user=user,
            full_name=full_name,
        )


class Department(models.Model):
    department_name = models.CharField(max_length=255, unique=True)

    department_head = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="departments",
        null=True
    )

    def __str__(self):
        return self.department_name


class Skill(models.Model):
    skill_name = models.CharField(max_length=255, unique=True)
    skill_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.skill_name


class Team(models.Model):
    team_leader = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_teams",
    )

    team_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    disbanded_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        default="Active",
        choices=[
            ("Active", "Active"),
            ("Paused", "Paused"),
            ("Disbanded", "Disbanded"),
        ],
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    team_description = models.CharField(max_length=255, null=True, blank=True)
    team_mission = models.CharField(max_length=255, null=True, blank=True)
    responsibilities = models.CharField(max_length=255, null=True, blank=True)

    members = models.ManyToManyField(
        Employee,
        through="TeamEmployee",
        related_name="teams",
        blank=True,
    )

    skills = models.ManyToManyField(
        Skill,
        through="TeamSkill",
        related_name="teams",
        blank=True,
    )

    def __str__(self):
        return self.team_name


class TeamEmployee(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    team_join_date = models.DateTimeField(default=timezone.now)
    left_team_date = models.DateTimeField(null=True, blank=True)
    team_role = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "team"],
                name="unique_employee_team_membership",
            )
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.team.team_name}"


class TeamSkill(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_skill_links",
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="team_skill_links",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "skill"],
                name="unique_team_skill",
            )
        ]

    def __str__(self):
        return f"{self.team.team_name} - {self.skill.skill_name}"


class TeamRepo(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="repositories",
    )

    codebase_link = models.CharField(max_length=255, null=True, blank=True)
    versioning_approach = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Repo {self.id} - {self.team.team_name}"


class TeamContact(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    team_email = models.CharField(max_length=255, null=True, blank=True)
    slack_channel = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Contact {self.id} - {self.team.team_name}"


class Dependency(models.Model):
    downstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="downstream_dependencies",
    )

    upstream_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="upstream_dependencies",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(downstream_team=F("upstream_team")),
                name="dependencies_not_self",
            ),
            models.UniqueConstraint(
                fields=["downstream_team", "upstream_team"],
                name="unique_team_dependency",
            ),
        ]

    def __str__(self):
        return (
            f"{self.downstream_team.team_name} depends on "
            f"{self.upstream_team.team_name}"
        )


class Message(models.Model):
    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )

    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255)
    message_date = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=30,
        default="Sent",
        choices=[
            ("Sent", "Sent"),
            ("Draft", "Draft"),
            ("Read", "Read"),
        ],
    )

    def __str__(self):
        return f"{self.subject or 'Message'} from {self.author_user}"


class Meeting(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="meetings",
    )

    title = models.CharField(max_length=255)
    meeting_date = models.DateTimeField()
    meeting_description = models.CharField(max_length=255, null=True, blank=True)

    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_meetings",
    )

    def __str__(self):
        return f"{self.title} - {self.meeting_date}"


class AuditLog(models.Model):
    CREATE_TEAM = "CREATE_TEAM"
    EDIT_TEAM = "EDIT_TEAM"
    DELETE_TEAM = "DELETE_TEAM"

    ACTION_CHOICES = [
        (CREATE_TEAM, "Create team"),
        (EDIT_TEAM, "Edit team"),
        (DELETE_TEAM, "Delete team"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action_type = models.CharField(max_length=30, choices=ACTION_CHOICES)
    audit_details = models.CharField(max_length=255, blank=True)
    audit_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} by {self.user}"
