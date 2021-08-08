from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Creator(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    foundation_date = models.DateField(auto_now_add=True)
    logo_url = models.URLField(null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField('Название игры', max_length=100)
    description = models.TextField('Краткое описание игры')
    rating = models.PositiveSmallIntegerField('Рейтинг игры', validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    create_date = models.DateField('Дата выхода игры', auto_now_add=True)
    logo_url = models.URLField(null=True)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

