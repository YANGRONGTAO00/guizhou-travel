from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("spots/", views.SpotListView.as_view(), name="spot_list"),
    path("spots/add/", views.SpotCreateView.as_view(), name="spot_add"),
    path("spots/<int:pk>/", views.SpotDetailView.as_view(), name="spot_detail"),
    path("spots/<int:pk>/delete/", views.SpotDeleteView.as_view(), name="spot_delete"),
]
