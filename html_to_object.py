# Line number where the faculty name is located in the HTML
faculty_name_line = 32

# Starting lines for each day in the schedule
line_starts = [50, 94, 138, 182, 226, 270]
line_dist = 7  # Distance between lines for each subject

# Create a list of line indices for each day based on the starting lines and distance
lines = []
for x in line_starts:
    temp = []
    for i in range(6):
        temp.append(x + i * line_dist)
    lines.append(temp)

# Dictionary to hold schedules (if needed in the future)
schedules = {}

def file_to_list(file_path):
    """Reads a file and returns its contents as a list of lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()  # Split lines and return as a list

def create_schedule(input_file_path):
    """Creates a schedule from the provided input file."""
    html = file_to_list(input_file_path)  # Read HTML content

    # Extract faculty name from the specified line
    name = html[faculty_name_line - 1].strip()  # Get the line for faculty name
    name = name.removeprefix('<td class="c_rep" colspan="8" style="font-size:9px;">').removesuffix('</td>')  # Clean up the string

    # Initialize the schedule dictionary
    schedule = {f'day{day + 1}': [] for day in range(6)}

    # Extract subjects for each day
    for day in range(6):
        subjects = []
        for i in lines[day]:
            line = html[i - 1].replace('border-bottom:solid 1px grey;', '').strip()  # Read and clean the line
            line = line.removeprefix('<td class="c_top" style="font-size:9px;"><b>').removesuffix('</b></td>')  # Further cleanup

            # Handle specific cases for blank entries
            if line == ' <br> ':
                line = ''  # Replace HTML line breaks with empty strings
            subjects.append(line)  # Add the cleaned line to subjects

        schedule[f'day{day + 1}'] = subjects  # Assign the extracted subjects to the corresponding day in the schedule

    return name, schedule  # Return the faculty name and the complete schedule
