import json
from html_to_object import create_schedule
from load_html import login, write_schedule_to_file, logout, loadIds
import os, shutil   
from bot import botStart


output_file_path = 'schedule.json'

def create_files():
    folder = './schedules'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    
    for i in range(1,37):
        for j in range(1,5):
            try:
                write_schedule_to_file(i,j)
            except:
                print(f'Error for faculty_id: {i}, course: {j}')

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return ""


if __name__ == '__main__':
    # login()
    # loadIds()
    # create_files()
    # logout()
    faculty_ids = json.load(open('faculty_ids.json', 'r', encoding='utf-8'))

    schedules = {}

    for i in range(1,37):
        for j in range(1,4):
            try:
                (name, schedule) = create_schedule(f'./schedules/{i}-{j}.txt', )
                faculty = get_key(faculty_ids, i)
                if(faculty != "" and not faculty in schedules.keys()):
                    schedules[faculty] = {}
                schedules[faculty][name] = schedule
            except FileNotFoundError:
                pass
    

    json_obj = json.dumps(schedules, ensure_ascii=False, indent=4)


    f = open(output_file_path, 'w', encoding='utf-8')
    f.write(json_obj)
    f.close()
    
    botStart()