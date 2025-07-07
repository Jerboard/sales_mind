from django.db import models
from django.utils.safestring import mark_safe

from enums import HANDLER_KEY_CHOICES


help_text_for_text = mark_safe(
    '&lt;b&gt;&lt;/b&gt; - <b>жирный</b> '
    '&lt;i&gt;&lt;/i&gt; - <i>италик</i> '
    '&lt;u&gt;&lt;/u&gt; - <u>подчёркнутый</u> '
    '&lt;s&gt;&lt;/s&gt; - <s>зачёркнутый</s> '
    '&lt;code&gt;&lt;/code&gt; - <code>моноширинный (копируется)</code>'
    '&lt;pre&gt;&lt;/pre&gt; - <pre>блок кода</pre>'
    )


# Пользователи
class User(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Первый визит")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последний визит")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    subscription_end = models.DateTimeField(null=True, blank=True, verbose_name="Окончание подписки")
    requests_remaining = models.IntegerField(default=0, verbose_name="Осталось запросов")
    is_accepted = models.BooleanField(verbose_name="Принял правила", default=False)
    is_ban = models.BooleanField(verbose_name="Заблокирован", default=False)

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        # managed = False

    def __str__(self):
        return f'{self.full_name}'


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

    def __str__(self):
        return f"Ошибка #{self.id}"


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

    def __str__(self):
        return f'{self.name}'


# Промпты
class Prompt(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    category = models.ForeignKey(PromptCategory, on_delete=models.CASCADE, db_column="category_id", verbose_name="Категория")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название")
    role = models.TextField(null=True, blank=True, verbose_name="Роль")
    prompt = models.TextField(null=True, blank=True, verbose_name="Промпт")
    hint = models.TextField(null=True, blank=True, verbose_name="Подсказка", help_text=help_text_for_text)
    model = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Модель",
        help_text='gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4.1, gpt-4.1-mini, o3-pro, o3, o4-mini, gpt-3.5-turbo-0125'
    )
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

    def __str__(self):
        return f"Промпт #{self.id} {self.name}"


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

    def __str__(self):
        return f"Запрос #{self.id}"


class Tariff(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    name = models.CharField(max_length=100, verbose_name="Название", help_text="На кнопке",)
    description = models.TextField(verbose_name="Описание", help_text=help_text_for_text)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость",)
    duration = models.IntegerField(verbose_name="Продолжительность в днях", default=0)
    response_count = models.IntegerField(verbose_name="Количество запросов", default=0)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f'{self.name}'


class Info(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    name = models.CharField(max_length=100, verbose_name="Название", help_text="На кнопке")
    description = models.TextField(verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        db_table = "info"
        verbose_name = "Информация"
        verbose_name_plural = "Информация"

    def __str__(self):
        return f'{self.name}'


class LogsUser(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    action = models.CharField(max_length=255, verbose_name="Действие", choices=HANDLER_KEY_CHOICES)
    session = models.CharField(max_length=255, verbose_name="Сессия", null=True, blank=True)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    msg = models.ForeignKey("Message", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ответ ГПТ")

    class Meta:
        db_table = "logs_users"
        verbose_name = "Действия пользователя"
        verbose_name_plural = "Действия пользователей"

    def __str__(self):
        return f"{self.user} — {self.action}"


class Text(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    key = models.CharField(max_length=255, verbose_name="Ключ")
    text = models.TextField(verbose_name="Текст", help_text=help_text_for_text)

    class Meta:
        db_table = "texts"
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"

    def __str__(self):
        return f'{self.key}'
