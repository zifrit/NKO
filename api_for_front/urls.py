from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'project', views.MainProjectViewSet)
router.register(r'steps', views.ListStep)
router.register(r'links', views.LinkStepViewSet)

urlpatterns = [
    path('create-step-template-schema/', views.CreateTemplatesStep.as_view()),
    path('create-step/', views.CreateStep.as_view()),
    path('update-step_info/', views.AddInfoInStage.as_view()),
    path('', include(router.urls)),
]
