import datetime
import logging
import os
import warnings
from pathlib import Path

import colorlog
import yaml
from dotenv import load_dotenv
from ics import Calendar, DisplayAlarm, Event, Organizer
from pydantic import ValidationError

from event_schema import EventData

# Suppress the FutureWarning from ics library
# NOTE: The warning arises in the store method and can be ignored safely
warnings.filterwarnings(
  "ignore",
  message="Behaviour of str\\(Component\\) will change in version 0.9",
  category=FutureWarning,
  module="ics",
)


class CalendarGenerator:
  def __init__(self):
    self.logger = self._get_logger_config(logging.INFO)

    self.logger.debug("Initializing CalendarGenerator")

    self.logger.debug("Loading environment variables")
    load_dotenv()

    self.posts_dir: Path = Path(os.getenv("POSTS_DIR", "../_posts"))
    self.output_ics_file: Path = Path(
      os.getenv("OUTPUT_ICS_FILE", "dotnet-regensburg.ics")
    )
    self.organizer = Organizer(
      common_name="DotNet UserGroup Regensburg", email="info@dotnet-regensburg.de"
    )
    self.talks_url: str = "https://dotnetregensburg.github.io/archive/"
    self.alarm: DisplayAlarm = DisplayAlarm(trigger=datetime.timedelta(minutes=15))

    self.logger.debug("Finished loading environment variables successfully")

  def _get_logger_config(self, level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance for the current module.

    Returns:
      logging.Logger: Configured logger instance.
    """
    log_output_handler = colorlog.StreamHandler()
    log_output_handler.setFormatter(
      colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(message_log_color)s%(message)s",  # noqa: E501
        datefmt="%H:%M:%S",
        log_colors={
          "DEBUG": "white",
          "INFO": "green",
          "WARNING": "yellow",
          "ERROR": "red",
          "CRITICAL": "bold_red,bg_white",
        },
        secondary_log_colors={
          "message": {
            "ERROR": "red",
            "CRITICAL": "bold_red,bg_white",
          }
        },
      )
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.addHandler(log_output_handler)

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
    calendar = Calendar(creator=self.organizer.common_name)

    for filename in sorted(self.posts_dir.rglob("*.md")):
      try:
        event = self._create_calendar_event(filename)
      except (ValidationError, ValueError):
        self.logger.warning(
          f"Skipping event creation for file {filename} due to validation error."
        )
        continue

      calendar.events.add(event)

    return calendar

  def _create_calendar_event(self, filename: Path) -> Event:
    """
    Creates a calendar event from the given file.

    Args:
      filename (Path): The path to the file containing event data.

    Returns:
      Event: The constructed calendar event.

    Raises:
      ValueError: If the event date is missing or None.
    """
    with open(filename, encoding="utf-8") as file:
      file_content = file.read()
      event_data = self._parse_event_data(file_content)

    if event_data.date is None:
      raise ValueError("Event date is missing or None")

    self.logger.debug(f"Parsed event data from file {filename.name}")

    # Set default event duration to 2 hours
    end_time = event_data.date.shift(hours=2)

    if (event_data.location is None) or (event_data.location.strip() == ""):
      event_data.location = "<No Location Provided>"

    event = Event(
      name=event_data.title,
      begin=event_data.date,
      end=end_time,
      location=event_data.location,
      description=self._build_description_string(event_data),
      organizer=self.organizer,
      url=self.talks_url,
      alarms=[self.alarm],
    )

    return event

  def _parse_event_data(self, file_content: str) -> EventData:
    """
    Parses event data from a file content string.

    Args:
      file_content (str): The content of the event file.

    Returns:
      EventData: The parsed EventData.

    Raises:
      ValueError: If event validation fails due to invalid or missing required fields.
    """
    file_parts = [part for part in file_content.split("---") if part.strip()]

    yaml_data = yaml.safe_load(file_parts[0]) if file_parts else {}
    try:
      event_data = EventData(**(yaml_data or {}))
    except ValidationError as e:
      for err in e.errors():
        self.logger.error(f"Event validation failed: {err['msg']}")
      raise

    if len(file_parts) < 2 and event_data.layout == "talk":
      self.logger.warning(f"Event {event_data.title} does not contain talk description")
    else:
      event_data.description = file_parts[1].strip() if len(file_parts) > 1 else ""

    return event_data

  def _build_description_string(self, event_data: EventData) -> str:
    """
    Constructs a formatted description string for an event.

    Args:
      event_data (EventData): The event data.

    Returns:
      str: A formatted multi-line string describing the event and speaker.
    """
    description_lines = []

    if event_data.description:
      description_lines.append(f"{event_data.description}\n")

    if event_data.speaker and event_data.speaker.name:
      description_lines.append(f"Speaker: {event_data.speaker.name}\n")
      if event_data.speaker.description:
        description_lines.append(f"{event_data.speaker.description}\n")

      if event_data.speaker.social:
        social_links = "\n".join(
          f"- {link.title}: {link.url}"
          for link in event_data.speaker.social
          if link.url
        )
        if social_links:
          description_lines.append(f"\nSocial Links:\n{social_links}")

    description = "\n".join(description_lines)
    return description

  def store_calendar_file(self, calendar: Calendar):
    """
    Stores the given Calendar object as an ICS file.

    Args:
      calendar (Calendar): The Calendar object to be serialized and stored.
    """
    if self.output_ics_file.exists():
      self.output_ics_file.unlink()

    with open(self.output_ics_file, "x", encoding="utf-8") as ics_file:
      ics_file.writelines(calendar.serialize())

    self.logger.info(
      f"Calendar file '{self.output_ics_file.name}' generated successfully."
    )


# Script execution
if __name__ == "__main__":
  generator = CalendarGenerator()
  calendar = generator.create_calendar()
  generator.store_calendar_file(calendar)
