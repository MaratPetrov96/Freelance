from django.shortcuts import render,get_object_or_404,redirect
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import DetailView,UpdateView
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.urls import reverse
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import UserPassesTestMixin

order_num = 5 #количество заказов на одной странице/number of order in one page

def unread(request): #количество непрочитанных сообщений/number of unread messages
    if request.user.is_authenticated:
        return Message.objects.filter(unread=True,receiver=request.user).count()
    else:
        return 0

@login_required #отмена заказа/canceling order
def cancel(request,pk):
    if request.method=='POST':
        one=Order.objects.get(pk=pk)
        one.status=False
        one.save()
    return redirect('main')

def main(request): #главная страница/main page
    return render(request,'Main.html',{'user':request.user,'title':'Главная страница','data':Category.objects.all(),
                                       'unread':unread(request)})

def sellers(request,cat=None,pg=None): #страница с исполнителями/sellers page
    if not pg:
        pg=1
    if not cat: #все
        data=Paginator(SiteUser.objects.filter(seller=True).all(),20).page(pg)
    else: #определённой категории
        cat=Category.objects.get(pk=cat)
        title=cat.title
        data=Paginator(cat.sellers.all(),20).page(pg)
    return render(request,'Users.html',{'user':request.user,'data':data,'cat':cat,'title':'Фрилансеры',
                                        'catg':Category.objects.all(),'unread':unread(request)})

def Orders(request,cat,pg=None): #страница с заказами/orders page
    if not pg:
        pg=1
    if cat: #определённой категории
        data=Order.objects.filter(category=Category.objects.get(id=cat)).all()
    else: #все
        data=Order.objects.all()
    return render(request,'Orders.html',{'user':request.user,'orders':Paginator(data,order_num).page(pg),'title':'Заказы','catg':Category.objects.all()
                                         ,'cat_id':cat,'unread':unread(request)})
def kind(filename): #проверка типа файла в просмотре заказа или портфолио
    return any([filename.endswith(i) for i in ('.jpg','.png','.jpeg')])

class OrderView(DetailView): #просмотр заказа/view order
    model=Order
    template_name='OrderPage.html'
    context_object_name='order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=self.object.name
        context['form'] = OfferForm
        context['user'] = self.request.user
        context['unread'] = unread(self.request)
        context['filetype'] = kind(self.object.files.name)
        context['filename'] = self.object.files.name.split('/')[-1]
        return context

@login_required
def new_order(request): #добавление заказа/adding order
    error=''
    if request.method=='POST':
        data=OrderForm(request.POST, request.FILES)
        if data.is_valid():
            new=data.save(commit=False)
            new.user=request.user.siteuser
            new.save()
            #file = request.FILES['files']
            #file_name = default_storage.save(file.name, file)
            #new.save()
            return HttpResponseRedirect(reverse('Order', args=(new.id,)))
        error='Ошибка'
    return render(request,'AddingOrder.html',{'user':request.user,'form':OrderForm,'title':'Добавление заказа','error':error,
                                              'unread':unread(request),'link':'<a href=*ссылка*>Текст, описывающий ссылку</a>'})

@login_required
def offer(request,order): #предложение/offer sending
    if request.method=='POST':
        data=OfferForm(request.POST)
        work=get_object_or_404(Order,id=order)
        if data.is_valid():
            off=data.save(commit=False)
            off.user=request.user.siteuser
            off.order=work
            off.save()
            work.offers.add(off)
            work.save()
    return redirect('Order',pk=order)

class UserView(DetailView): #просмотр страницы пользователя/view user page
    model=SiteUser
    template_name='UserPage.html'
    context_object_name='user_pg'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=self.object.user.username
        context['user']=self.request.user
        context['unread'] = unread(self.request)
        return context

class PortfolioView(DetailView): #просмотр портфолио/portfolio view
    model=PortProject
    template_name='Portfolio.html'
    context_object_name='project'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=self.object.name
        context['user']=self.request.user
        context['unread'] = unread(self.request)
        return context

class PortfolioEdit(UserPassesTestMixin,UpdateView): #редактирование портфолио/portfolio editor
    model=PortProject
    template_name='PortfolioEditor.html'
    fields=['category','content','files','prev']
    def test_func(self, **kwargs):
        return self.request.user.pk==self.get_object().user.pk
    def get_absolute_url(self):
        return redirect('Portfolio',pk=self.get_object().pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=self.object.name
        context['user'] = self.request.user
        context['unread'] = unread(self.request)
        context['test'] = '<p>'+'</p><p>'.join(dir(self))+'</p>'
        return context

@login_required
def message_view(request,pk): #просмотр сообщения/viewing a message
    m=Message.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user not in (m.receiver,m.sender):
            return redirect('main')
        if request.user==m.receiver and m.unread==True:
            m.unread=False
            m.save()
        return render(request,'Message.html',{'title':'Сообщение','user':request.user,
                                          'unread':unread(request),'message':m,'filename':m.files.name.split('/')[-1]})
    return redirect('sign')

@login_required
def editor(request): #редактор профиля/profile editor
    if request.method=='POST':
        user=request.user.siteuser
        new=UserUpdateForm(request.POST, request.FILES,instance=user)
        if new.is_valid():
            new.save()
    form=UserUpdateForm(initial=model_to_dict(request.user.siteuser))
    return render(request,'UserEditor.html',{'user':request.user,'title':'Редактирование профиля',
                                             'user_pg':request.user.siteuser,'unread':unread(request),
                                             'count':User.objects.get(pk=request.user.pk).views_about.count()})

def views(request,pk,pg=None): #отзывы/reviews
    if not pg:
        pg=1
    data=Paginator(User.objects.get(pk=pk).views_about.all(),20).page(pg)
    return render(request,'UserViews.html',{'user':request.user,'data':data,'title':'Отзывы','user_pg':SiteUser.objects.get(pk=pk),
                                            'form':ViewForm,'unread':unread(request),'count':User.objects.get(pk=pk).views_about.count()})

@login_required
def Viewing(request,pk): #оставление отзыва/sending review
    if request.method == 'POST':
        form = ViewForm(request.POST)
        if form.is_valid():
            view=form.save(commit=False)
            view.viewer=request.user
            view.viewed=User.objects.get(pk=pk)
            view.save()
    return HttpResponseRedirect(
        reverse('views',kwargs={'u_id':pk,'pg':Paginator(User.objects.get(id=pk).views,20).count})
        )

@login_required
def chat(request,pg=None): #полученные сообщения/view received messages
    if not pg:
        pg=1
    data=Paginator(Message.objects.filter(receiver=request.user).all(),20).page(pg)
    return render(request,'Messenger.html',{'user':request.user,'data':data,'title':'Сообщения','unread':unread(request)})

@login_required
def sent(request,pg=None): #отправленные сообщения/view sent messages
    if not pg:
        pg=1
    data=Paginator(Message.objects.filter(sender=request.user).all(),20).page(pg)
    return render(request,'Messenger.html',{'user':request.user,'data':data,'title':'Сообщения','unread':unread(request)})

@login_required
def message(request,user): #отправка сообщения/sending message
    if user!=request.user.pk:
        if request.method=='POST':
            form = MessageForm(request.POST, request.FILES)
            if form.is_valid():
                new=form.save(commit=False)
                new.sender=request.user
                new.receiver=User.objects.get(pk=user)
                new.save()
                return redirect('messenger')
        return render(request,'MessageForm.html',{'user':request.user,'user_pg':SiteUser.objects.get(pk=user),'form':MessageForm,
                                                  'title':'Написать сообщение','unread':unread(request),
                                                  'count':request.user.views_about.count()})
    return redirect('main')

@login_required
def portfolio_table(request): #просмотр портфолио/viewing portfolio
    data=request.user.siteuser.portfolio.all()
    return render(request,'PortfolioTable.html',{'user':request.user,'data':data,'title':'Редактирование','user_pg':request.user.siteuser
                                                 ,'unread':unread(request),'count':request.user.views_about.count()})

@login_required
def portfolio(request): #пополнение портфолио/extending portfolio
    if request.method=='POST':
        form=AddPortf(request.POST,request.FILES)
        if form.is_valid():
            su=request.user.siteuser
            new=form.save(commit=False)
            new.user=su
            new.save()
            if not su.seller: #добавление пользователя в список фрилансеров/adding user to sellers list
                su.seller=True
            if form.cleaned_data.get('category') not in su.categories.all(): #добавление пользователю категории/adding category to user's ones
                su.categories.add(form.cleaned_data.get('category'))
            su.save()
            return redirect('UPage',pk=request.user.id)
    return render(request,'AddForm.html',{'user':request.user,'form':AddPortf(),'title':'Добавление работы','unread':unread(request)})

def search(request): #поиск/search)
    if request.method=='POST':
        data=PortProject.objects.filter(content__icontains=request.POST['query'])
        return render(request,'Search.html',{'user':request.user,'res':data,'unread':unread(request)})

@login_required
def close(request,id_): #отмена заказа/closing order
    Order.objects.get(pk=id_).status=False
    Order.objects.get(pk=id_).save()
    return redirect('main')

def group(request): #заказы определённой категории/orders of category
    if request.POST:
        arg = request.POST.get('select',None)
        return redirect('orders',cat=arg,pg=1)

def signup(request): #авторизация/authorization
    if request.method == 'POST':
        form = UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            user=SiteUser(user=user)
            user.save()
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'Sign.html', {'form': form,'user':request.user,'title':'Регистрация','unread':unread(request)})

def LogIn(request): #аутентификация/authentication
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('main')
    form = AuthenticationForm
    return render(request, 'Login.html', {'form': form,'user':request.user,'title':'Вход','unread':unread(request)})

@login_required
def LogOut(request): #выход из аккаунта/log out)
    logout(request)
    return HttpResponseRedirect(request.path_info)

def download(request,filename): #скачать файл/upload file
    if request.method=='POST':
        file_path = os.path.join('static', filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read())
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

def download_from_mess(request,filename): #скачать файл/upload file
    if request.method=='POST':
        file_path = os.path.join('messages', filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read())
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
