from .models import *
from django.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.conf import settings
from django.conf.urls.static import static

class OfferForm(ModelForm):
     class Meta:
        model=Offer
        fields=['price','time','unit','content']
        widgets={
            'price':NumberInput(attrs={'min':'100','name':'price'}),
            'time':NumberInput(attrs={'min':'1','name':'time'}),
            'unit':Select(attrs={'name':'summa'},
                 choices=(('$','Доллар США'),('руб.','Рубль'),('€','Евро'))
                 ),
            'content':Textarea(attrs={'rows':'7'})
            }

class OrderForm(ModelForm):
     class Meta:
        model=Order
        fields=['name','price','unit','content','category','files']
        widgets={
        'name':TextInput(attrs={'name':'title'}),
        'price':NumberInput(attrs={'min':'100','name':'price'}),
        'unit':Select(attrs={'name':'summa'},
                 choices=(('$','Доллар США'),('руб.','Рубль'),('€','Евро'))
                 ),
        'content':Textarea(attrs={'rows':'7','name':'content','id':'id_content'}),
        'category':Select(attrs={'name':'category','required':True},
            choices=tuple((i.id,i.title) for i in Category.objects.all())),
        'files':ClearableFileInput(attrs={'multiple': True,'accept':'.zip,.rar,.7zip,.jpg,.png,.jpeg'})}

class AddPortf(ModelForm):
     class Meta:
        model=PortProject
        fields=['name','content','files','category','prev']
        widgets={
        'name':TextInput(attrs={'name':'title'}),
        'content':Textarea(attrs={'name':'content'}),
        'images':FileField(widget=ClearableFileInput(attrs={'multiple': True})),
        'category':Select(attrs={'class':'category'},
            choices=tuple((i.id,i.title) for i in Category.objects.all()))}

class ViewForm(ModelForm):
     class Meta:
        model=View
        fields=['content','char']
        widgets={
          'content':Textarea(attrs={'name':'content'}),
          'char':Select(attrs={'name':'kind'},choices=[(1,'Положительный'),
                                                       (2,'Нейтральный'),(3,'Отрицательный')])
          }

class UserUpdateForm(ModelForm):
    class Meta:
        model = SiteUser
        fields = ['content','picture']

class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=30, help_text='Optional.')
    last_name = CharField(max_length=30, help_text='Optional.')
    email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class MessageForm(ModelForm):
     class Meta:
        model=Message
        fields=['theme','content','files']
        widgets={
        'theme':TextInput(attrs={'name':'theme'}),
        'content':Textarea(attrs={'rows':'7','name':'content'}),
        'files':ClearableFileInput(attrs={'multiple': True,'accept':'.zip,.rar,.7zip,.jpg,.png,.jpeg'})}
