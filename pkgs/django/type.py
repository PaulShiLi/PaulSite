from typing import Optional
from dataclasses import dataclass, field


# Using dataclass to instantiate the classes for the API response
@dataclass
class ErrorType:
    code: int
    message: str
