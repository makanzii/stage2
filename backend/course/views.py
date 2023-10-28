import openai
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import StreamingHttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from rest_framework.views import APIView
from .utils import generate_study_plan
from .models import User, Post
from .serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course, Reply, Quiz
from .serializers import CourseSerializer, PostSerializer, ReplySerializer, ReplyCreateSerializer, QuizSerializer, \
    PostCreateSerializer
from .bgtask import bg_ask_for_gpt


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(email=username).first()
        if user and user.check_password(password):
            return user
        return None


def aggregate_errors(errors_dict):
    """Aggregate Django form or serializer errors into a single string."""
    errors = []
    for field, field_errors in errors_dict.items():
        if field_errors:
            errors.append(field_errors[0])
    return {"error": ' '.join(errors)}


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # 使用 set_password 方法而不是直接修改密码字段
            user = User(**serializer.validated_data)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_message = aggregate_errors(serializer.errors)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        if not request.user.courses.filter(id=course.id).exists():
            request.user.courses.add(course)
            return Response({'message': 'Successfully joined the course.'})
        return Response({'error': 'Already joined the course.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def drop(self, request, pk=None):
        course = self.get_object()
        if request.user.courses.filter(id=course.id).exists():
            request.user.courses.remove(course)
            return Response({'message': 'Successfully left the course.'})
        return Response({'error': 'Not a member of the course.'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if 'my-courses' in request.query_params:
            self.queryset = request.user.courses.all()
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.GenericViewSet):  # 使用 GenericViewSet，因为我们只需要自定义的行为
    permission_classes = [IsAuthenticated]  # 默认为需要认证

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_info(self, request):
        user = request.user
        # 使用你的用户序列化器，这里我假设它叫 UserSerializer
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def update_info(self, request):
        user = request.user
        if request.data.get('username'):
            user.username = request.data['username']
        if request.data.get('avatar'):
            user.avatar = request.data['avatar']
        if request.data.get('password'):
            user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PostViewSet(mixins.ListModelMixin,  # 为了分页查询列表
                  mixins.RetrieveModelMixin,  # 查看post详情
                  mixins.CreateModelMixin,  # 发布post
                  mixins.DestroyModelMixin,  # 删除post
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')
        query = self.request.query_params.get('search', None)
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if "@gpt" in request.data['content']:
            bg_ask_for_gpt(serializer.instance.id)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        # 检查请求的用户是否是文章的创建者
        if post.user != request.user:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)


class QuizViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class ReplyViewSet(mixins.CreateModelMixin,  # 发布回复
                   mixins.DestroyModelMixin,  # 删除回复
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Reply.objects.all().order_by('-created_at')
    serializer_class = ReplySerializer

    def list(self, request, *args, **kwargs):
        post_id = self.request.query_params.get('post', None)
        if post_id is None:
            return Response({"error": "post parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        replies = Reply.objects.filter(post_id=post_id).order_by('-created_at')
        serializer = self.serializer_class(replies, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = ReplyCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        reply = get_object_or_404(Reply, pk=kwargs.get('pk'))
        if reply.user != request.user:
            return Response({"error": "You do not have permission to delete this reply"},
                            status=status.HTTP_403_FORBIDDEN)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class ChatView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('input', '')
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stream=True,
            messages=[
                {
                    'role': 'user',
                    'content': user_input,
                }
            ]
        )

        def get_streaming_content(chat_resp):
            for chunk in chat_resp:
                choice = chunk['choices'][0]['delta']
                if 'content' in choice:
                    yield choice['content']

        response = StreamingHttpResponse(get_streaming_content(chat_response), content_type='application/octet-stream')
        return response


class DashBoardView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        schedule = user.get_user_courses_schedule()
        today_course = user.get_today_course()
        return Response(data={"schedule": schedule, "studyPlan": user.study_plan, 'todayCourse': today_course})


class StudyPlanView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        course_name_list = []
        for course in user.courses.all():
            course_name_list.append(course.title)
        user.study_plan = generate_study_plan(course_name_list)
        user.save()
        return Response(data={"studyPlan": user.study_plan})
