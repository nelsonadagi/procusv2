from django.contrib import admin
from .models import Project, ProjectRequirement, InvestmentCommitment, ProjectContractLink, ProjectUpdate


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'estimated_budget', 'funding_required', 'created_at')
    list_filter = ('status', 'funding_required', 'created_at', 'category')
    search_fields = ('title', 'description', 'location_text', 'formatted_address')
    readonly_fields = ('created_at',)


@admin.register(ProjectRequirement)
class ProjectRequirementAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'description', 'quantity')
    list_filter = ('type',)


@admin.register(InvestmentCommitment)
class InvestmentCommitmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'investor', 'amount_committed', 'status', 'created_at')
    list_filter = ('status', 'created_at')


@admin.register(ProjectContractLink)
class ProjectContractLinkAdmin(admin.ModelAdmin):
    list_display = ('project', 'contract')


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'posted_by', 'created_at')
    readonly_fields = ('created_at',)
