import json

faculty_name_line = 32

line_starts = [50,94,138,182,226,270]
line_dist = 7
lines = []
for x in line_starts:
    temp = []
    for i in range(6):
        temp.append(x + i*line_dist)
    lines.append(temp)



schedules = {

}

def file_to_list(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    html = f.read()
    html = html.splitlines()
    f.close()
    return html

def create_schedule(input_file_path):
    html = file_to_list(input_file_path)

    name = html[faculty_name_line-1]
    name = name.removeprefix('                        ')
    name = name.removeprefix('<td class="c_rep" colspan="8" style="font-size:9px;">')
    name = name.removesuffix('</td>')

    schedule = {
        "day1": [],
        "day2": [],
        "day3": [],
        "day4": [],
        "day5": [],
        "day6": []
    }
    
    for day in range(6):
        subjects = []
        for i in lines[day]:
            line = html[i-1]
            line = line.replace('border-bottom:solid 1px grey;', '')
            line = line.removeprefix('                                        ')
            line = line.removeprefix('<td class="c_top" style="font-size:9px;"><b>')
            line = line.removesuffix('</b></td>')
            if (line == ' <br> '):
                line = ''
            subjects.append(line)
        schedule[f'day{day+1}'] = subjects
    return (name, schedule)

