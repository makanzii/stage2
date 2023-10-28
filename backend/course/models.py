from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from .utils import answer_forum_question
from django_jsonform.models.fields import JSONField


def get_or_create_gpt_user():
    gpt = User.objects.filter(email="gpt@gpt.com").first()
    if gpt:
        return gpt
    gpt = User.objects.create_user(email="gpt@gpt.com", username="gpt", password="gpt")
    return gpt


class User(AbstractUser):
    avatar = models.TextField(
        default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxwmlnoJbzLcou6rVQAZ1_ayDmxTKBUs4WaXJ7RmVkZg&s")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    courses = models.ManyToManyField('Course', related_name='students', blank=True)
    study_plan = models.TextField(null=True, blank=True)

    def get_user_courses_schedule(self):
        courses = self.courses.all()
        schedule = []

        for course in courses:
            # 获取课程开始和结束日期之间的所有日期
            current_date = course.start_time
            while current_date <= course.end_time:
                day_name = current_date.strftime('%A').lower()  # 获取当前日期的星期名称并转化为小写
                if getattr(course, day_name):  # 使用getattr检查该课程是否在当前日期有课
                    schedule.append({
                        'title': course.title,
                        'start': current_date
                    })
                current_date += timedelta(days=1)  # 增加一天，直到达到课程的结束日期

        return schedule

    def get_today_course(self):
        courses = self.courses.all()
        today = datetime.now().date()
        for course in courses:
            day_name = today.strftime('%A').lower()
            if getattr(course, day_name):
                return course.title
        return None

    def reply_to_post(self, post, content):
        reply = Reply(user=self, post=post, content=content)
        reply.save()

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Quiz(models.Model):
    question_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "text": {
                    "title": "Question Text",
                    "type": "string"
                },
                "options": {
                    "title": "Options",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "correctAnswer": {
                    "title": "Correct Answer",
                    "type": "string"
                }
            },
            "required": ["text", "options", "correctAnswer"]
        }
    }
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    description = models.TextField()
    questions = JSONField(schema=question_schema)
    date = models.DateField(default=datetime.now)
    participants = models.ManyToManyField(User, related_name='quizzes_participated', null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now)

    def ask_for_gpt(self):
        gpt_user = get_or_create_gpt_user()
        question = f"{self.title}\n{self.content}"
        question.replace("@gpt", "")
        answer = answer_forum_question(question)
        gpt_user.reply_to_post(self, answer)

    def __str__(self):
        return self.title


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"


class GptUsage(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.prompt

    class Meta:
        verbose_name = "GPT Usage"
        verbose_name_plural = "GPT Usages"
