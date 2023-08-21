from django.urls import path
from .views import TodoListViewsList,TodoListViewsCreate,TodoListRelatedViews


urlpatterns = [

    path('',TodoListViewsList.as_view(),name="retrieve-stickynotes"),
    path('create/',TodoListViewsCreate.as_view(),name="create-stickynotes"),
    path('update/<int:pk>/',TodoListRelatedViews.as_view(),name="update-stickynotes"),
    path('delete/<int:pk>/',TodoListRelatedViews.as_view(),name="delete-stickynotes"),
    
]

