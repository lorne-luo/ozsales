# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from material import Layout, Row, Fieldset

from .models import Seller


class SellerProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if 'username_readonly' in kwargs:
            username_readonly = kwargs.pop('username_readonly')
        else:
            username_readonly = False

        super(SellerProfileForm, self).__init__(*args, **kwargs)
        if username_readonly:
            self.fields['username'].widget.attrs['readonly'] = True

    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Seller
        fields = ['name']


class PasswordLengthValidator(object):
    ''' check password length '''

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 4:
            raise ValidationError("Password must be at least 4 characters.")
        return password1


class ResetPasswordEmailForm(SetPasswordForm, PasswordLengthValidator):
    email_user = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'toggle'}))

    class Meta:
        model = Seller
        fields = ['password1', 'password2']

    def save(self, commit=True, request=None,
             email_template_name='email/admin_reset_password_txt.html',
             html_email_template_name='email/admin_reset_password.html',
             from_email=None):

        self.user.set_password(self.cleaned_data['new_password1'])

        # print self.email_user
        if self.cleaned_data['new_password1'] and self.cleaned_data['email_user'] and self.user.email:
            from django.template import loader
            from django.contrib.sites.models import get_current_site
            from django.core.mail import EmailMultiAlternatives

            current_site = get_current_site(request)
            if not from_email:
                from_email = settings.DEFAULT_FROM_EMAIL

            c = {
                'name': self.user.get_short_name(),
                'username': self.user.username,
                'password': self.cleaned_data['new_password1'],
                'site_name': current_site.name,
                'site': current_site.domain
            }

            subject = 'Password Reset'
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None

            msg = EmailMultiAlternatives(subject, email, from_email, [self.user.email])
            msg.attach_alternative(html_email, "text/html")
            msg.send()

        if commit:
            self.user.save()
        return self.user


class UserResetPasswordForm(PasswordChangeForm, PasswordLengthValidator):
    class Meta:
        model = Seller
        fields = ['password1', 'password2']


class RegisterForm(forms.Form):
    mobile = forms.CharField(label=u"澳洲或国内手机", validators=[
        RegexValidator(regex='^\d*$', message=u'请输入合法的澳洲或国内手机号，无需国际区号', code='Invalid number')])
    email = forms.EmailField(label=u"电子邮件 (可选)", required=False)
    # name = forms.CharField(label=u"姓名", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label=u"密 码", min_length=6, error_messages={
        'min_length': _(u'密码最小长度6位'),
        'required': _(u'必填项'),
    })
    password_confirm = forms.CharField(widget=forms.PasswordInput, label=u"确认密码")

    layout = Layout('mobile', 'email',
                    Row('password', 'password_confirm'))

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')

        if password1 and password1 != password2:
            self.add_error('password_confirm', u'确认密码不匹配，请重新输入')

        return self.cleaned_data


class SellerProfileForm2(RegisterForm):
    name = forms.CharField(label=u"姓名", required=False)

    def __init__(self, *args, **kwargs):
        super(SellerProfileForm2, self).__init__(*args, **kwargs)

class LoginForm(forms.Form):
    mobile = forms.CharField(label=u"澳洲或国内手机", validators=[
        RegexValidator(regex='^\d*$', message=u'请输入澳洲或国内手机号，无需区号', code='Invalid number')],error_messages={
        'required': _(u'请填写手机号'),
    })
    password = forms.CharField(widget=forms.PasswordInput, label=u"密 码", min_length=6, error_messages={
        'min_length': _(u'密码最小长度6位'),
        'required': _(u'请填写密码'),
    })
