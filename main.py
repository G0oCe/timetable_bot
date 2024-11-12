from schedule_manager import create_files, load_faculty_ids, create_schedules, save_schedules_to_file
from load_html import login, logout, setup_driver
from bot import botStart

if __name__ == '__main__':
    # Setup the web driver and login
    setup_driver()
    login()  # Log into the timetable site

    # Create new schedule files
    create_files()  # Clear old files and create new ones

    # Load faculty IDs from the JSON file
    faculty_ids = load_faculty_ids()

    # Create schedules using the loaded faculty IDs
    schedules = create_schedules(faculty_ids)

    # Save the created schedules to a JSON file
    save_schedules_to_file(schedules)

    # Logout from the site
    logout() 

    # Start the bot after saving the schedules
    botStart()
