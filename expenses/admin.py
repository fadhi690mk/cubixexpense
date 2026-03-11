from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Fund,
    Expense,
    ExpenseCategory,
    ExpenseDocument,
    ActivityLog,
    Todo,
    Contributor
)


# -----------------------
# Base Admin (Soft Delete)
# -----------------------
class SoftDeleteAdmin(admin.ModelAdmin):
    actions = ["soft_delete", "restore_records"]

    def get_queryset(self, request):
        # Show ALL records (active and inactive) in admin
        return super().get_queryset(request).all()

    def soft_delete(self, request, queryset):
        queryset.update(is_active=False)
    soft_delete.short_description = "🗑️ Soft delete selected records"

    def restore_records(self, request, queryset):
        queryset.update(is_active=True)
    restore_records.short_description = "↩️ Restore selected records"

    def is_active_display(self, obj):
        """Display is_active status with color"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Active</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Deleted</span>'
            )
    is_active_display.short_description = "Status"


# -----------------------
# Contributor Admin
# -----------------------
@admin.register(Contributor)
class ContributorAdmin(SoftDeleteAdmin):
    list_display = ("id", "name", "is_active_display", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


# -----------------------
# Fund Admin
# -----------------------
@admin.register(Fund)
class FundAdmin(SoftDeleteAdmin):
    list_display = (
        "id",
        "contributor",
        "amount",
        "date",
        "added_by",
        "is_active_display",
    )
    list_filter = ("contributor", "date", "is_active")
    search_fields = ("description", "contributor__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-date",)


# -----------------------
# Expense Category Admin
# -----------------------
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(SoftDeleteAdmin):
    list_display = ("id", "name", "is_active_display", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


# -----------------------
# Expense Document Inline
# -----------------------
class ExpenseDocumentInline(admin.TabularInline):
    model = ExpenseDocument
    extra = 1
    readonly_fields = ("uploaded_by", "created_at")


# -----------------------
# Expense Admin
# -----------------------
@admin.register(Expense)
class ExpenseAdmin(SoftDeleteAdmin):
    list_display = (
        "id",
        "category",
        "amount",
        "date",
        "paid_by",
        "is_active_display",
    )
    list_filter = ("category", "date", "is_active")
    search_fields = ("description",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ExpenseDocumentInline]
    ordering = ("-date",)


# -----------------------
# Activity Log Admin (Read-only)
# -----------------------
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "model_name",
        "object_id",
        "timestamp",
    )
    list_filter = ("action", "model_name", "timestamp")
    search_fields = ("description", "user__username")
    readonly_fields = (
        "user",
        "action",
        "model_name",
        "object_id",
        "description",
        "timestamp",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# -----------------------
# Todo Admin
# -----------------------
@admin.register(Todo)
class TodoAdmin(SoftDeleteAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "estimated_amount",
        "target_date",
        "status_display",
        "created_by",
        "is_active_display",
    )
    list_filter = ("status", "target_date", "is_active", "category")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-target_date",)

    def status_display(self, obj):
        """Display status with color"""
        colors = {
            "PENDING": "blue",
            "COMPLETED": "green",
            "CANCELLED": "gray"
        }
        color = colors.get(obj.status, "black")
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
        )
    status_display.short_description = "Status"
