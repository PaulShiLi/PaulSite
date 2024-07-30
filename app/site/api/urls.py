from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from django.conf import settings
from django.http import HttpResponse
from typing import Literal
 
from app.site.api.views import (
    spotify as spotifyView,
    discord as discordView
)
from pkgs.django.map import mapUrl
from pkgs.common.util import util


# define the router
router = routers.DefaultRouter()


urlMap: dict[
    str,
    dict[
        str,
        dict[str, dict[Literal["view", "name"], str | HttpResponse]]
        | dict[Literal["view", "name"], str | HttpResponse],
    ],
] = {
    "spotify": {
        "recent": {"view": spotifyView.Recent, "name": "Recent"},
        "medium": {"view": spotifyView.Medium, "name": "Medium Term"},
        "long": {"view": spotifyView.Long, "name": "Long Term"},
        "status": {"view": spotifyView.Current, "name": "Current Song"},
        "view": spotifyView.All,
        "name": "All Songs",
    },
    "discord": {
        "status": {
            "view": discordView.Status,
            "name": "Current Status",
        },
    }
}

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += mapUrl(
    util.flattenDict(urlMap, separator="/")
)



# urlpatterns = [
#     path('', include(router.urls)),
#     path('site/', views.site.base),
#     path('discord/', views.discord.base),
#     path('discord/status', views.discord.status),
#     path('spotify/', views.spotify.base),
#     path('spotify/status', views.spotify.status),
#     path('spotify/history', views.spotify.history),
#     path('scarlet/', views.site.scarlet),
# ]

# if settings.DEBUG:
#     urlpatterns += path('api-auth/', include('rest_framework.urls'))