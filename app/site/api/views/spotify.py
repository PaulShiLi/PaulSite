from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drfasyncview import AsyncAPIView
from dataclasses import asdict
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from pkgs.spotify.spotify import spotifyDb
from pkgs.django.serializer import ErrorSerializer

spClient = spotifyDb()

class Recent(AsyncAPIView):

    @swagger_auto_schema(operation_id="Get all Recent Songs", responses={
        200: openapi.Response(
            description="All Recent Songs",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        content = spClient.recentlyPlayed("short_term")

        return Response(content, status=status.HTTP_200_OK)

class Medium(AsyncAPIView):

    @swagger_auto_schema(operation_id="Get all Medium Term Songs", responses={
        200: openapi.Response(
            description="All Medium Term Songs (~ 6 Months)",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        content = spClient.recentlyPlayed("medium_term")

        return Response(content, status=status.HTTP_200_OK)

class Long(AsyncAPIView):
    
    @swagger_auto_schema(operation_id="Get all Long Term Songs", responses={
        200: openapi.Response(
            description="All Long Term Songs (~ 1 Year)",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        content = spClient.recentlyPlayed("long_term")

        return Response(content, status=status.HTTP_200_OK)

class Current(AsyncAPIView):

    @swagger_auto_schema(operation_id="Get Current Song", responses={
        200: openapi.Response(
            description="Current Song",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        content = spClient.recentlyPlayed("current")[0]

        return Response(content, status=status.HTTP_200_OK)

class All(AsyncAPIView):

    @swagger_auto_schema(operation_id="Get All Songs", responses={
        200: openapi.Response(
            description="All Songs",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        history = {
            "recents": spClient.recentlyPlayed("short_term"),
            "mediumTerm": spClient.recentlyPlayed("medium_term"),
            "longTerm": spClient.recentlyPlayed("long_term"),
            "status": spClient.recentlyPlayed("current")[0]
        }

        return Response(history, status=status.HTTP_200_OK)