"""paul_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
# Import apps in the project
from paul_site_app import views
#import TemplateView
from django.views.generic.base import TemplateView
# Custom file path
# https://stackoverflow.com/questions/40248356/how-to-serve-a-directory-of-static-files-at-a-custom-url-in-django#:~:text=from%20django.conf%20import%20settings%20from%20django.conf.urls.static%20import%20static,path%20of%20the%20folder%20you%20want%20to%20serve.
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static

from proxy.views import proxy_view

urlpatterns = [
    path('', views.index, name='Home'),
    re_path('p/(?P<b64url>.*)', proxy_view),
    path('api/', include("api.urls")),
    path('fileKudasai/', views.fileskudasai, name='Files Desu'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('404/', views.notFound_404, name='404')
]

if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)