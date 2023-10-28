from background_task import background

from course.models import Post


@background(schedule=2)
def bg_ask_for_gpt(postId):
    print("ask for gpt")
    post = Post.objects.get(id=postId)
    post.ask_for_gpt()
