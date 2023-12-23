from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django import forms
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Avg, Count

from .models import User, Profile, Course, ForumCategory, ForumTopic, ForumPost, Quiz, Question, Option, QuizAttempt

from .forms import ReviewForm, ForumTopicForm, ForumPostForm, ProfileForm, QuizAttemptForm
from .models import Quiz, Question, Option, QuizAttempt
from .forms import QuizAttemptForm


def index(request):
    return render(request, "academy/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Use request.POST.get() to access the 'next' parameter
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect("index")
        else:
            return render(request, "academy/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "academy/login.html")



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
            return render(request, "academy/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create a profile for the user
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "academy/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "academy/register.html")

def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    user_topics = profile.user.forumtopic_set.all().order_by('-created_at')
    num_topics = user_topics.count()
    user_posts = ForumPost.objects.filter(user=profile.user)
    num_posts = user_posts.count()

    # Fetch the total replies received for user's topics
    num_replies = 0
    for topic in user_topics:
        num_replies += topic.posts.count()

    # Fetch quiz attempts for the user
    quiz_attempts = QuizAttempt.objects.filter(user=profile.user)

    # Separate handling for GET and POST requests
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'academy/profile.html', {
        'profile': profile,
        'user_topics': user_topics,
        'num_topics': num_topics,
        'num_posts': num_posts,
        'num_replies': num_replies,
        'profile_form': form,
        'quiz_attempts': quiz_attempts,  # Pass the quiz attempts to the template
    })

@login_required
def course_list(request):
    courses = Course.objects.all().annotate(average_rating=Avg('reviews__rating'))
    
    profile = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)

    return render(request, 'academy/course_list.html', {
        'courses': courses,
        'profile': profile,
    })



@login_required
def course_registration(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        try:
            # Assuming you have a Profile model for the user
            user_profile = get_object_or_404(Profile, user=request.user)

            # Check if the user is already registered for the course
            if course in user_profile.courses.all():
                # User is already registered, so unregister them
                user_profile.courses.remove(course)
                # Return a JSON response indicating successful unregistration
                return JsonResponse({'success': True})
            else:
                # User is not registered, so register them
                user_profile.courses.add(course)
                # Return a JSON response indicating successful registration
                return JsonResponse({'success': True})
        except Exception as e:
            # Return a JSON response indicating failure and the error message
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Return the course details to the template
    context = {'course': course}
    return render(request, 'academy/course_page.html', context)


    

def course_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    average_rating = course.reviews.aggregate(Avg('rating'))['rating__avg']
    quiz = Quiz.objects.filter(course=course).first()  # Get the associated quiz

    # Get the user's quiz attempt for the course
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()

    # Initialize the ReviewForm
    form = ReviewForm()

    context = {
        'course': course,
        'average_rating': average_rating,
        'quiz': quiz,
        'quiz_attempt': attempt,
        'form': form,
    }
    return render(request, 'academy/course_page.html', context)



@login_required
def create_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            
            return redirect('course_page', course_id=course.id)
    else:
        form = ReviewForm()
    
    return render(request, 'academy/create_review.html', {'form': form, 'course': course})

# Forums views

def forum_category_list(request):
    categories = ForumCategory.objects.all()

    # Modify this to get the latest 4 topics for each category in reverse chronological order
    for category in categories:
        latest_topics = category.topics.order_by('-created_at')[:4]
        category.latest_topics = latest_topics

    return render(request, 'academy/forum/category_list.html', {'categories': categories})


def forum_topic_list(request, category_id):
    category = get_object_or_404(ForumCategory, id=category_id)
    topics = category.topics.all()
    return render(request, 'academy/forum/topic_list.html', {'category': category, 'topics': topics})


def forum_topic_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    posts = topic.posts.all()

    # Incrementing views each time the topic it's acccesedo
    topic.views +=1
    topic.save()

    # Serializing the topic
    serialized_topic = topic.serialize(request)

    # getting the profile pictures for tipic and each post
    topic_profile = Profile.objects.get(user=topic.user)
    topic_profile_pic =topic_profile.profile_pic_upload
    
    posts_with_profile_pic = []
    for post in posts:
        user_profile = Profile.objects.get(user=post.user)
        posts_with_profile_pic.append((post, user_profile.profile_pic_upload))

    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.user = request.user
            post.save()
            return redirect('forum_topic_detail', topic_id=topic_id)
    else:
        form = ForumPostForm()

    return render(request, 'academy/forum/topic_detail.html', {
        'topic': topic, 
        'posts': posts_with_profile_pic, 
        'form': form, 
        'serialized_topic':serialized_topic,
        'topic_profile_pic': topic_profile_pic,
        })

@login_required
def forum_create_topic(request, category_id):
    category = get_object_or_404(ForumCategory, id=category_id)
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.user = request.user
            topic.save()
            return redirect('forum_topic_detail', topic_id=topic.id)
    else:
        form = ForumTopicForm()
    return render(request, 'academy/forum/create_topic.html', {'category': category, 'form': form})

@login_required
def like_topic(request, topic_id):
    if request.method == 'POST':
        topic = ForumTopic.objects.get(pk=topic_id)
        user = request.user

        if topic.topic_liked.filter(id=user.id).exists():
            # Unlike the topic
            topic.topic_liked.remove(user)
            topic.likes -= 1
            is_liked = False
        else:
            # Like the topic
            topic.topic_liked.add(user)
            topic.likes += 1
            is_liked = True

        topic.save()

        return JsonResponse({'success': True, 'likes_count': topic.likes, 'is_liked': is_liked})

    return JsonResponse({'success': False})

def resources_page(request):
    return render(request, 'academy/resources.html')


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()

    if attempt and attempt.attempts_left == 0:
        return render(request, 'academy/quiz_finished.html', {'quiz': quiz, 'score': attempt.score})

    if request.method == 'POST':
        user_scores = []
        for question in questions:
            user_option_id = request.POST.get(f'question_{question.id}')
            if user_option_id:
                user_option = Option.objects.filter(id=user_option_id, question=question).first()
                if user_option.is_correct:
                    user_scores.append(1)

        total_score = sum(user_scores)
        if not attempt:
            attempt = QuizAttempt(user=request.user, quiz=quiz, score=total_score, attempts_left=1)
        else:
            attempt.score = max(attempt.score, total_score)
            attempt.attempts_left -= 1
        attempt.save()

        return redirect('quiz_result', quiz_id=quiz_id)

    return render(request, 'academy/take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()
    
    if attempt:
        total_questions = quiz.questions_qty
        percentage_score = (attempt.score / total_questions) * 100 if total_questions > 0 else 0

        return render(request, 'academy/quiz_result.html', {'quiz': quiz, 'percentage_score': percentage_score})
    else:
        return render(request, 'academy/quiz_result.html', {'quiz': quiz, 'percentage_score': 0})


@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = int(request.POST.get('score', 0))
        print(request)
        print(f"The score is {score}")

        attempt, created = QuizAttempt.objects.get_or_create(user=request.user, quiz=quiz)
        if score > attempt.score:
            attempt.score = score
            attempt.attempts_left -= 1
            attempt.save()

        return JsonResponse({'redirect_url': reverse('quiz_result', args=[quiz_id])})
