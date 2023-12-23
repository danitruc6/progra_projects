from django.contrib.auth.models import AbstractUser
from django.db import models
from  embed_video.fields  import  EmbedVideoField

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.URLField(max_length=200, default = "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg")
    bio = models.TextField(blank=True)
    courses = models.ManyToManyField('Course', related_name='profiles')
    profile_pic_upload = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    course_img = models.URLField(max_length=200, default = "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg")
    course_video = EmbedVideoField()

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"

# Forum models
class ForumCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category_image = models.URLField(max_length=200, default = "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg")

    def __str__(self):
        return self.name

class ForumTopic(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    topic_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
    
    def serialize(self, request=None):
        is_liked = False
        if request and request.user.is_authenticated:
            is_liked =self.topic_liked.filter(id=request.user.id).exists()
        return {
            "id": self.id,
            "author": self.user.username,
            "description": self.description,
            "timestamp": self.created_at,
            "likes": self.likes,
            "is_liked": is_liked
        }


class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} in {self.topic.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions_qty = models.IntegerField(default=1)

    def __str__(self):
        return f"Quiz for {self.course.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
    def display_options(self):
        return self.option_set.all()


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Q: {self.question.text}, A: {self.text} --> is it correct: {self.is_correct}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    attempts_left = models.IntegerField(default=2)
    
    def __str__(self):
        return str(self.quiz)
