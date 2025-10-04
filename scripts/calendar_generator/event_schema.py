import datetime
import logging
from typing import List

import arrow
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class SocialLink(BaseModel):
  title: str = ""
  url: HttpUrl | None = None

  @field_validator("url", mode="before")
  @classmethod
  def validate_url(cls, v: HttpUrl | str | None) -> HttpUrl | None:
    if v is None:
      return None
    if isinstance(v, str):
      v = v.strip()
      if v == "" or v is None:
        return None
      try:
        http_url = HttpUrl(v)
      except ValueError:
        return None
      return http_url
    return v

class Speaker(BaseModel):
  name: str = ""
  description: str = ""
  social: List[SocialLink] = Field(default_factory=list)

  @field_validator("social", mode="before")
  @classmethod
  def parse_social_links(cls, v: List[dict] | None) -> List[SocialLink]:
    if v is None:
      return []
    if isinstance(v, list):
      safe_links = []
      for item in v:
        if isinstance(item, dict):
          safe_link = {
            "title": str(item.get("title", "")),
            "url": item.get("url"),
          }
          safe_links.append(safe_link)
      return [SocialLink(**link) for link in safe_links]
    return []


class EventData(BaseModel):
  model_config = {"arbitrary_types_allowed": True}

  layout: str = ""
  date: arrow.Arrow | None = None
  location: str = ""
  title: str = ""
  speaker: Speaker = Field(default_factory=Speaker)
  description: str | None = ""

  @field_validator("date", mode="before")
  @classmethod
  def parse_date(
    cls, v: str | datetime.datetime | arrow.Arrow | None
  ) -> arrow.Arrow | None:
    if isinstance(v, (str, datetime.datetime)):
      return arrow.get(v)
    return v

  @field_validator("layout", "location", "title", "description", mode="before")
  @classmethod
  def parse_strings(cls, v: str | None) -> str:
    if v is None:
      return ""
    return str(v)

  @field_validator("speaker", mode="before")
  @classmethod
  def parse_speaker(cls, v: str | None | dict) -> dict:
    if v is None or v == "":
      return {}
    if isinstance(v, dict):
      # Ensure nested fields are safe
      safe_speaker = {
        "name": str(v.get("name", "")),
        "description": str(v.get("description", "")),
        "social": v.get("social", []),
      }
      return safe_speaker
    return {}

  @model_validator(mode="after")
  def validate_event(self) -> "EventData":
    self._check_required_fields()
    self._warn_optional_fields()
    return self

  def _check_required_fields(self) -> "EventData":
    required_fields = ["layout", "date", "title"]
    missing_required = [field for field in required_fields if not getattr(self, field)]
    if missing_required:
      raise ValueError(
        f"Missing required event fields for event: {', '.join(missing_required)}"
      )
    return self

  def _warn_optional_fields(self) -> "EventData":
    logger = logging.getLogger("__main__")
    optional_fields = ["location", "speaker"]
    for field in optional_fields:
      if not getattr(self, field):
        logger.debug(f"Optional event field '{field}' is missing or empty.")
    return self
