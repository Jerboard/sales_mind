# myapp/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import User, LogsError, PromptCategory, Prompt


# ────────── inlines ──────────
class PromptInline(TabularInline):
    model = Prompt
    extra = 0
    fields = ("name", "model", "hint", "role", "prompt", "is_active")
    show_change_link = True            # клик → полноценная форма Prompt
    ordering = ("-updated_at",)


# ────────── основные модели ──────────
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("id", "full_name", "username", "subscription_end", "created_at", "updated_at")
    search_fields = ("full_name", "username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(LogsError)
class LogsErrorAdmin(ModelAdmin):
    list_display = ("id", "message", "created_at")
    # list_filter = ("user",)
    search_fields = ("message", "traceback")
    readonly_fields = ("traceback", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(PromptCategory)
class PromptCategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "is_active", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    inlines = (PromptInline,)          # вкладываем промпты прямо в категорию
    readonly_fields = ("created_at", "updated_at")


@admin.register(Prompt)
class PromptAdmin(ModelAdmin):
    list_display = ("id", "name", "category", "model", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "model", "category")
    search_fields = ("name", "hint", "role", "prompt")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")

