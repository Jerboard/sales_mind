from django.db import models
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.db.models import Count, Q, F

import logging
import typing as t

from enums import HANDLER_KEY_CHOICES, HANDLER_KEY_DICT, PayType, PAY_TYPE_CHOICES


logger = logging.getLogger(__name__)


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
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="email")

    subscription_end = models.DateTimeField(null=True, blank=True, verbose_name="Окончание подписки")
    requests_remaining = models.IntegerField(default=0, verbose_name="Осталось запросов")
    tariff = models.ForeignKey("Tariff", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тариф")

    source = models.CharField(max_length=255, null=True, blank=True, verbose_name="Источинк")

    is_accepted = models.BooleanField(verbose_name="Принял правила", default=False)
    is_ban = models.BooleanField(verbose_name="Заблокирован", default=False)
    is_used_trial = models.BooleanField(verbose_name="Использовал пробный", default=False)

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        # managed = False

    def __str__(self):
        return f'{self.full_name}'

    @classmethod
    def update(
            cls, user_id: int, requests: int = None, subscription_end: datetime = None, tariff_id: int = None
    ) -> None:
        updates = {}
        if requests:
            updates['requests_remaining'] = requests
        if subscription_end:
            updates['subscription_end'] = subscription_end
        if tariff_id:
            updates['tariff_id'] = tariff_id

        logger.warning(updates)
        # Выполняем единый UPDATE в базе
        cls.objects.filter(id=user_id).update(**updates)


    @classmethod
    def get_user(cls, user_id: int) -> t.Self:
        return cls.objects.filter(id=user_id).first()


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
    ordering = models.IntegerField(verbose_name="Сортировка", default=1)

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
    ordering = models.IntegerField(verbose_name="Сортировка", default=1)

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
    is_unlimited = models.BooleanField(default=False, verbose_name="Безлимитный тариф")
    ordering = models.IntegerField(verbose_name="Сортировка", default=1)

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_by_id(cls, tariff_id: int) -> t.Self:
        return cls.objects.filter(id=tariff_id).first()


class Request(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость",)
    response_count = models.IntegerField(verbose_name="Количество запросов", default=0)
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    ordering = models.IntegerField(verbose_name="Сортировка", default=1)

    class Meta:
        db_table = "requests"
        verbose_name = "Запрос докупить"
        verbose_name_plural = "Запросы докупить"

    def __str__(self):
        return f'{self.price}'

    @classmethod
    def get_by_id(cls, request_id: int) -> t.Self:
        return cls.objects.filter(id=request_id).first()


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

    @classmethod
    def add(cls,
            user_id: int,
            action: str,
            session: str = None,
            comment: str = None,
            msg_id: int = None) -> t.Self:
        data = {
            "user_id": user_id,
            "action": action,
        }
        if session:
            data["session"] = session
        if comment:
            data["comment"] = comment
        if msg_id:
            data["msg_id"] = msg_id

        return cls.objects.create(**data)

    def get_unique_users(self, period: str = None) -> int:
        """
        period: 'day', 'week' или 'month'
        """
        now = datetime.now()
        if period == 'day':
            since = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            since = now - timedelta(days=7)
        elif period == 'month':
            since = now - timedelta(days=30)
        elif period == 'active':
            since = now - timedelta(days=3)
        else:
            return LogsUser.objects.values('user').distinct().count()

        return (
            LogsUser.objects
                .filter(created_at__gte=since)
                .values('user')
                .distinct()
                .count()
        )

    def get_users_with_multiple_sessions(self) -> int:
        """
        Считает уникальных пользователей у которых distinct(session) > 1
        за указанный период: 'day', 'week' или 'month'.
        """

        return (
            LogsUser.objects
            .values('user')
            .annotate(session_count=Count('session', distinct=True))
            .filter(session_count__gt=1)
            .count()
        )

    def get_percent_multiple_sessions(self, all_users_count: int,  multisession_users_count: int = None) -> float:
        """
        Процент пользователей с >1 сессией за заданный период.
        Возвращает число в формате float (например, 12.5 для 12.5%).
        """
        if not multisession_users_count:
            multisession_users_count = self.get_users_with_multiple_sessions()
        return round(multisession_users_count / all_users_count * 100, 2)

    def get_total_messages(self) -> int:
        """
        Общее число логов с msg (сообщениями) за период.
        """
        return LogsUser.objects.count()

    def get_avg_messages_per_session(self, total_msg: int) -> float:
        """
        Среднее число сообщений на одну сессию за период.
        """
        # считаем число уникальных сессий, где session не пустой
        sessions = (
            LogsUser.objects
            .filter(~Q(session=None))
            .values('session')
            .distinct()
            .count()
        )
        if sessions == 0:
            return 0.0
        return round(total_msg / sessions, 2)


    def get_top_actions(self, limit: int = 5):
        """
        Возвращает список топ-{limit} action с их количеством за период.
        """
        qs = (
            LogsUser.objects
                .values('action')
                .annotate(count=Count('action'))
                .order_by('-count')[:limit]
        )
        # приводим к нужному формату
        return [{"command": HANDLER_KEY_DICT.get(item["action"]), "count": item["count"]} for item in qs]


class Text(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    key = models.CharField(max_length=255, verbose_name="Ключ")
    text = models.TextField(verbose_name="Текст", help_text=help_text_for_text)
    ordering = models.IntegerField(verbose_name="Сортировка", default=1)

    class Meta:
        db_table = "texts"
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"

    def __str__(self):
        return f'{self.key}'

    @classmethod
    def get_by_key(cls, key: str) -> t.Self:
        return cls.objects.filter(key=key).first()


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    tariff = models.ForeignKey("Tariff", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тариф")
    amount = models.FloatField(verbose_name="Сумма")
    payment_id = models.CharField(max_length=255, verbose_name="ID платежа")
    payment_type = models.CharField(
        max_length=255, verbose_name="Тип платежа", default=PayType.TARIFF.value, choices=PAY_TYPE_CHOICES
    )

    class Meta:
        db_table = "payments"
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} — {self.amount} ₽"

    @classmethod
    def add(cls, user_id: int, tariff_id: int, amount: float, payment_id: str, payment_type: str) -> None:
        return cls.objects.create(
            user_id=user_id,
            tariff_id=tariff_id,
            amount=amount,
            payment_id=payment_id,
            payment_type=payment_type,
        )

    @classmethod
    def get_unique_users(cls) -> int:
        return cls.objects.values('user').distinct().count()


class DisallowCategory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    category = models.ForeignKey("PromptCategory", on_delete=models.CASCADE, verbose_name="Категория")
    tariff = models.ForeignKey("Tariff", on_delete=models.CASCADE, verbose_name="Тариф")

    class Meta:
        db_table = "disallow_categories"
        verbose_name = "Запрещённый сценарий"
        verbose_name_plural = "Запрещённые сценарии"

    def __str__(self):
        return f"{self.category} — {self.tariff}"

