from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def post_published(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )

    def get_published_post(self, post_id):
        post = get_object_or_404(Post, id=post_id)
        if (not post.is_published
                or not post.category.is_published
                or post.pub_date > timezone.now()):
            raise Http404('Страница не найдена')
        return post


class CategoryQuerySet(models.QuerySet):
    def category_post(self, slug):
        category = get_object_or_404(Category, slug=slug)
        if not category.is_published:
            raise Http404('Страница не найдена')
        return category


class Category(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок', null=False)
    description = models.TextField(verbose_name='Описание', null=False)
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        null=False,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено', null=False)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название места', null=False)
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено', null=False)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок', null=False)
    text = models.TextField(verbose_name='Текст', null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        null=False,
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        null=False
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено', null=False)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
