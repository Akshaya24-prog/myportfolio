from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('resume/', views.download_resume, name='download_resume'),
    path('api/admin/login/', views.api_admin_login, name='api_admin_login'),
    path('api/admin/logout/', views.api_admin_logout, name='api_admin_logout'),
    path('api/admin/skills/add/', views.api_add_skill, name='api_add_skill'),
    path('api/admin/skills/<int:pk>/delete/', views.api_delete_skill, name='api_delete_skill'),
    path('api/admin/projects/add/', views.api_add_project, name='api_add_project'),
    path('api/admin/projects/<int:pk>/delete/', views.api_delete_project, name='api_delete_project'),
    path('api/admin/bio/update/', views.api_update_bio, name='api_update_bio'),
    path('api/admin/education/add/', views.api_add_education, name='api_add_education'),
    path('api/admin/education/<int:pk>/edit/', views.api_edit_education, name='api_edit_education'),
    path('api/admin/education/<int:pk>/delete/', views.api_delete_education, name='api_delete_education'),
]
