from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Review)

# Courses
admin.site.register(Lesson)

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines=[LessonInline]

# Forum models
admin.site.register(ForumCategory)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)

# Quiz models
admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(QuizAttempt)

# Adding the capability to edit Question and optins all in one single adming page

class QuestionOptionInLine(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionOptionInLine
    ]
