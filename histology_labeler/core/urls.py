from django.urls import path
from . import views

urlpatterns = [
     
    path('', views.home, name='home'),
    path('register/', views.signup_view, name='register'),
    path('upload/', views.upload_image, name='upload'),
    path('gallery/', views.gallery, name='gallery'),
    path('slide/<int:slide_id>/', views.slide_detail, name='slide_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('slide/<int:slide_id>/annotate/', views.save_annotation, name='save_annotation'),
    path('annotation/<int:annotation_id>/delete/', views.delete_annotation, name='delete_annotation'),
    path('slide/<int:slide_id>/export_csv/', views.export_annotations_csv, name='export_annotations_csv'),
  
    path('slide/<int:slide_id>/analyze/', views.analyze_slide, name='analyze_slide'),






]
