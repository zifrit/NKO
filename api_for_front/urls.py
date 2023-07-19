from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'project', views.ProjectKOViewSet)

urlpatterns = [
    path('stage/', views.CreateApiViewME.as_view()),
    path('textfield/', views.CreateTextFieldAPI.as_view()),
    path('textareafiled/', views.CreateTextareaFieldAPI.as_view()),
    path('liststage/', views.ViewListStage.as_view()),
    # path('maintableko/<int:pk>/', views.ViewMainTableKo.as_view()),
    path('list_create_main_table/', views.ListCreateMainTableKo.as_view()),
    path('create_stage/', views.CreateStage.as_view()),
    path('update_stage_info/<int:pk>/', views.AddIngoInStage.as_view()),
    path('', include(router.urls)),
]
