from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'project', views.MainProjectViewSet)
router.register(r'steps', views.Steps)
router.register(r'links', views.LinkStepViewSet)

urlpatterns = [
    path('step-filed/delete/<int:pk>/', views.DeleteStepFiled.as_view()),
    path('departments/', views.GetDepartmentView.as_view()),
    path('departments/', views.CreateDepartmentView.as_view()),
    path('departments/<int:pk>/', views.DepartmentUserView.as_view()),
    path('departments/add_users/', views.AddToDepartmentUserView.as_view()),
    path('templates/', views.ListCreateTemplatesStep.as_view()),
    path('templates/<int:pk>/', views.UpdateSchema.as_view()),
    path('templates/delete/<int:pk>/', views.DeleteSchema.as_view()),
    path('replacement-step-place/<int:pk>/', views.ReplacementPlaceStep.as_view()),
    path('', include(router.urls)),
]
