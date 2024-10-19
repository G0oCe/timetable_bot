import json
import os
import shutil
from load_html import write_schedule_to_file
from html_to_object import create_schedule


# Constants
OUTPUT_FILE_PATH = 'schedule.json'
SCHEDULES_DIR = './schedules'
FACULTY_IDS_FILE = 'faculty_ids.json'


def create_files():
    """Clears existing schedule files and creates new ones."""
    # Remove existing files and directories in the schedules folder
    if os.path.exists(SCHEDULES_DIR):
        shutil.rmtree(SCHEDULES_DIR)  # Delete existing schedules directory
    os.makedirs(SCHEDULES_DIR, exist_ok=True)  # Create a new schedules directory

    # Write new schedule files for each faculty and course
    for faculty_id in range(1, 37):  # Faculty IDs from 1 to 36
        for course in range(1, 5):  # Courses from 1 to 4
            try:
                write_schedule_to_file(faculty_id, course)  # Generate schedule file
            except Exception as e:
                print(f'Error for faculty_id: {faculty_id}, course: {course}. Reason: {e}')


def load_faculty_ids():
    """Loads faculty IDs from a JSON file and returns them as a dictionary."""
    with open(FACULTY_IDS_FILE, 'r', encoding='utf-8') as f:
        faculty_ids = json.load(f)
    return faculty_ids


def create_schedules(faculty_ids):
    """Creates schedules for each faculty and course, returns a dictionary of schedules."""
    schedules = {}  # Dictionary to hold the final schedule data

    # Create schedules for each faculty and course
    for i in range(1, 37):
        for j in range(1, 4):
            try:
                (name, schedule) = create_schedule(f'./schedules/{i}-{j}.txt')  # Get the schedule
                faculty = get_key(faculty_ids, i)  # Get the faculty key
                if faculty and faculty not in schedules:  # Check if faculty is valid and not already in schedules
                    schedules[faculty] = {}
                    schedules[faculty][name] = schedule
            except FileNotFoundError:
                print(f"File not found for faculty ID {i} and course {j}.")  # Log missing file
    return schedules


def save_schedules_to_file(schedules):
    """Saves the schedules dictionary to a JSON file."""
    # Convert schedules dictionary to a JSON object
    json_obj = json.dumps(schedules, ensure_ascii=False, indent=4)

    # Write the schedules to the output JSON file
    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(json_obj)


def get_key(d, value):
    """Returns the key corresponding to the given value in the dictionary."""
    value = str(value)  # Ensure value is a string
    for k, v in d.items():
        if v == value:
            return k
    return ""  # Return empty string if not found
