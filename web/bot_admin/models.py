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
    model = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Модель",
        help_text='gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4.1, gpt-4.1-mini, o3-pro, o3, o4-mini, gpt-3.5-turbo-0125'
    )
    hint = models.TextField(null=True, blank=True, verbose_name="Подсказка")
    role = models.TextField(null=True, blank=True, verbose_name="Роль")
    prompt = models.TextField(null=True, blank=True, verbose_name="Промпт")
    temperature = models.FloatField(
        verbose_name="Температура", default=0.9, help_text=f'От 0 до 2. Чем выше, тем креативнее (>1.3 глючит)'
    )
    presence_penalty = models.FloatField(
        verbose_name="Штраф за темы", default=0.4, help_text=f'От -2 до 2. Чем выше, больше тем (>1 глючит)'
    )
    frequency_penalty = models.FloatField(
        verbose_name="Штраф за повторы", default=0.3, help_text=f'От -2 до 2. Чем выше, больше формулировок (большее 1.3 глючит)'
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        db_table = "prompts"
        verbose_name = "Промпт"
        verbose_name_plural = "Промпты"
        # managed = False

    def __str__(self): return self.name or f"Промпт #{self.id}"


# Промпты
class Message(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    prompt = models.ForeignKey("Prompt", on_delete=models.CASCADE, verbose_name="Промпт")
    request = models.TextField(verbose_name="Запрос")
    response = models.TextField(verbose_name="Ответ")
    time_answer = models.CharField(verbose_name='Время ответа')
    prompt_tokens = models.IntegerField(verbose_name='Токенов запроса')
    completion_tokens = models.IntegerField(verbose_name='Токенов ответа')

    is_like = models.BooleanField(verbose_name="Понравился ответ", null=True, blank=True)

    class Meta:
        db_table = "messages"
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
        # managed = False

    def __str__(self): return self.user or f"Запрос #{self.id}"
