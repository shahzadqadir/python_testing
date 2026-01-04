from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "notes")


admin.site.register(Company, CompanyAdmin)
