import os


import yaml
from pathlib import Path

base_path = Path(__file__).parent.parent

LOG_FILE = os.path.join(base_path, "logs", "output.log")

# method to delete the log file
def delete_log_file():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

# print the log file
def print_log_file():
    with open(LOG_FILE, 'r') as file:
        for line in file:
            print(line, end='')

# method to write message in the log file
def write_log_file( msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{msg}\n")


def write_log(msg, indent=0):
    # if msg is not null or empty
    if msg:
        # printlog(msg, indent)
        write_log_file(msg)

def printlog(msg, indent=0):
    # if msg is not null or empty
    if msg:
        print(get_formatted_msg(msg, indent))

# check if the log has any error 
def has_error():
    with open(LOG_FILE, 'r') as file:
        for line in file:
            if "ERROR" in line:
                return True
    return False

def printhdr(msg, indent=0):
    write_log(get_formatted_hdr(msg, indent))

def get_formatted_msg(msg, indent=0):
    msg = f"{' ' * indent}{msg}"
    return msg

def get_formatted_hdr(msg, indent=0):
    msg = f" {msg} " if msg else ""
    msg = f"{'=' * 50}{msg}{'=' * 50}"
    return get_formatted_msg(msg, indent)

def get_home_dir():
    """
    Get the home directory setup in backup.yml file and remove any trailing slash
    """
    backup_file = get_backup_file_path()
    # check the home directory setup in the backup.yml file
    with open(backup_file, "r") as f:
        # loop for each mapping defined in the yaml file
        data = yaml.safe_load(f)

        # Get the home directory and remove any trailing slash
        home_dir = data["homedir"]
        # Get the home directory and remove any trailing slash
        if home_dir.endswith(os.path.sep):
            home_dir = home_dir[:-1]
    return home_dir


def get_backup_file_path():
    # Check if os specific file exists otherwise take the default file
    print(os.name)
    os_name = "windows" if os.name == "nt" else "mac"
    backup_file = f"backup-{os_name}.yml"
    file_path = os.path.join(base_path, "config", backup_file)
    if not os.path.exists(file_path):
        raise Exception(
            f"Missing file : ${file_path}\nPlease setup the backup configuration file."
        )
    return file_path


def get_local_path_with_home_adjusted(local_path):
    # Get the home directory and remove any trailing slash
    homedir = get_home_dir()

    if local_path.startswith("~"):
        # check the home directory setup in the backup.yml file
        # Get the local path
        local_path = local_path.replace("~", homedir)
    return local_path


def get_base_path(base_dir: str, file: str):
    # Get the local path
    local_path = os.path.join(base_dir, file)
    return get_local_path_with_home_adjusted(local_path)
