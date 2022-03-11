from django.urls import path
from user import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path("all/", views.ListUserAPIView.as_view(), name="user_all"),
    path("get/<int:id>/", views.UserView.as_view(), name="user"),
    path("create/", views.UserAddView.as_view(), name="user_create"),
    path("add-property/", views.UserPropertyAddView.as_view(), name="user_add_property"),
    path("update/<int:pk>/", views.UpdateUserAPIView.as_view(), name="update_user"),
    path("delete/<int:pk>/", views.DeleteUserAPIView.as_view(), name="delete_user")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
