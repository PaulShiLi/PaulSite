from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pkgs.common.util import util
from pkgs.django.type import ErrorType

from django.http import HttpResponse
from django.urls import path
# import urlpattern from django.urls
from django.urls.resolvers import URLPattern
from django.http import QueryDict
from typing import TypedDict, TypeVar

def mapUrl(urlMap: dict[str, dict[str, str | HttpResponse]]) -> list[URLPattern]:
    urls: list[URLPattern] = [
        path(key, val["view"].as_view(), name=val["name"]) for key, val in util.flattenDict(urlMap, separator="/").items()
    ]
    # print(util.flattenDict(urlMap, separator="/"))
    return urls
