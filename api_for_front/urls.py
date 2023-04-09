from django.urls import path
from . import views

urlpatterns = [
    path('stage/', views.CreateApiViewME.as_view()),
    path('textfield/', views.CreateTextFieldAPI.as_view()),
    path('textareafiled/', views.CreateTextareaFieldAPI.as_view()),
    path('liststage/', views.ViewListStage.as_view()),
]
