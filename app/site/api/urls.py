# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

from django.conf import settings


# import everything from views
from api import views
 
# define the router
router = routers.DefaultRouter()

# router.register(r'view/site_api', views.API_ViewSet)

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('site/', views.site.base),
    path('discord/', views.discord.base),
    path('discord/status', views.discord.status),
    path('spotify/', views.spotify.base),
    path('spotify/status', views.spotify.status),
    path('spotify/history', views.spotify.history),
]

# if settings.DEBUG:
#     urlpatterns += path('api-auth/', include('rest_framework.urls'))