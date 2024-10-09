from django import forms
from adminpanel.models import Profile, Blog, Comment, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import  PasswordChangeForm


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label = 'Phone:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your phone number '
    }))
    profile_image = forms.ImageField(label = 'Profile image:', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    id_proof = forms.ImageField(label = 'ID Proof:', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    profile_description = forms.CharField(label = 'About:', required=True, widget = forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Describe yourself '
    }))
    class Meta:
        model = Profile
        fields = ['phone', 'profile_image', 'id_proof', 'profile_description']

        
class BlogForm(forms.ModelForm):
    status_choices = (
        ('PUBLISH', 'Publish'),
        ('DRAFT', 'Draft'),
    )
    title = forms.CharField(label = 'Title:', required=True, widget = forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your blog title '
    }))
    content = forms.CharField(label = 'Description:', required=True, widget = forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Describe blog content '
    }))
    blog_image = forms.ImageField(label = 'Blog image', required=True, widget = forms.ClearableFileInput(attrs={
        'class' : 'form-control'
       
    }))
    status = forms.ChoiceField(choices = status_choices, required=True, initial='PUBLISH', widget = forms.RadioSelect(attrs={
        'class' : 'form-radio-inline'
    }))
    class Meta:
        model = Blog
        fields = ['title','content','blog_image','status']



class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=200, required = True,
    label="", widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'post your comments here.....'
    }))
    class Meta:
        model = Comment
        fields = ['comment']


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(label= 'First Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(label= 'Last Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    username = forms.CharField(label= 'Username',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
   
    password1 = forms.CharField(label= 'Password',required = True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(label= 'Confirm Password',required = True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your confirm password'
    }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password1', 'password2']


class RegistrationEditForm(forms.ModelForm):

    first_name = forms.CharField(label= 'First Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(label= 'Last Name',required = True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'  # Set the readonly attribute
        })
    )
   
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        



class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username',max_length=100,required = True,
     widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your username'
    }))   
    password = forms.CharField(label = 'Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Enter your password'
    }))     

 
class ResetPasswordForm(PasswordChangeForm):
    def __int__(self, user, *args, **kwargs):
        super().__int__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']        


class AdminResetPasswordForm(PasswordChangeForm):
    def __int__(self, user, *args, **kwargs):
        super().__int__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ['old_password1', 'new_password3', 'new_password4']


class SiteResetPasswordForm(forms.Form):
    username = forms.CharField(label = 'Username',max_length=100,required = True,
     widget = forms.TextInput(attrs={
        'class':'form-control',
         'placeholder':'Enter your username'
    }))   
    password3 = forms.CharField(label = 'Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Enter your new password'
    }))   
    password4 = forms.CharField(label = 'Password',max_length=100,required = True,
     widget = forms.PasswordInput(attrs={
        'class':'form-control', 
        'placeholder':'Confirm your password'
    }))   

    class Meta:
        fields = ['username', 'password3', 'password4']        


class ForgotPasswordForm(forms.ModelForm):
    email = forms.CharField(label= 'Email',required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))

    class Meta:
        model = User
        fields = ['email']

    
class OtpForm(forms.Form):
    otp = forms.CharField(label='Enter Otp', max_length=6, min_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter 6 digit otp'
    }))    