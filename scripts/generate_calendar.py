import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from ics import Calendar, Event


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
    event = Event()
    with open(filename, encoding="utf-8") as file:
      file_content = file.read()
      file_parts = file_content.split("---")

      # TODO: Parse file to yaml, check if it's layout is 'talk', create event
      if len(file_parts) <= 2:
        self.logger.warning(f"File {filename} does not contain talk description.")

      event.name = filename.stem
      # Add more event details here as needed
    return event


# Example usage
if __name__ == "__main__":
  generator = CalendarGenerator()
  calendar = generator.create_calendar()
