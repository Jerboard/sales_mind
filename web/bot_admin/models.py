from django.db import models
# from django.utils import timezone


# Пользователи
class User(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Первый визит")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последний визит")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    subscription_end = models.DateTimeField(null=True, blank=True, verbose_name="Окончание подписки")

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        # managed = False

    def __str__(self): return self.full_name


# Логи ошибок
class LogsError(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, db_column="user_id", verbose_name="Пользователь", null=True, blank=True
    )
    traceback = models.TextField(null=True, blank=True, verbose_name="Traceback")
    message = models.TextField(null=True, blank=True, verbose_name="Сообщение")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        db_table = "logs_error"
        verbose_name = "Лог ошибки"
        verbose_name_plural = "Логи ошибок"
        # managed = False

    def __str__(self): return f"Ошибка #{self.id}"


# Категории промптов
class PromptCategory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    name = models.CharField(max_length=255, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        db_table = "prompt_categories"
        verbose_name = "Категория промптов"
        verbose_name_plural = "Категории промптов"
        # managed = False

    def __str__(self): return self.name


# Промпты
class Prompt(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    category = models.ForeignKey(PromptCategory, on_delete=models.CASCADE, db_column="category_id", verbose_name="Категория")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название")
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name="Модель")
    hint = models.TextField(null=True, blank=True, verbose_name="Подсказка")
    role = models.TextField(null=True, blank=True, verbose_name="Роль")
    prompt = models.TextField(null=True, blank=True, verbose_name="Промпт")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        db_table = "prompts"
        verbose_name = "Промпт"
        verbose_name_plural = "Промпты"
        # managed = False

    def __str__(self): return self.name or f"Промпт #{self.id}"
