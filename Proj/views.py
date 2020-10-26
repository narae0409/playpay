from django.views.generic import ListView, FormView
from django.views import View
from Proj.models import *
from taggit.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from Proj.forms import *
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
import json
import hashlib
from django.db.models import Q


class Login(FormView):
    form_class = LoginForm
    template_name ="Proj/login.html"

    def get(self,request,*args,**kwargs):
        form = self.form_class(initial= self.initial)
        #request.session['login'] = False # 추가 session
        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_pw = form.cleaned_data['your_pw']
            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            
            try:
                 data = User.objects.get(my_id=new_id)
            except Exception:
                return redirect('proj:login')

            if x == data.pw:
                request.session['login'] = True # 추가 로그인 성공시 True 설정
                request.session['my_id'] = data.my_id
                request.session['time'] = data.time
                request.session['name'] = data.name

                return redirect('proj:main')
            else:
                return redirect('proj:login')
        
        return render(request,self.template_name,{'form':form})
    

class Main(View):

    def get(self, request, *args, **kwargs):
        #if not request.session.get('login', False):
        #    return HttpResponseRedirect('/')
        
        userdata = request.session.get('my_id')
        context = {'model_list':['Board'], 'userdata':userdata}

        return render(request, 'Proj/main.html', context=context)

class Join(FormView):
    form_class = JoinForm
    template_name ="Proj/join.html"

    def get(self,request,*args,**kwargs):
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):                  #my_id, pw, name, number, prof
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_pw = form.cleaned_data['your_pw']
            new_ph = form.cleaned_data['your_ph']
            new_name = form.cleaned_data['your_name']
            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            try:
                User.objects.create(my_id=new_id, pw=x, name=new_name, ph=new_ph)
            except:
                return redirect('proj:join')
            request.session['login'] = False
            return HttpResponseRedirect('/')
        
        return render(request,self.template_name,{'form':form})


class Edit(FormView):
    form_class = EditForm
    template_name = 'Proj/edit.html'

    def get(self,request,*args,**kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        new_my_id = request.session.get('my_id')
        form = self.form_class(initial= {'your_id':new_my_id})

        return render(request,self.template_name,{'form':form, 'my_id':new_my_id}) #, 'new_id':new_id
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_my_id = request.session.get('my_id')
            new_pw = form.cleaned_data['your_pw']
            new_ph = form.cleaned_data['your_ph']
            new_name = form.cleaned_data['your_name']
            try:
                data = User.objects.get(my_id=new_my_id)
            except Exception:
                return HttpResponse(Exception)

            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            if new_name != data.name or new_ph != data.ph or x != data.pw:
                data.pw=x
                data.ph=new_ph
                data.name=new_name
                data.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/edit/')
        request.session['login'] = False

        return render(request,self.template_name,{'form':form})        


class Logout(View):

    def get(self, request, *args, **kwargs):
        request.session['login'] = False
        request.session['my_id'] = {}
        request.session['name'] = {}
        request.session['time'] = {}
        return HttpResponseRedirect('/')


class Admin(FormView):
    form_class = AdminForm
    template_name = 'Proj/admin.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_prof = form.cleaned_data['your_prof']
            try:
                post_instance = User.objects.filter(my_id=new_id)
                post_instance.update(prof=new_prof)
            except Exception:
                return render(request, 'Proj/admin.html', {'form':form})

            return HttpResponseRedirect('/admin/')

        return render(request, 'Proj/admin.html', {'form':form})

class Maps(View):
    
    def get(self, request, name):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        pcname = name
        return render(request, 'Proj/maps.html', {'name':pcname})           

class Setting(FormView):
    form_class = SettingForm
    template_name = 'Proj/main.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = SettingForm
        return render(request, 'Proj/setting.html' ,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)    
        if form.is_valid():
            new_boardnum = form.cleaned_data['your_settingnum']
            time = new_boardnum
            return render(request, self.template_name ,{'form':form})

class Distance(View):
    
    def get(self, request):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        
        return render(request, 'Proj/distance.html')  

class Boarding(View):
    
    def get(self, request):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        val = request.session.get('my_id')
        userdata = User.objects.get(my_id = val)
        boarddata1 = Board.objects.all()

        return render(request, 'proj/board.html', {'userdata':userdata, 'boarddata':boarddata1})


class BoardManage(FormView):
    form_class = BoardManageForm
    template_name = 'Proj/boardmanage.html'
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_boardnum = form.cleaned_data['your_boardnum']
            new_board = form.cleaned_data['your_board']
            Board.objects.create(boardnum=new_boardnum, title=new_board)                

        return redirect('proj:main')

class ContentList(View):

    def get(self, request, boardnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.filter(boardnumber=boardnum).order_by('-id')
        form = SearchForm
        bn = boardnum
        return render(request, 'proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})

    def post(self, request, boardnum):
    
        data = Text.objects.filter(boardnumber=boardnum).order_by('-star')
        bn = boardnum
        form = SearchForm
        return render(request, 'proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})


class SearchContent(FormView):
    form_class = SearchForm
    template_name = 'Proj/contentlist.html'
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, boardnum):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_search = form.cleaned_data['your_search']
            data = Text.objects.filter(boardnumber=boardnum).filter(tags__name=new_search)
            print(data)
            print(new_search)
            bn = boardnum
            return render(request, 'Proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})

        return redirect('proj:main')


class Content(View):
    def get(self, request, boardnum, textnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.get(id=textnum)
        bn = boardnum
        tn = textnum
        return render(request, 'proj/content.html', {'data':data, 'bn':bn, 'tn':tn})


class Write(FormView):
    form_class = BoardForm
    template_name = 'Proj/write.html'


    def get(self, request):
        mid = request.session.get('my_id')
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        if mid != 'admin@admin.admin':
            form = self.form_class(initial= self.initial)
            return render(request,self.template_name,{'form':form})
        else:
            form = NoticeForm
            return render(request, self.template_name, {'form':form})

    def post(self, request):
        mid = request.session.get('my_id')
        if mid != 'admin@admin.admin':
            form = self.form_class(request.POST)
            if form.is_valid():            
                new_board = form.cleaned_data['your_board']
                me = Board.objects.get(boardnum=new_board)
                new_title = form.cleaned_data['your_title']
                new_content = form.cleaned_data['your_content']
                new_star = form.cleaned_data['your_star']
                new_tag = form.cleaned_data['your_tag'].split(',')

                data = Text.objects.create(id=None,boardnumber=me, text_title=new_title, content=new_content, star=new_star)    
                if new_tag != None:
                    for tag in new_tag:
                        tag = tag.strip()
                        data.tags.add(tag)            

            return HttpResponseRedirect('/board/1/')

        else:
            form = NoticeForm(request.POST)
            if form.is_valid():            
                new_board = form.cleaned_data['your_board']
                me = Board.objects.get(boardnum=new_board)
                new_title = form.cleaned_data['your_title']
                new_content = form.cleaned_data['your_content']
                new_star = request.POST.get('star_')

                Text.objects.create(id=None,boardnumber=me, text_title=new_title, content=new_content, star=new_star)

            return HttpResponseRedirect('/board/')            


class Delete(View):
    def get(self, request, boardnum, textnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.get(id=textnum)
        data.delete()

        return HttpResponseRedirect('/board/1/')

def Fox(request):
    name = 'fox'
    return render(request, 'pc/fox.html', {'name':name})

def Ghostcastle(request):
    name = 'ghostcastle'
    return render(request, 'pc/ghostcastle.html', {'name':name})

def Lime(request):
    name = 'lime'
    return render(request, 'pc/lime.html', {'name':name})

def Pop(request):
    name = 'pop'
    return render(request, 'pc/pop.html', {'name':name})

def Skybridge(request):
    name = 'skybridge'
    return render(request, 'pc/skybridge.html', {'name':name})

def Ocelot(request):
    name = 'ocelot' 
    return render(request, 'pc/ocelot.html', {'name':name})

def Pclist(request):
    name1='fox'
    name2='ghostcastle'
    name3='lime'
    name4='ocelot'
    name5='pop'
    name6='skybridge'
    context = {'name1':name1,'name2':name2,'name3':name3,'name4':name4,'name5':name5,'name6':name6}
    return render(request, 'pc/pclist.html', context=context)


def Payment(request):
    try:
        new_id = request.session.get('my_id')
        info = User.objects.get(my_id=new_id)
        info.time += 30
        info.save()
        request.session['time'] = info.time
    except Exception:
        return redirect('proj:main')
    return redirect('proj:main')
    
def Refund(request):
    try:
        new_id = request.session.get('my_id')
        info = User.objects.get(my_id=new_id)
        info.time -= 30
        if (info.time < 0):
            info.time += 30
            return redirect('proj:main')
        else:
            info.save()
        request.session['time'] = info.time
    except Exception:
        return redirect('proj:main')
    return redirect('proj:main')