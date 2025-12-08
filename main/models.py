from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    second_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        parts = [self.last_name or "", self.first_name or "", self.second_name or ""]
        fio = " ".join(p for p in parts if p).strip()
        return f"{fio} ({self.username})" if fio else self.username


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=999)
    drawing = models.FileField(upload_to="drawings/")
    information = models.CharField(max_length=999999)
    articul = models.CharField(max_length=999999)


    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return f"{self.name}"


class Status(models.TextChoices):
    INWORK = "В работе","В работе"
    DONE = "Выполнен", "Выполнен"
    NOTDONE = "Не выполнен", "Не выполнен"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # что делать при удалении пользователя
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,  # что делать при удалении пользователя
    )
    deadline = models.DateField()
    status = models.CharField(max_length=999999, choices=Status.choices, default=Status.NOTDONE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ от {self.user.last_name} {self.user.first_name}, материал {self.material.name}"
# Create your models here.
