from django.urls import path
from .views import AddExtraTimeAPIView,ExtraTimeCalendarAPIView, UpdateExtraTimeAPIView, ExtraTimeRequestAPIView,DeleteTimeAPIView


urlpatterns = [
    
    path('extra-time',AddExtraTimeAPIView.as_view(),name="add-extra-time"),
    path('extra-time/<int:pk>',UpdateExtraTimeAPIView.as_view(),name="update-extra-time"),
    path('extra-time/delete/<int:pk>',DeleteTimeAPIView.as_view(),name="extra-time-delete"),
    path('extra-time/calendar',ExtraTimeCalendarAPIView.as_view(),name="extra-time-calendar"),
    path('extra-time/request',ExtraTimeRequestAPIView.as_view(),name="extra-time-request-list")
]

