import os
import common.constants as Constant


def delete_temp():
    for root, _, files in os.walk(Constant.TEMP_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except (Exception, ValueError):
                pass


def change_name(name):
    return name.strip('.')


def write_key(key, email):
    with open('google_key.txt', 'a') as file:
        file.write(email + ":" + key + '\n')


def write_error(error, email, name_project=None):
    with open('error_email.txt', 'a') as file:
        if name_project:
            file.write(email + ":" + error + ":" + name_project + '\n')
        else:
            file.write(email + ":" + error + '\n')


def check_number(email):
    if email[0].isdigit():
        return True
    return False
