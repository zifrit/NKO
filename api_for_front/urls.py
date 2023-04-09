from django.urls import path
from . import views

urlpatterns = [
    path('stage/', views.CreateApiViewME.as_view()),
    path('textfield/', views.CreateTextFieldAPI.as_view()),
    path('textareafiled/', views.CreateTextareaFieldAPI.as_view()),
    path('liststage/', views.ViewListStage.as_view()),
    path('maintableko/<int:pk>/', views.ViewMainTableKo.as_view()),
    path('create_main_table/', views.CreateMainTableKo.as_view()),
    path('create_stage/', views.CreateStage.as_view()),
    path('update_stage_info/<int:pk>/', views.AddIngoInStage.as_view()),
]
