from django.contrib import admin

from network_search.programs.models import Program
from network_search.programs.forms import ProgramAdminForm


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramAdminForm
