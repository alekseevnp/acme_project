from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField(
        "Фамилия", blank=True, help_text="Необязательное поле", max_length=20
    )
    birthday = models.DateField("Дата рождения", validators=(real_age,))
    image = models.ImageField("Фото", upload_to="birthdays_images", blank=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("first_name", "last_name", "birthday"),
                name="Unique person constraint",
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse("birthday:detail", kwargs={"pk": self.pk})


class Congratulation(models.Model):
    text = models.TextField("Текст поздравления")
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name="congratulations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)
