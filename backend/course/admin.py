from django.contrib import admin
from django.contrib.auth.models import Group
from background_task.models import Task,CompletedTask
from .models import User, Course, Post, Reply, Quiz


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_time', 'end_time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    search_fields = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('content',)
    list_filter = ['user', 'post', 'created_at']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description')
    list_filter = ['course', 'date']


admin.site.site_header = 'E-Class Backend'
admin.site.site_title = 'E-Class Backend'
admin.site.unregister(Group)
admin.site.unregister(Task)
admin.site.unregister(CompletedTask)