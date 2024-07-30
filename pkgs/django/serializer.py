from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pkgs.django.type import ErrorType

from rest_framework_dataclasses.serializers import DataclassSerializer


class ErrorSerializer(DataclassSerializer):
    class Meta:
        dataclass = ErrorType
        fields = '__all__'