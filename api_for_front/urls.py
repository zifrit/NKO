from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'projects', views.MainKoViewSet)
router.register(r'projects/templates', views.TemplateMainKo)
router.register(r'schema-steps', views.SchemaSteps)
router.register(r'links', views.LinkStepViewSet)
router.register(r'templates', views.TemplatesStep)
router.register(r'departments_v2', views.Departments)

urlpatterns = [
    path('steps/user-steps/', views.ListUserStep.as_view(), name='user-steps'),
    path('steps/<int:pk>/', views.RetrieveStep.as_view(), name='user-steps'),
    # path('projects/templates/', views.TemplateMainKo.as_view(), name='list-create-projects-templates'),
    # path('projects/templates/<int:pk>/', views.TemplateMainKo.as_view(), name='list-create-projects-templates'),
    path('departments/', views.GetDepartmentView.as_view(), name='get_departments'),
    path('departments/create/', views.CreateDepartmentView.as_view(), name='post_departments'),
    path('departments/<int:pk>/', views.DepartmentUserView.as_view(), name='users_in_departments'),
    path('departments/delete/<int:pk>/', views.DeleteDepartmentView.as_view(), name='delete_departments'),
    path('departments/add_or_remove_users/', views.AddToDepartmentUserView.as_view(),
         name='add_or_remove_users_in_departments'),
    path('replacement-step-place/<int:pk>/', views.ReplacementPlaceStep.as_view(), name='replacement_step_place'),
    path('responsible-step-users/<int:pk>/', views.SetGetWhoResponsibleStep.as_view(), name='responsible_step_users'),
    path('step-by-step/<int:pk>/', views.StepByStep.as_view(), name='step_by_step'),
    path('step-files/<int:pk>/', views.FilesView.as_view(), name='step_files'),
    path('step-files/', views.FilesCreate.as_view(), name='step_files'),
    path('', include(router.urls)),
]
