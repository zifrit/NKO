from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'project', views.CRUDProjectViewSet)
router.register(r'steps', views.ListRetrieveStep)

urlpatterns = [
    # path('liststage/', views.ViewListStage.as_view()),
    # path('maintableko/<int:pk>/', views.ViewMainTableKo.as_view()),
    path('list_create_main_table/', views.ListCreateMainTableKo.as_view()),
    path('create_step/', views.CreateStep.as_view()),
    path('update_stage_info/<int:pk>/', views.AddInfoInStage.as_view()),
    path('', include(router.urls)),
]
