from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from django.views.decorators.http import require_POST, require_http_methods

from .models import User, Post, Follow 

# def index(request):
#     posts = Post.objects.all().order_by('-timestamp')
#     print(posts)
#     return render(request, "network/index.html", {
#         "posts": posts
#     })



def index(request):
    # Retrieve all posts ordered by timestamp
    posts = Post.objects.all().order_by('-timestamp')

    # Create a Paginator object with a page size of 10
    paginator = Paginator(posts, 10)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page_number)

    # Create a list to hold serialized posts
    serialized_posts = []

    # Iterate over the posts in the current page and serialize them
    for post in page_obj:
        serialized_post = post.serialize(request)
        serialized_posts.append(serialized_post)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "serialized_posts": serialized_posts
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(content=content, user=user)
        post.save()

    return redirect("index")

# enable the following line if you want that a user should be signed in to view the profile of any user
# @login_required(login_url='login')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    num_followers = Follow.objects.filter(following=user).count()
    num_followings = Follow.objects.filter(follower=user).count()

    follow_obj = None
    if request.user.is_authenticated and request.user != user:
        follow_obj = Follow.objects.filter(follower=request.user, following=user).first()

    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create a list to hold serialized posts
    serialized_posts = []

    # Iterate over the posts in the current page and serialize them
    for post in page_obj:
        serialized_post = post.serialize(request)
        serialized_posts.append(serialized_post)

    return render(request, 'network/profile.html', {
        'profile_user': user,
        'num_followers': num_followers,
        'num_followings': num_followings,
        'follow_obj': follow_obj,
        "page_obj": page_obj,
        "serialized_posts": serialized_posts
    })

 
 # replease this function to not use username instead of following_id
    
@login_required
def follow(request):
    if request.method == 'POST':
        following_id = request.POST.get('following')
        print(f' the following id is {following_id}')
        try:
            following = User.objects.get(id=following_id)
            follow_obj = Follow.objects.filter(follower=request.user, following=following).first()
            
            
            print(f' the user following object is is {following}')
            print(f' the following object is is {follow_obj}')
            
            if follow_obj is None:
                # Follow object doesn't exist, so create a new one
                follow_obj = Follow.objects.create(follower=request.user, following=following)
            else:
                # Follow object exists, so delete it
                follow_obj.delete()
            return HttpResponseRedirect(reverse('profile', args=[following.username]))
        except User.DoesNotExist:
            return HttpResponseBadRequest("Invalid user id")
    else:
        return HttpResponseBadRequest("Invalid request method")

# use this if you want to use username insteac of following_id
# @login_required
# def follow(request):
#     if request.method == 'POST':
#         following_username = request.POST.get('following_username')
#         try:
#             following = User.objects.get(username=following_username)
#             follow_obj = Follow.objects.filter(follower=request.user, following=following).first()
#             if follow_obj is None:
#                 # Follow object doesn't exist, so create a new one
#                 follow_obj = Follow.objects.create(follower=request.user, following=following)
#             else:
#                 # Follow object exists, so delete it
#                 follow_obj.delete()
#             return HttpResponseRedirect(reverse('profile', args=[following_username]))
#         except User.DoesNotExist:
#             return HttpResponseBadRequest("Invalid user id")
#     else:
#         return HttpResponseBadRequest("Invalid request method")


        
@login_required
def unfollow(request, username):
    try:
        following_user = User.objects.get(username=username)
        follow_obj = Follow.objects.get(follower=request.user, following=following_user)
        follow_obj.delete()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid user id")
    except Follow.DoesNotExist:
        return HttpResponseBadRequest("You are not following this user.")


@login_required
def following_posts(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create a list to hold serialized posts
    serialized_posts = []

    # Iterate over the posts in the current page and serialize them
    for post in page_obj:
        serialized_post = post.serialize(request)
        serialized_posts.append(serialized_post)

    return render(request, 'network/following.html', {
        'page_obj': page_obj,
        "serialized_posts": serialized_posts
    })




@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        # Get the edited content from the JSON data
        data = json.loads(request.body)
        edited_content = data.get('edited_content')
        
        # Update the post's content and save it
        post.content = edited_content
        post.save()
        
        return JsonResponse({'success': True, 'content': post.content})
    else:
        post.editing = True
        post.save()
        return JsonResponse({'message': 'Editing mode enabled'})

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        user = request.user

        if post.post_liked.filter(id=user.id).exists():
            # Unlike the post
            post.post_liked.remove(user)
            post.likes -= 1
            is_liked = False
        else:
            # Like the post
            post.post_liked.add(user)
            post.likes += 1
            is_liked = True

        post.save()

        return JsonResponse({'success': True, 'likes_count': post.likes, 'is_liked': is_liked})

    return JsonResponse({'success': False})