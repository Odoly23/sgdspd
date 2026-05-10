from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('email', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-sm btn-primary" type="submit">Altera <i class="fa fa-save"></i></button> """)
		)

from django.contrib.auth.forms import PasswordChangeForm
class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}))
	new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput())
	new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ['old_password','new_password1','new_password2']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('old_password', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('new_password1', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('new_password2', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-sm btn-primary" type="submit">Alterar <i class="fa fa-save"></i></button> """)
		)