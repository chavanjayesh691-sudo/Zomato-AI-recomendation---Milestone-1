from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Restaurant(BaseModel):
    id: str
    name: str
    location: str
    cuisines: List[str]
    rating: float
    cost_for_two: int
    votes: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None
