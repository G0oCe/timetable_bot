import json
from html_to_object import create_schedule
from tmp import login, write_html_to_file, logout


output_file_path = 'schedule.json'

def create_files():
    login()

    for i in range(1,37):
        for j in range(1,5):
            try:
                write_html_to_file(i,j)
            except:
                print(f'Error for faculty_id: {i}, course: {j}')

    logout()

if __name__ == '__main__':
    #create_files()

    schedules = {}

    for i in range(1,37):
        for j in range(1,4):
            try:
                (name, schedule) = create_schedule(f'{i}-{j}.txt')
                schedules[name] = schedule
            except FileNotFoundError:
                pass
    

    json_obj = json.dumps(schedules, ensure_ascii=False, indent=4)


    f = open(output_file_path, 'w', encoding='utf-8')
    f.write(json_obj)
    f.close()
    