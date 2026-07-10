from __future__ import annotations
from typing import Literal, Union, List, Optional

from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    location: str
    budget: Union[str, int, float]
    cuisine: Union[str, List[str]] = ""
    min_rating: float = Field(ge=0, le=5, default=0.0)
    additional_preferences: Optional[str] = None
