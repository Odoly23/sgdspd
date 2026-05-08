import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from custom.models import  Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
                           Year, Estructure
from django.template.loader import render_to_string
from django.contrib import messages
from membro.models import Membru, LocationTL, ContactInfo, AddressOrigin, MembroPosition, Photo, FormalEducation
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class DateInput(forms.DateInput):
	input_type = 'date'

class MembroForm(forms.ModelForm):
	dob = forms.DateField(label="Data Moris", widget=DateInput(), required=True)

	class Meta:
		model = Membru
		fields = ['nu_id','name','sex','pob','dob','marital',\
			      'file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('nu_id', css_class='form-group col-md-5 mb-0'),
				Column('name', css_class='form-group col-md-5 mb-0'),
				Column('sex', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('pob', css_class='form-group col-md-4 mb-0'),
				Column('dob', css_class='form-group col-md-4 mb-0'),
				Column('marital', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(

				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML("""
                <div class="text-center mt-4">
                    <div class="text-left mt-4">
                        <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save">
                            <span class="btn-label"><i class="fa fa-save"></i></span> Save
                        </button>

                        <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="history.back()">
                            <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                        </button>
                    </div>
                </div>
            """)
        )


class ContactInfoForm(forms.ModelForm):
	class Meta:
		model = ContactInfo
		fields = ['email','phone']

	def __init__(self, *args, **kwargs):
		super(ContactInfoForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('email', css_class='form-group col-md-4 mb-0'),
				Column('phone', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML("""
                <div class="text-center mt-4">
                    <div class="text-left mt-4">
                        <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save">
                            <span class="btn-label"><i class="fa fa-save"></i></span> Save
                        </button>

                        <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="history.back()">
                            <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                        </button>
                    </div>
                </div>
            """)
        )

class LocationTLForm(forms.ModelForm):
	class Meta:
		model = LocationTL
		fields = ['municipality','administrativepost','village','aldeia']

	def __init__(self, *args, **kwargs):
		super(LocationTLForm, self).__init__(*args, **kwargs)
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		self.fields['aldeia'].queryset = SubVillage.objects.none()
		
		if 'municipality' in self.data:
			try:
				municipality_id = int(self.data.get('municipality'))
				self.fields['administrativepost'].queryset = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.municipality:
			self.fields['administrativepost'].queryset = self.instance.municipality.administrativepost_set.order_by('-id')

		if 'administrativepost' in self.data:
			try:
				administrativepost_id = int(self.data.get('administrativepost'))
				self.fields['village'].queryset = Village.objects.filter(administrativepost_id=administrativepost_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.administrativepost:
			self.fields['village'].queryset = self.instance.administrativepost.village_set.order_by('name')

		if 'village' in self.data:
			try:
				village_id = int(self.data.get('village'))
				self.fields['aldeia'].queryset = SubVillage.objects.filter(village_id=village_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.village:
			self.fields['aldeia'].queryset = self.instance.village.aldeia_set.order_by('name')

class AddressOriginForm(forms.ModelForm):
	class Meta:
		model = AddressOrigin
		fields = ['city','address']
	
	def __init__(self, *args, **kwargs):
		super(AddressOriginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('city', css_class='form-group col-md-6 mb-0'),
				Column('address', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML("""
                <div class="text-center mt-4">
                    <div class="text-left mt-4">
                        <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save">
                            <span class="btn-label"><i class="fa fa-save"></i></span> Save
                        </button>

                        <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="history.back()">
                            <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                        </button>
                    </div>
                </div>
            """)
        )

class PhotoUploadForm(forms.ModelForm):
	image = forms.FileField(label="Upload Photo", required=False)

	class Meta:
		model = Photo
		fields = ['image']

class FormalEducationForm(forms.ModelForm):
	graduation_year = forms.DateField(label="Tinan Gradua", widget=DateInput(), required=False)
	summary = forms.CharField(label="Resumu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = FormalEducation
		fields = ['educationlevel','university','faculty','studyprogram','area','graduation_year','file','summary']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('university', css_class='form-group col-md-5 mb-0'),
				Column('educationlevel', css_class='form-group col-md-3 mb-0'),
				Column('faculty', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('studyprogram', css_class='form-group col-md-5 mb-0'),
				Column('area', css_class='form-group col-md-5 mb-0'),
				Column('graduation_year', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('summary', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML("""
                <div class="text-center mt-4">
                    <div class="text-left mt-4">
                        <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save">
                            <span class="btn-label"><i class="fa fa-save"></i></span> Save
                        </button>

                        <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="history.back()">
                            <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                        </button>
                    </div>
                </div>
            """)
        )

class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = MembroPosition
        fields = ['estructure','position']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(

            Row(
                Column('estructure', css_class='col-md-6'),
                Column('position', css_class='col-md-6'),
            ),
			HTML("""
                <div class="text-center mt-4">
                    <div class="text-left mt-4">
                        <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save">
                            <span class="btn-label"><i class="fa fa-save"></i></span> Save
                        </button>

                        <button class="btn btn-sm btn-labeled btn-secondary" type="button" onclick="history.back()">
                            <span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel
                        </button>
                    </div>
                </div>
            """)
        )
