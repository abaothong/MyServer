from abaoblog.forms import PostForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework.authtoken.models import Token

__author__ = 'haoyi'

from abaoblog.api.serializers import PostSerializers
from abaoblog.models import Post
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from setuptools.compat import unicode


@api_view(['POST'])
def token(request, format=None):
    username = request.POST["username"]
    password = request.POST["password"]

    login_user = authenticate(username=username, password=password)
    login(request, login_user)

    token = Token.objects.get_or_create(user=request.user)
    content = {
        'token': unicode(token),
    }
    return Response(content)





class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

    @api_view(['GET'])
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def api_post_list(request, format=None):
        if request.method == 'GET':
            posts = Post.objects.all()
            serializer = PostSerializers(posts, many=True)
            content = {
                'result': unicode("200"),
                'items': unicode(serializer.data),
            }
            return Response(content)

        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return JSONResponse(serializer.data)

    @api_view(['POST'])
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def api_post(request, format=None):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            content = {
                'result': unicode("200"),
                'message': unicode("Success"),
            }
        else:
            content = {
                'result': unicode("400"),
                'message': unicode("fail"),
                'auth': unicode(request.auth),
            }
        return Response(content)