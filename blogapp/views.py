from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlog, BlogCommentForm, EditBlog
from .models import Blog, Comment
import requests
import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')

def blogMain(request):
    blogs = Blog.objects.all()

    return render(request, 'blogMain.html', {'blogs': blogs})

def createBlog(request):

    if request.method == 'POST':
        form = CreateBlog(request.POST)

        if form.is_valid():
            form.save()
            return redirect('blogMain')
        else:
            return redirect('index')
    else:
        form = CreateBlog()
        return render(request, 'createBlog.html', {'form': form})


    # form = CreateBlog()
    #
    # return render(request, 'createBlog.html', {'form': form})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog_id=blog_id)

    if request.method == 'POST':
        comment_form = BlogCommentForm(request.POST)

        if comment_form.is_valid():
            Comment.objects.create(
                blog = blog_detail,
                comment_textfield = comment_form.cleaned_data['comment_textfield'],
                comment_user=comment_form.cleaned_data['comment_user'],
                comment_thumbnail_url=comment_form.cleaned_data['comment_thumbnail_url'],
                comment_password=comment_form.cleaned_data['comment_password'],
                comment_date=datetime.datetime.now(),
            )
            return redirect(f'/blogMain/detail/{ blog_id }')


            login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'

            client_id = '87dd2dd26d27bc7ce564c17b7153fa3d'
            redirect_uri = 'http://127.0.0.1:8000/oauth'

            login_request_uri += 'client_id=' + client_id
            login_request_uri += '&redirect_uri=' + redirect_uri
            login_request_uri += '&response_type=code'

            request.session['client_id'] = client_id
            request.session['redirect_uri'] = redirect_uri

            return redirect(login_request_uri)

        else:
            return redirect('blogMain')
    else:
        comment_form = BlogCommentForm()


    context = {
        'blog_detail': blog_detail,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'detail.html', context)

def editBlog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog_body = blog.body
    print(blog)
    print(blog_body)
    bloginfo = Blog.objects.filter(pk=blog_id)
    print(bloginfo)
    print(bloginfo[0])
    bloginfo1 = list(Blog.objects.filter(pk=blog_id).values('title', 'body'))
    print(bloginfo1)
    print(bloginfo1[0]['title'])
    blog2 = Blog.objects.all()
    print(blog2)
    blog3 = Blog.objects.values()
    print(blog3)

    if request.method == 'POST':
        if request.POST['password'] == blog.password:
            blog.title = request.POST['title']
            blog.body= request.POST['body']
            blog.password = request.POST['password']
            blog.pub_date = datetime.datetime.now()
            blog.save()
            return redirect(f'/blogMain/detail/{ blog.pk }')

        else:
            return redirect('/fail/')

    else:
        form = EditBlog(instance = blog)

    return render(request, 'editBlog.html', {'form':form, 'blog': blog})


def removeBlog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)

    if request.method == 'POST':
        if request.POST['password'] == blog.password:
            blog.delete()
            return redirect('/blogMain/')

        else:
            return redirect('/fail/')

    return render(request, 'removeBlog.html', {'blog': blog})



def oauth(request):
    code = request.GET['code']
    print('code=' + str(code))

    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"

    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    print(access_token_request_uri)

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    print(access_token)

    user_profile_info_uri = "https://kapi.kakao.com/v1/api/talk/profile?access_token="
    user_profile_info_uri += str(access_token)

    user_profile_info_uri_data = requests.get(user_profile_info_uri)
    user_json_data = user_profile_info_uri_data.json()
    nickName = user_json_data['nickName']
    profileImageURL = user_json_data['profileImageURL']
    thumbnailURL = user_json_data['thumbnailURL']

    print("nickName = " + str(nickName))
    print("profileImageURL = " + str(profileImageURL))
    print("thumbnailURL = " + str(thumbnailURL))

    return redirect('blogMain')

def fail(request):
    return render(request, 'fail.html')