import logging
import os
import sys
from pathlib import Path

import arrow
import yaml
from dateutil import tz
from dotenv import load_dotenv
from ics import Calendar, Event

from event_schema import EventData


class CalendarGenerator:
  def __init__(self):
    self.logger = self._get_logger_config()

    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables and validate they are not empty
    env_posts_dir = os.getenv("POSTS_DIR")
    env_output_ics_file = os.getenv("OUTPUT_ICS_FILE")

    if not env_posts_dir or str(env_posts_dir).strip() == "":
      self.logger.error("POSTS_DIR environment variable is not set or empty")
      sys.exit(1)

    if not env_output_ics_file or str(env_output_ics_file).strip() == "":
      self.logger.error("OUTPUT_ICS_FILE environment variable is not set or empty")
      sys.exit(1)

    self.posts_dir: str = env_posts_dir
    self.output_ics_file: str = env_output_ics_file

  def _get_logger_config(self) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file logging (uncomment to enable)
    # file_handler = logging.FileHandler('calendar_generator.log')
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger

  def create_calendar(self) -> Calendar:
    """
    Creates a Calendar object populated with events.

    Iterates through all markdown (*.md) files found recursively in the specified posts
    directory, creates an event entry for each file, and adds it to the calendar.

    Returns:
      Calendar: A Calendar object containing all generated events.
    """
    calendar = Calendar()

    for filename in Path(self.posts_dir).rglob("*.md"):
      event = self._create_calendar_event(filename)
      calendar.events.add(event)

    return calendar

  def _create_calendar_event(self, filename: Path) -> Event:
    with open(filename, encoding="utf-8") as file:
      file_content = file.read()
      event_data = self._parse_event_data(file_content)

    if event_data.date is None:
      self.logger.error("Event date is missing or None")
      sys.exit(1)

    begin_time = arrow.get(event_data.date)
    end_time = begin_time.shift(hours=1, minutes=30)  # Default duration of 1.5 hours

    event = Event(
      name=event_data.title,
      begin=begin_time,
      end=end_time,
      location=event_data.location,
      description=event_data.description,
    )

    return event

  def _parse_event_data(self, file_content: str) -> EventData:
    file_parts = [part for part in file_content.split("---") if part.strip()]

    yaml_data = yaml.safe_load(file_parts[0]) if file_parts else {}
    try:
      event_data = EventData(**(yaml_data or {}))
    except ValueError as e:
      self.logger.error(f"Event validation failed: {e}")
      sys.exit(1)

    if len(file_parts) < 2 and event_data.layout == "talk":
      self.logger.warning(f"Event {event_data.title} does not contain talk description")
    else:
      event_data.description = file_parts[1].strip() if len(file_parts) > 1 else ""

    self.logger.debug("Parsed event data from file")

    return event_data


# Example usage
if __name__ == "__main__":
  generator = CalendarGenerator()
  generator._parse_event_data(
    open(Path("../_posts/2025-11-20-avalonia.md"), encoding="utf-8").read()  # noqa: SIM115
  )
  # calendar = generator.create_calendar()
