from django.contrib import admin
from django.contrib.auth import get_user_model
from project_management.models import Project, ProjectMembers

User = get_user_model()

admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectMembers)
