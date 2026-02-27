from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from furniture import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.product_list, name='product_list'),
    path('dashboard/add/', views.product_add, name='product_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)