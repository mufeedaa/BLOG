from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import  Blog, Comment, Profile, User
from django.contrib import messages
from .forms import ProfileForm, BlogForm, RegistrationForm,RegistrationEditForm, CommentForm, ResetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/404/')
def userhome(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    context ={
        'logged_user':logged_user,'profile':profile
    }   
    return render(request, 'userpanel/user_home.html', context )     

@login_required(login_url='/404/')
def viewprofile(request):
    logged_user = request.user  
    profile = get_object_or_404(Profile, user = logged_user)
    context ={
        'logged_user':logged_user,'profile':profile
    }   
    return render(request, 'userpanel/view_profile.html', context )    

@login_required(login_url='/404/')
def editprofile(request):
    
    if request.method == 'POST':
        form = RegistrationEditForm(request.POST, instance=request.user)
        pro_form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid() and pro_form.is_valid():
            form.save()
            pro_form.save()
            messages.success(request, 'Your profile has been updated!!')
            return redirect('user_viewprofile')  
    else:
        form = RegistrationEditForm(instance=request.user)
        pro_form = ProfileForm(instance=request.user.profile)

    return render(request, 'userpanel/edit_profile.html', {'form': form , 'pro_form': pro_form})    
    
 
 
def logged_user_data(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    return logged_user, profile

@login_required(login_url='/404/')
def addblog(request):
    status = (
        ('PUBLISH', 'Publish'),
        ('DRAFT', 'Draft'),
    )
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    
    logged_user, profile = logged_user_data(request)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            addblog = form.save(commit = False)
            addblog.user = logged_user
            addblog.author = request.user
            # addblog.status = request.POST.get('PUBLISH', 'DRAFT')
            addblog.save()
            messages.success(request, 'Blog Added Successfully!!')
            return redirect('user_bloglist')
    else:
        form = BlogForm()
    context = {
        'logged_user': logged_user,
        'form' : form,
        'profile': profile
    }
    return render(request, 'userpanel/add_blog.html', context )            


@login_required(login_url='/404/') 
def editblog(request, blog_id):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the logged-in user is the author of the blog
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog post.")
    
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated Successfully!!')
            return redirect('user_myblog')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'userpanel/edit_blog.html', {'form': form, 'blog': blog, 'logged_user':logged_user, 'profile':profile})

@login_required(login_url='/404/')
def deleteblog(request, blog_id):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user) 
    blog = get_object_or_404(Blog, id = blog_id, author=request.user)
    # if request.method == 'POST':
    blog.delete()
    messages.success(request,'Product deleted successfully')
    return redirect('user_myblog')
    return render(request, 'userpanel/my_blogs.html', {'blog':blog, 'logged_user':logged_user, 'profile':profile})    

@login_required(login_url='/404/')
def viewblog(request, blog_id):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    # blog view
    logged_user = request.user
    blog = get_object_or_404(Blog, id = blog_id)
    
    # comment view
    comments = Comment.objects.filter(blog = blog, status = 'visible', author__is_active = True).order_by('-updated_at')
    # adding comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.blog = blog
            comment.author = logged_user 
            comment.save()
            messages.success(request, 'Comment added successfully!!!')
            return redirect('user_viewblog', blog_id = blog_id)
    else:
        form = CommentForm()        
    

    context = {'blog': blog ,
    'form': form,
    'comments':comments,
    'logged_user':logged_user,
    'profile':profile
    }
   
    return render(request, 'userpanel/view_blog.html',context )    

@login_required(login_url='/404/')
def myblog(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    blogs = Blog.objects.filter(author = request.user , status= 'PUBLISH' ).order_by('-updated_at')
    return render(request, 'userpanel/my_blogs.html', {'blogs': blogs, 'logged_user':logged_user, 'profile':profile})    

@login_required(login_url='/404/')
def draftblog(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    blogs = Blog.objects.filter(author = logged_user ,status = 'DRAFT').order_by('-created_at')
    return render(request, 'userpanel/draft_blog.html', {'blogs':blogs , 'logged_user':logged_user, 'profile':profile})

@login_required(login_url='/404/')
def publishblog(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    blogs = Blog.objects.filter(author = request.user , status = 'PUBLISH').order_by('-created_at')
    return render(request, 'userpanel/publish_blog.html', {'blogs': blogs , 'logged_user':logged_user, 'profile':profile})    

@login_required(login_url='/404/')
def bloglist(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    blogs = Blog.objects.filter(status='PUBLISH').order_by('-updated_at').filter(author__is_active = True)
    return render(request, 'userpanel/blog_list.html', {'blogs': blogs, 'logged_user':logged_user, 'profile':profile} )

@login_required(login_url='/404/')
def edit_comment(request, comment_id):
    logged_user = request.user
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    blog = get_object_or_404(Blog, id = comment.blog.id)
    comments = Comment.objects.filter(blog = blog)
    profile = get_object_or_404(Profile,  user = logged_user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully')
        else:
            messages.error(request, 'The action failed')  
            return redirect('user_viewblog', id=comment.blog.id)  
            
    else:
        form = CommentForm(instance=comment)

    context = {'blog': blog ,
    'form': form,
    'comments':comments,
    'logged_user':logged_user,
    'profile':profile
    }    
    return render(request, 'userpanel/view_blog.html',context ) 
    
@login_required(login_url='/404/')
def delete_comment(request, comment_id):
   
    logged_user = request.user
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    blog_id = comment.blog.id
    comment.delete()
    messages.success(request, 'Comment deleted')
       
    return redirect('user_viewblog', blog_id=blog_id)

    
      
@login_required(login_url='/404/')
def resetpassword(request):
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)
    if request.method == 'POST':
        form = ResetPasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your password has been updated seccessfully.')
            return redirect('site_login')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = ResetPasswordForm(user = request.user)            
    return render(request, 'userpanel/reset_password.html', {'form':form, 'logged_user':logged_user, 'profile':profile})  

@login_required(login_url='/404/')
def sign_out(request):
    logout(request)
    return redirect('site_home')    







