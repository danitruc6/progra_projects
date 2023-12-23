from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('courses/', views.course_list, name='course_list'),
    path('course_registration/<int:course_id>/', views.course_registration, name='course_registration'),
    path('course/<int:course_id>/', views.course_page, name='course_page'),
    path('course/<int:course_id>/review/', views.create_review, name='create_review'),
    path('forum/', views.forum_category_list, name='forum_category_list'),
    path('forum/category/<int:category_id>/', views.forum_topic_list, name='forum_topic_list'),
    path('forum/topic/<int:topic_id>/', views.forum_topic_detail, name='forum_topic_detail'),
    path('forum/category/<int:category_id>/create/', views.forum_create_topic, name='forum_create_topic'),
    path('like_topic/<int:topic_id>/', views.like_topic, name='like_topic'),
    path('resources/', views.resources_page, name="resources_page"),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('submit_quiz/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
]
