from django.urls import path

from .views import TodoListApi, TodoCreateApi, TodoUpdateApi, TodoDeleteApi

urlpatterns = [
    path("list/", TodoListApi.as_view(), name="todo-list"),
    path("create/", TodoCreateApi.as_view(), name="todo-create"),
    path("update/<int:id>/", TodoUpdateApi.as_view(), name="todo-update"),
    path("delete/<int:id>/", TodoDeleteApi.as_view(), name="todo-delete"),
]
