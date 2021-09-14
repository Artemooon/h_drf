from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Creator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rating = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    foundation_date = models.DateField(auto_now_add=True)
    logo_url = models.URLField(null=True)

    def __str__(self):
        return self.name


class GameCategory(models.Model):
    category_name = models.CharField(max_length=150, null=False)
    slug = models.SlugField(null=False, blank=True, unique=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(GameCategory, self).save(*args, **kwargs)


class Game(models.Model):
    name = models.CharField('Название игры', max_length=100, unique=True)
    description = models.TextField('Краткое описание игры')
    rating = models.PositiveSmallIntegerField('Рейтинг игры', validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    create_date = models.DateField('Дата выхода игры', auto_now_add=True)
    logo_url = models.URLField(null=True)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    categories = models.ManyToManyField(GameCategory, related_name="categories")

    def __str__(self):
        return self.name
