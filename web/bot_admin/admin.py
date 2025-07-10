# myapp/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import User, LogsError, PromptCategory, Prompt, Message, Tariff, Info, LogsUser, Text
from web.settings import DEBUG


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
    list_display = ("id", "full_name", "username", "subscription_end", "is_ban", "created_at", "updated_at")
    search_fields = ("full_name", "username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_editable = ["is_ban"]


@admin.register(LogsError)
class LogsErrorAdmin(ModelAdmin):
    list_display = ("created_at", "message", "traceback")
    # list_filter = ("user",)
    search_fields = ("message",)
    readonly_fields = ("traceback", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(PromptCategory)
class PromptCategoryAdmin(ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    inlines = (PromptInline,)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Prompt)
class PromptAdmin(ModelAdmin):
    list_display = ("name", "category", "model", 'role', 'prompt', "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "model", "category")
    search_fields = ("name", "hint", "role", "prompt")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("user", "created_at", "time_answer", "prompt_tokens", "completion_tokens", "is_like")
    list_filter = ("prompt", "user", "is_like", "created_at")
    search_fields = ("request", "response")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(Tariff)
class TariffAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "price", "is_active", "updated_at")
    list_editable = ("name", "description", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(Info)
class InfoAdmin(ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(LogsUser)
class LogsUserAdmin(ModelAdmin):
    change_list_template = "bot_admin/log_error_statistic.html"
    # list_before_template = "bot_admin/log_error_statistic.html"

    list_display = ("created_at", "user", "action", "msg", "comment")
    readonly_fields = ("id", "user", "action", "msg", "created_at", "updated_at", "session")
    search_fields = ("user__id", "action")
    list_filter = ("action",)
    ordering = ("-created_at",)


@admin.register(Text)
class InfoKeyAdmin(ModelAdmin):
    list_display = ("key", "text", "updated_at")
    readonly_fields = ["id", "created_at", "updated_at"]
    list_editable = ("text",)
    ordering = ("id",)

    if not DEBUG:
        readonly_fields.append('key')

        # **Блокируем добавление и удаление через админку**
        def has_add_permission(self, request):
            return False

        def has_delete_permission(self, request, obj=None):
            return False
