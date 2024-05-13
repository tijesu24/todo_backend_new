from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


@api_view(['GET'])
def home(request):
	taskobj = Task.objects.all()
	print(taskobj)
	serializer = TaskSerializer(taskobj, many=True)
	return Response({'status': 200, 'payload': serializer.data})


@api_view(['POST'])
def markCompleted(request, pk):
	try:
		instance = Task.objects.get(pk=pk)
	except Task.DoesNotExist:
		return Response(status=status.HTTP_204_NO_CONTENT)
	instance.completed = True
	instance.save()
	return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def postTask(request):
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def deleteTask(request, pk):
	try:
		instance = Task.objects.get(pk=pk)
	except Task.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	instance.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
