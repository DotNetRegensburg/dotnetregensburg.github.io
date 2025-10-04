import logging
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, model_validator


class SocialLink(BaseModel):
  title: str = ""
  url: Optional[HttpUrl] = None


class Speaker(BaseModel):
  name: str = ""
  description: str = ""
  social: List[SocialLink] = Field(default_factory=list)


class EventData(BaseModel):
  layout: str = ""
  date: Optional[datetime] = None
  location: str = ""
  thumbnail: str = ""
  title: str = ""
  speaker: Speaker = Field(default_factory=Speaker)
  description: str = ""

  def _check_required_fields(self) -> "EventData":
    required_fields = ["layout", "date", "location", "title"]
    missing_required = [field for field in required_fields if not getattr(self, field)]
    if missing_required:
      raise ValueError(f"Missing required event fields: {', '.join(missing_required)}")
    return self

  def _warn_optional_fields(self) -> "EventData":
    logger = logging.getLogger(__name__)
    optional_fields = ["thumbnail", "speaker"]
    for field in optional_fields:
      if not getattr(self, field):
        logger.warning(f"Optional event field '{field}' is missing or empty.")
    return self

  @model_validator(mode="after")
  def validate_event(self) -> "EventData":
    self._check_required_fields()
    self._warn_optional_fields()
    return self
