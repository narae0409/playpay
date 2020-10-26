from django import forms
from Proj.models import *


class JoinForm(forms.Form):
    your_id = forms.EmailField(label='아이디', max_length=100)
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)
    your_ph = forms.IntegerField(label='전화번호(숫자만)')
    your_name = forms.CharField(label='이름', max_length=10)

class LoginForm(forms.Form):
    your_id = forms.EmailField(label='아이디', max_length=100)
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)

class AdminForm(forms.Form):
    your_id = forms.EmailField(label='학생 ID', max_length=100)

class EditForm(forms.Form):
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)
    your_ph = forms.CharField(label='전화번호', max_length=11)
    your_name = forms.CharField(label='이름', max_length=10)

class BoardForm(forms.Form):
    your_board = forms.ChoiceField(widget = forms.Select(), choices = ([('1','리뷰 게시판')]), initial='1', label='게시판 선택', required = True)
    your_title = forms.CharField(max_length=200, label='제목')
    your_content = forms.CharField(widget=forms.Textarea, label='내용')
    your_star = forms.ChoiceField(widget = forms.Select(), choices = ([('1','★'), ('2','★★'),('3','★★★'), ('4','★★★★'), ('5','★★★★★')]), initial='1', label='별점 선택', required = True)
    your_tag = forms.CharField(max_length=200, label='태그', required=False, widget=forms.TextInput(attrs={'placeholder': 'comma-separated'}))

class NoticeForm(forms.Form):
    your_board = forms.ChoiceField(widget = forms.Select(), choices = ([('1','리뷰 게시판'), ('2','공지사항')]), initial='1', label='게시판 선택', required = True)
    your_title = forms.CharField(max_length=200, label='제목')
    your_content = forms.CharField(widget=forms.Textarea, label='내용')

class BoardManageForm(forms.Form):
    your_boardnum = forms.IntegerField(label='게시판번호')
    your_board = forms.CharField(label='게시판명', max_length=100)

class SearchForm(forms.Form):
    your_search = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter HashTags..'}))

class SettingForm(forms.Form):
    your_settingnum = forms.IntegerField(label='시간설정')