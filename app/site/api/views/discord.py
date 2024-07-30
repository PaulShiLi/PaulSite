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

from pkgs.mongo.db import Mongo
from pkgs.django.serializer import ErrorSerializer


class Status(AsyncAPIView):

    @swagger_auto_schema(operation_id="Get current status", responses={
        200: openapi.Response(
            description="Current status",
            examples={
                "application/json": {
                    "string": "string"
                }
            }),
        400: ErrorSerializer()
    })
    async def get(self, request: Request, format=None) -> Response:
        content = Mongo.find("discord", "status")[0]

        return Response(content, status=status.HTTP_200_OK)
