from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Todo


class TodoListApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = ["id", "user", "title", "description", "completed"]

    def get(self, request):
        qs = Todo.objects.get_for_user(user=request.user)
        serializer = self.OutputSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = ["title", "description", "completed"]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Todo.objects.create(user=request.user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class TodoUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = ["title", "description", "completed"]

    def put(self, request, id):

        instance = get_object_or_404(Todo, user=request.user, pk=id)
        serializer = self.InputSerializer(
            instance=instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        Todo.objects.update(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class TodoDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        instance = get_object_or_404(Todo, user=request.user, pk=id)
        instance.delete()

        return Response(status=status.HTTP_200_OK)
