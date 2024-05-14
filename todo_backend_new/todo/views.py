from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

# Create your views here.
from rest_framework import viewsets, status, generics
from .serializers import ProfileSerializer, TodoSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from .models import Todo, CustomUser

# Create your views here.


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class HomeView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Welcome to the JWT \
Authentication page using React Js and Django!'}
        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserCreate(APIView):
#     """
#     Creates the user.
#     """

#     def post(self, request, format='json'):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    """Renders a simple 'Hello, World!' HTML response for the root URL."""
    context = {'message': 'Hello, World!'}  # Pass context for dynamic content
    # Render the 'home.html' template
    return render(request, 'todo/home.html', context)


# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Register User


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# api/profile  and api/profile/update


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# api/todos


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTodos(request):

    user_todos = request.user.todos.all()
    todos = user_todos
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)
