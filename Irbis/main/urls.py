from django.contrib.auth.views import *
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='main_index'),
    path("category/<str:name>", views.by_category, name='by_category'),
    path("create/category/<str:name>", views.create_category,name='create_category'),
    path("category/<str:name>/<str:search>", views.by_category, name='by_category'),
    path("category/<str:name>/detail/<int:pk>", views.detail_view, name='detail_view'),
    path("category/<str:name>/update/<int:pk>", views.update_view, name='update_view'),
    path("compose/<str:model_name>/<int:composed_id>", views.composition, name='composition'),
    path("search", views.search, name='search'),

    path('pbc/upload_files', views.upload_pcb_files, name='pbc_upload_files'),

    path("auth/login", LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path("auth/logout", LogoutView.as_view(), name='logout'),
    # path("auth/reg", views.RegisterView.as_view(), name='reg')
]