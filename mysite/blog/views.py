from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blog.models import Blog, Post, Tag, Comments
from django.utils import timezone
import re
from xml.sax.saxutils import unescape

def index(request):
    most_popular_blog = Blog.objects.order_by('-view_track')[:5]
    most_popular_post = Post.objects.order_by('-view_track')[:5]
    context = {'most_popular_blog': most_popular_blog, 'most_popular_post': most_popular_post}
    return render(request, 'blog/index.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def register(request):
    return render(request, 'blog/register.html')

def reg_result(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username, password=password)
    except:
        message = "Unexpected error:  Username already exits"
        return render(request, 'blog/reg_result.html', {
            'message': message,
        })
    else:
        message = "success"
        return render(request, 'blog/reg_result.html', {
            'message': message,
        })

def login(request):
    if request.user.is_authenticated():
        username = request.user.username
        return render(request, 'blog/login_result.html', {'username': username})
    else:
        return render(request, 'blog/login.html')

def login_result(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            username = request.user.username
            return render(request, 'blog/login_result.html', {'username': username})
        else:
            return render(request, 'blog/login_result.html', {
            'error_message': "disabled account.",
            })
    else:
        return render(request, 'blog/login_result.html', {
            'error_message': "Invalid login.",
        })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('blog:logout_result'))

def logout_result(request):
    username = request.user.username
    return render(request, 'blog/logout_result.html', {'username': username})

def blogs(request, blog_id, page_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.view_track += 1
    blog.save()
    num_posts = blog.post_set.all().count()
    if num_posts%10:
        num_pages = num_posts/10
    else:
        num_pages = num_posts/10 - 1
    no = int(page_id)
    next = no + 1
    prev = no - 1
    if num_pages == no:
        postlist = blog.post_set.all().order_by('-mod_date')[no*10:]
    else:
        postlist = blog.post_set.all().order_by('-mod_date')[no*10:no*10+10]
    return render(request, 'blog/blogs.html', {'blog':blog, 'postlist': postlist, 'page_id':no, 'next':next, 'prev':prev,'num_pages':num_pages, 'num_posts': num_posts})

def posts(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.view_track += 1
    post.save()
    return render(request, 'blog/posts.html', {'post': post})

def tags(request, tag_id, page_id):
    the_tag = get_object_or_404(Tag, pk=tag_id)
    taglist = Tag.objects.filter(name=the_tag.name)
    allpostlist = []
    for t in taglist:
        allpostlist.append(t.post)
    num_posts = len(allpostlist)
    if num_posts%10:
        num_pages = num_posts/10
    else:
        num_pages = num_posts/10 - 1
    no = int(page_id)
    next = no + 1
    prev = no - 1
    for i in range(0,len(allpostlist)):
        for j in range(i,len(allpostlist)):
            if allpostlist[i].mod_date < allpostlist[j].mod_date:
                temp = allpostlist[i]
                allpostlist[i] = allpostlist[j]
                allpostlist[j] = temp
    if num_pages == no:
        postlist = allpostlist[no*10:]
    else:
        postlist = allpostlist[no*10:no*10+10]
    return render(request, 'blog/tags.html', {'the_tag':the_tag, 'postlist': postlist, 'page_id':no, 'next':next, 'prev':prev,'num_pages':num_pages, 'num_posts': num_posts})

def myblogs(request):
    if request.user.is_authenticated():
        username = request.user.username
        bloglist = Blog.objects.filter(user_id = request.user.id)
        return render(request, 'blog/myblogs.html', {'bloglist': bloglist, 'username': username})
    else:
        return render(request, 'blog/login.html')

def addnewblog(request):
    if request.user.is_authenticated():
        return render(request, 'blog/addnewblog.html')
    else:
        return render(request, 'blog/login.html')

def addblog_result(request):
    blogname = request.POST['blogname']
    b = Blog(user=request.user, name=blogname, cre_date=timezone.now(), view_track=0)
    b.save()
    return render(request, 'blog/addblog_result.html')

def rmblog(request, blog_id):
    b = Blog.objects.get(id = blog_id)
    if request.user.id == b.user.id:
        b.delete()
        return HttpResponse("This blog's been removed.  Please click back button.")
    else:
        return HttpResponse("You are not the owner of the blog.  Please go back and modify your own blog.")

def addnewpost(request, blog_id):
    b = Blog.objects.get(id = blog_id)
    if request.user.id == b.user.id:
        return render(request, 'blog/addnewpost.html', {'blog_id': blog_id})
    else:
        return HttpResponse("You are not the owner of the blog.  Please go back and modify your own blog.")

def addpost_result(request):
    title = request.POST['title']
    body = request.POST['body']
    body = re.sub(r'(http://\S+)', r'<a href="\1">\1</a>', body)
    body = re.sub(r'(https://\S+)', r'<a href="\1">\1</a>', body)
    blogID = request.POST['blogID']
    b = Blog.objects.get(pk = blogID)
    p = b.post_set.create(title=title, body=body, pub_date=timezone.now(), mod_date=timezone.now(), view_track=0)
    return render(request, 'blog/addpost_result.html', {'blog_id': blogID})

def rmpost(request, post_id):
    p = Post.objects.get(id = post_id)
    if request.user.id == p.blog.user.id:
        p.delete()
        return HttpResponse("This post's been removed.  Please click back button.")
    else:
        return HttpResponse("You are not the owner of the post.  Please go back and modify your own blog.")

def addnewtag(request, post_id):
    p = Post.objects.get(id = post_id)
    if request.user.id == p.blog.user.id:
        return render(request, 'blog/addnewtag.html', {'post_id': post_id})
    else:
        return HttpResponse("You are not the author of the post.  Please go back and modify your own blog.")

def addtag_result(request, post_id):
    name = request.POST['name']
    postID = request.POST['postID']
    p = Post.objects.get(pk = postID)
    t = p.tag_set.create(name=name)
    return render(request, 'blog/addtag_result.html', {'post_id':postID})

def rmtag(request, tag_id):
    t = Tag.objects.get(id = tag_id)
    if request.user.id == t.post.blog.user.id:
        t.delete()
        return HttpResponse("This tag's been removed.  Please click back button.")
    else:
        return HttpResponse("You are not the owner of the post.  Please go back and modify your own blog.")

def editpost(request, post_id):
    p = Post.objects.get(id = post_id)
    blog_id = p.blog.id
    body = str(p.body)
    body = re.sub(r'<a href="(http://\S+)"\S+</a>', r'\1', body)
    body = re.sub(r'<a href="(https://\S+)"\S+</a>', r'\1', body)
    if request.user.id == p.blog.user.id:
        return render(request, 'blog/editpost.html', {'post': p, 'body': body})
    else:
        return HttpResponse("You are not the author of the post.  Please go back and modify your own blog.")

def editpost_result(request):
    title = request.POST['title']
    body = request.POST['body']
    body = re.sub(r'(http://\S+)', r'<a href="\1">\1</a>', body)
    body = re.sub(r'(https://\S+)', r'<a href="\1">\1</a>', body)
    postID = request.POST['postID']
    p = Post.objects.get(pk = postID)
    p.mod_date = timezone.now()
    p.title = title
    p.body = body
    p.save()
    return render(request, 'blog/editpost_result.html', {'post': p})