# Author : w2105627
from django.contrib import admin
from .models import (
    Organisation,
    Employee,
    Department,
    Skill,
    Team,
    TeamEmployee,
    TeamSkill,
    TeamRepo,
    TeamContact,
    Dependency,
    Message,
    Meeting,
    AuditLog,
)

admin.site.register(Organisation)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Skill)
admin.site.register(Team)
admin.site.register(TeamEmployee)
admin.site.register(TeamSkill)
admin.site.register(TeamRepo)
admin.site.register(TeamContact)
admin.site.register(Dependency)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(AuditLog)
