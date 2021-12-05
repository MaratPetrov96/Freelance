from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=70)
    def __repr__(self):
        return self.title
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'

class SiteUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,
                                primary_key=True)
    seller=models.BooleanField(default=False)
    content=models.TextField('Описание',blank=True)
    picture=models.ImageField(blank=True,upload_to='static/')
    categories=models.ManyToManyField(Category,related_name='sellers',blank=True)

    def __repr__(self):
        return self.user.username
    def __str__(self):
        return self.user.username

class Order(models.Model):
    user=models.ForeignKey(SiteUser,on_delete=models.CASCADE,
                           related_name='orders')
    content=models.TextField('Содержание')
    name=models.CharField('Заголовок',max_length=100)
    price=models.IntegerField('Цена')
    unit=models.CharField(max_length=10,
                          choices=(('$','Доллар США'),('руб.','Рубль'),('€','Евро'))
                          ,default='руб.')
    date=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,
                               related_name='orders')
    files = models.FileField(blank=True,upload_to='static/')
    status=models.BooleanField(default=True)
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

class Offer(models.Model):
    user=models.ForeignKey(SiteUser,on_delete=models.CASCADE,
                           related_name='offers')
    order=models.ForeignKey(Order,on_delete=models.CASCADE,
                           related_name='offers')
    content=models.TextField('Содержание',default='')
    unit=models.CharField('Валюта',max_length=10,
                          choices=(('$','Доллар США'),('руб.','Рубль'),('€','Евро'))
                          ,default='руб.')
    price=models.IntegerField('Цена')
    date=models.DateTimeField(auto_now_add=True)
    time=models.IntegerField('Срок (в днях)')

    def __repr__(self):
        return f'{self.user.user.username} ({self.price}): {self.content}'
    def __str__(self):
        return f'{self.user.user.username} ({self.price}): {self.content}'

class PortProject(models.Model):
    user=models.ForeignKey(SiteUser,on_delete=models.CASCADE,
                           related_name='portfolio')
    name=models.CharField('Название',max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,
                               related_name='projects')
    content=models.TextField('Содержание')
    files = models.FileField(blank=True,upload_to='static/')
    prev = models.ImageField(blank=True,upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)

class View(models.Model):
    viewer=models.ForeignKey(User,on_delete=models.CASCADE,
                             related_name='views_from')
    viewed=models.ForeignKey(User,on_delete=models.CASCADE,
                             related_name='views_about')
    content=models.TextField('Содержание')
    char=models.CharField('Характер отзыва',max_length=10,
                          choices=(('-1','Отрицательный'),('0','Нейтральный'),('1','Положительный'))
                          ,default='0')
    date=models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f'{self.content}'

class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,
                           related_name='sent')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,
                           related_name='received')
    theme=models.CharField('Название',max_length=100)
    content=models.TextField('Содержание')
    files = models.FileField(blank=True,upload_to='messages/')
    date=models.DateTimeField(auto_now_add=True)
    unread=models.BooleanField(default=True)
