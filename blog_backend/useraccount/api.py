from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserDetailSerializer, UsersListSerializer
from django.core.files.storage import default_storage
import os

def validate_image(file):
    # Maximum file size - 5MB
    MAX_SIZE = 5 * 1024 * 1024
    
    if file.size > MAX_SIZE:
        raise ValueError("File size cannot exceed 5MB")
    
    # Valid file extensions
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValueError("Invalid file type")

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def author_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = UserDetailSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_detail(request, pk):
    try:
        # Ensure user can only edit their own profile
        if str(request.user.pk) != pk:
            return JsonResponse({'error': 'Not authorized'}, status=403)
            
        user = request.user
        
        if request.method == 'GET':
            serializer = UserDetailSerializer(user, many=False)
            return JsonResponse(serializer.data, safe=False)
            
        elif request.method == 'PUT':
            if 'name' in request.data:
                try:
                    user.update_name(request.data['name'])
                except ValueError as e:
                    return JsonResponse({'error': str(e)}, status=400)
            
            if 'avatar' in request.FILES:
                try:
                    user.update_avatar(request.FILES['avatar'])
                except ValueError as e:
                    return JsonResponse({'error': str(e)}, status=400)
            
            serializer = UserDetailSerializer(user, many=False)
            return JsonResponse(serializer.data, safe=False)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manager_detail(request, pk):
    try:
        # Ensure the requesting user is a staff member
        if not request.user.is_staff:
            return JsonResponse({'error': 'Only staff members can update the is_staff field'}, status=403)
        
        # Extract the is_staff value from the request data
        # user_id = request.data.get('id')
        is_staff = request.data.get('is_staff')
        
        # Fetch the target user
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Update the is_staff field
        target_user.is_staff = is_staff
        target_user.save()
        
        # Return the updated user data
        serializer = UserDetailSerializer(target_user, many=False)
        return JsonResponse(serializer.data, safe=False)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def users_list(request):
    users = User.objects.all()
    serializer = UsersListSerializer(users, many=True)
    
    return JsonResponse({
        'data': serializer.data
    })