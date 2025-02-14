from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import PostForm

from .models import Post
from .serializers import PostsListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def posts_list(request):
    posts = Post.objects.all()
    serializer = PostsListSerializer(posts, many=True)
    
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
def create_post(request):
    text = request.data.get("text")

    if not text:
        return JsonResponse({"error": {"text": "This field is required."}}, status=400)

    form = PostForm({"text": text})  # Pass a dictionary to the form

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        errors = {field: form.errors[field].as_text() for field in form.errors}
        return JsonResponse({'error': errors}, status=400)