from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'project', views.MainProjectViewSet)
router.register(r'steps', views.ListRetrieveStep)
router.register(r'links', views.LinkStepViewSet)

urlpatterns = [
    # path('liststage/', views.ViewListStage.as_view()),
    path('create_step_template_schema/', views.CreateTemplatesStep.as_view()),
    path('create_step/', views.CreateStep.as_view()),
    path('update_stage_info/<int:pk>/', views.AddInfoInStage.as_view()),
    path('', include(router.urls)),
]
