from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Region(models.Model):
    """Административный район провинции Гуйчжоу: связь один-ко-многим с достопримечательностями."""

    name = models.CharField("Название района", max_length=80, unique=True)
    description = models.TextField("Описание района", blank=True)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Feature(models.Model):
    """Тематическая особенность достопримечательности: связь многие-ко-многим."""

    name = models.CharField("Название особенности", max_length=50, unique=True)
    icon = models.CharField("Иконка", max_length=8, default="✨")

    class Meta:
        verbose_name = "Особенность"
        verbose_name_plural = "Особенности"
        ordering = ["name"]

    def __str__(self):
        return f"{self.icon} {self.name}"


class ScenicSpot(models.Model):
    """Основная таблица достопримечательностей."""

    class Category(models.TextChoices):
        NATURE = "nature", "Природный ландшафт"
        CULTURE = "culture", "Исторический городок"
        WATERFALL = "waterfall", "Водопады и ущелья"
        CAVE = "cave", "Пещеры и карст"
        ETHNIC = "ethnic", "Этническая культура"

    name = models.CharField("Название достопримечательности", max_length=120)
    region = models.ForeignKey(
        Region,
        verbose_name="Район",
        related_name="spots",
        on_delete=models.PROTECT,
    )
    features = models.ManyToManyField(
        Feature,
        verbose_name="Особенности",
        related_name="spots",
        blank=True,
    )
    category = models.CharField("Тип достопримечательности", max_length=20, choices=Category.choices)
    short_description = models.TextField("Краткое описание")
    address = models.CharField("Адрес", max_length=180)
    ticket_price = models.DecimalField("Цена билета", max_digits=7, decimal_places=2)
    rating = models.PositiveSmallIntegerField(
        "Рейтинг рекомендации",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Оценка от 1 до 5",
    )
    opening_date = models.DateField("Дата открытия/создания")
    is_world_heritage = models.BooleanField("Объект Всемирного наследия", default=False)
    image_url = models.URLField("Ссылка на изображение", blank=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Достопримечательность"
        verbose_name_plural = "Достопримечательности"
        ordering = ["region__name", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("spot_detail", kwargs={"pk": self.pk})


class SpotProfile(models.Model):
    """Дополнительная информация: связь один-к-одному с достопримечательностью."""

    spot = models.OneToOneField(
        ScenicSpot,
        verbose_name="Достопримечательность",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    best_season = models.CharField("Лучший сезон для поездки", max_length=80)
    suggested_hours = models.PositiveSmallIntegerField("Рекомендуемое время посещения, часы", default=3)
    transport_tips = models.TextField("Советы по транспорту")
    official_phone = models.CharField("Телефон для справок", max_length=30, blank=True)

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"

    def __str__(self):
        return f"Дополнительная информация: {self.spot.name}"
