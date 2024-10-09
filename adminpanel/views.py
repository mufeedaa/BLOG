from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog,Profile, Comment, User
from userpanel.forms import BlogForm, CommentForm, LoginForm, AdminResetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


@login_required(login_url='/404/')
def adminhome(request):
    logged_user = request.user
    user_count = User.objects.filter(is_staff = False).count()
    active_user_count = User.objects.filter(is_active = True, is_staff = False).count()
    blog_count = Blog.objects.exclude(status='DRAFT').count()
    published_blog_count = Blog.objects.filter(status = 'PUBLISH').count()

    context = { 
    'user_count':user_count,
    'active_user_count':active_user_count,
    'blog_count':blog_count,
    'published_blog_count':published_blog_count,
    'logged_user':logged_user

    }
    return render(request, 'adminpanel/admin_home.html',context)

@login_required(login_url='/404/')
def userlist(request):
    
    users = User.objects.filter(is_staff=False)
    profiles = Profile.objects.all()
    context = {
        
        'profiles' : profiles,
        'users': users
    }
    return render(request, 'adminpanel/user_list.html', context) 

@login_required(login_url='/404/')
def userstatus(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if user.is_active:
        user.is_active = False
        messages.success(request, f'User {user.username} has been deactivated.')
    else:
        user.is_active = True
        messages.success(request, f'User {user.username} has been activated.')

    user.save()
    return redirect('admin_userlist')
    


       

@login_required(login_url='/404/')
def userview(request, user_id):
    user = get_object_or_404(User, id = user_id)
    profile = user.profile

    return render(request, 'adminpanel/view_user.html',  {'user': user, 'profile': profile})    

@login_required(login_url='/404/')   
def activeusers(request):
    users = User.objects.filter(is_active = True, is_staff = False)
    return render(request, 'adminpanel/active_users.html', {'users':users})

@login_required(login_url='/404/')
def inactiveusers(request):
    users = User.objects.filter(is_active = False)
    return render(request, 'adminpanel/inactive_users.html', {'users':users})    

@login_required(login_url='/404/')
def bloglist(request):
    blogs = Blog.objects.exclude(status='DRAFT').order_by('-updated_at').filter(author__is_active = True)
    return render(request, 'adminpanel/blog_list.html', {'blogs': blogs}) 
    

@login_required(login_url='/404/')
def blogview(request, blog_id):
    logged_user = request.user
    blog = get_object_or_404(Blog, id = blog_id)

    comments = Comment.objects.filter(blog = blog ).all()
    
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit = False)
    #         comment.blog = blog
    #         comment.author = logged_user 
    #         comment.save()
    #         return redirect('admin_blogview', blog_id = blog_id)
    # else:
    #     form = CommentForm()        

        # if 'comment_hide' in request.POST:
        #     comment_id = request.POST.get('comment_hide')
        #     if request.user.is_staff:
        #         comment = get_object_or_404(Comment, id=comment_id, blog=blog)
        #         comment.status = 'hidden'
        #         comment.save()
        #         messages.success(request, ' Comment has been hidden.')

        # elif 'comment_show' in request.POST:
        #     comment_id = request.POST.get('comment_show')
        #     if request.user.is_staff:
        #         comment = get_object_or_404(Comment, id = comment_id, blog=blog)
        #         comment.status = 'visible'
        #         comment.save()
        #         messages.success(request, 'Comment is now visible')        


    context = {'blog': blog ,
    'logged_user':logged_user,
    # 'form': form,
    'comments':comments
    }
    return render(request, 'adminpanel/blog_view.html', context)    

@login_required(login_url='/404/')
def blogstatus(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    #  the status between 'hidden' and 'publish'
    if blog.status == 'HIDDEN':
        blog.status = 'PUBLISH'
    else:
        blog.status = 'HIDDEN'
    
    # Save the blog
    blog.save()
    
    # Redirect to the blog list or any other page
    return redirect('admin_bloglist')




@login_required(login_url='/404/')
def user_blog_list(request, user_id):
   
    user = get_object_or_404(User, id=user_id)
    blogs = Blog.objects.filter(author = user ).exclude(status = 'DRAFT').order_by('-created_at')
   
    return render(request, 'adminpanel/user_blog_list.html', {'blogs':blogs, 'user':user })

@login_required(login_url='/404/')
def user_published_blog(request, user_id):
    user = get_object_or_404(User, id=user_id)
    blogs = Blog.objects.filter(author = user , status = 'PUBLISH').order_by('-created_at')
    return render(request, 'adminpanel/published_blogs.html', {'blogs':blogs, 'user':user })


@login_required(login_url='/404/')
def user_hidden_blog(request, user_id):
    user = get_object_or_404(User, id=user_id)
    blogs = Blog.objects.filter(author = user , status = 'HIDDEN').order_by('-created_at')
    return render(request, 'adminpanel/hidden_blogs.html', {'blogs':blogs})    

# def comment_status(request, comment_id):
   
#     if request.user.is_staff:
#         comment = get_object_or_404(Comment, id=comment_id)

    
#         if comment.status == 'hidden':
#             comment.status = 'visible'
#         else:
#             comment.status = 'hidden'
#         comment.save()
#     return redirect('admin_blogview', blog_id = comment.blog.id )



def hide_comments(request, comment_id):
    comment =get_object_or_404(Comment, id = comment_id)
    comment.status = 'Hidden'
    comment.save()
    blog_id = comment.blog.id
    return redirect('admin_blogview', blog_id = blog_id)
    
        

def show_comments(request, comment_id):
    comment =get_object_or_404(Comment, id = comment_id)
    comment.status = 'Visible'
    comment.save()
    blog_id = comment.blog.id
    return redirect('admin_blogview', blog_id = blog_id)   
       
def is_staff(user):
    return user.is_staff


def admin_sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None and user.is_staff:
                logout(request)
                login(request,user)
                return redirect('admin_home')
            else:
                messages.error(request, 'Invalid Usename or Password!!')
                return redirect('admin_login')    

    else:
        form = LoginForm() 
    return render(request, 'adminpanel/admin_login.html', {'form':form})

@login_required(login_url='/404/')
def resetpassword(request):
    if request.method == 'POST':
        form = AdminResetPasswordForm(user = request.user, data = request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'Your password has been updated seccessfully.')
            return redirect('admin_login')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = AdminResetPasswordForm(user = request.user) 
    return render(request, 'adminpanel/reset_password.html', {'form':form})    

@login_required(login_url='/404/')
def admin_sign_out(request):
    logout(request)
    return redirect('site_home') 