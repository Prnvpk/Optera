"""
URL configuration for optera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('register',views.register),
    path('shows',views.showuser),
    path('login',views.login),
    path('logout', views.logout, name='logout'),
    path('addproduct',views.addpro),
    path('viewproduct', views.viewproduct, name='viewproduct'),
    path('editproduct/<int:id>/', views.editproduct, name='editproduct'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),
    path('product',views.openproduct),
    path('productbuy/<int:id>/', views.openbuy, name='productbuy'),
    path('profile',views.openprofile),
    path('dashboard',views.dashboard),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
