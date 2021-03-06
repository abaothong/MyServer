from abaoblog.forms import PostForm
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token

__author__ = 'haoyi'

from abaoblog.api.serializers import PostSerializers
from abaoblog.models import Post
from django.http import HttpResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# email
from django.core.mail import EmailMessage

@api_view(['POST'])
def token(request):
    username = request.POST["username"]
    password = request.POST["password"]

    login_user = authenticate(username=username, password=password)
    if login_user is not None:
        if login_user.is_active:
            token = Token.objects.get_or_create(user=login_user)
            content = {
                'status_code': "200",
                'message': "Success",
                'result': token[0].key,
            }

        else:
            content = {
                'status_code': "400",
                'message': "user inactive",
            }
    else:
        content = {
            'status_code': "400",
            'message': "username or password error",
        }

    return Response(content)


@api_view(['POST','GET'])
def send_email(request):
    email = EmailMessage('title', 'body', to=['thonghaoyi@gmail.com'])
    result = email.send()
    content = {
            'status_code': "200",
            'message': result,
        }

    return Response(content)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

    def __unicode__(self):
        return u'%s' % (self)

    @api_view(['GET'])
    # @authentication_classes((TokenAuthentication,))
    # @permission_classes((IsAuthenticated,))
    def api_post_list(request, format=None):
        if request.method == 'GET':
            posts = Post.objects.all()
            serializer = PostSerializers(posts, many=True)
            content = {
                'result': "200",
                'items': serializer.data,
            }
            return Response(content)

        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return JSONResponse(serializer.data)

    @api_view(['POST'])
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def api_post(request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            content = {
                'status_code': "200",
                'message': "Success",
            }
        else:
            content = {
                'result': "400",
                'message': "fail",
            }
        return Response(content)