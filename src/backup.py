import os
import shutil

import pandas as pd
import yaml

from time import perf_counter
import py7zr

from src.utils import (
    printlog,
    printhdr,
    get_home_dir,
    get_base_path,
    get_backup_file_path,
    get_local_path_with_home_adjusted,
)

# List all files int the directory
home_dir = get_home_dir()
os_name = "windows" if os.name == "nt" else "mac"


def process_source_files(
    base_dir, copy_files_list, archive_files_list, target_dir, allow_override
):
    process_dicts_list = []
    # copy the files from list
    for file in [get_base_path(base_dir, file) for file in copy_files_list]:
        row = copy_or_archive(base_dir, file, target_dir, "copy", allow_override)
        process_dicts_list.append(row)

    # copy the files from list
    for file in [get_base_path(base_dir, file) for file in archive_files_list]:
        row = copy_or_archive(base_dir, file, target_dir, "zip", allow_override)
        process_dicts_list.append(row)

    df = pd.DataFrame(process_dicts_list)
    return df


def archive_file_dir(src_file_path, dest_dir):
    file_extn = ".7z"
    # create the zip file
    if os.path.exists(src_file_path):
        src_arch_file_path = f"{src_file_path}{file_extn}"
        try:
            printlog(f"Creating archive file {src_arch_file_path}", 2)
            # create the archive file
            with py7zr.SevenZipFile(src_arch_file_path, "w") as archive:
                archive.writeall(src_file_path, os.path.basename(src_file_path))
        except Exception as e:
            msg = f"Exception while creating the archive file : {src_file_path}: {e}"
            printlog(msg, 1)
            return

        dest_arch_file_path = os.path.join(
            dest_dir, os.path.basename(src_arch_file_path)
        )
        # check if the archive file exists in destination
        if os.path.exists(dest_arch_file_path):
            # if archive file is same as the source file, then do not copy
            if os.path.getsize(src_arch_file_path) == os.path.getsize(
                dest_arch_file_path
            ):
                # remove the archive file from source
                os.remove(src_arch_file_path)
                return (f"File already exists, skipping ...",)
            else:
                # remove the archive file from destination
                printlog(f"Removing the existing archive file {dest_arch_file_path}", 2)
                os.remove(dest_arch_file_path)

        # copy the file to destination
        shutil.move(src_arch_file_path, dest_arch_file_path)
        return f"File archived successfully."
    else:
        return f"File does not exists."


def copy_file_or_dir(src_file_path, file, target_dir, allow_override):
    # check if source file path exists and is a file or directory
    if os.path.exists(src_file_path):
        dest_file_path = os.path.join(target_dir, file)
        if os.path.isdir(src_file_path):
            # check if the destination directory exists
            # if destination directory exists and override is not allowed, then skip
            if os.path.exists(dest_file_path) and not allow_override:
                return f"Directory already exists, override not allowed."

            # if destination directory exists and override is allowed, then remove the directory
            if os.path.exists(dest_file_path) and allow_override:
                shutil.rmtree(dest_file_path)
                shutil.copytree(src_file_path, target_dir)
                return f"Directory copied successfully."

        elif os.path.isfile(src_file_path):
            # check if both files are same
            if os.path.exists(dest_file_path):
                # if file is same as the source file, then do not copy
                if os.path.getsize(src_file_path) == os.path.getsize(dest_file_path):
                    return f"File already exists, skipping ..."
                else:
                    # remove the file from destination
                    os.remove(dest_file_path)
            shutil.copy2(src_file_path, dest_file_path)
            return "Files copied successfully"
    else:
        return f"File not found."


# Function to copy the file or directory to destination
def copy_or_archive(base_dir, file, target_dir, mode="copy", allow_override=False):
    """

    @rtype: A dictionary with file name, mode, message and time taken
    """
    # If mode is copy
    # create a pandas data frame to save file and time taken
    t0 = perf_counter()
    msg = ""
    src_file_path = get_base_path(base_dir, file)
    try:
        # get the source file base path
        # Check if given mode is zip or copy
        if mode == "copy":
            msg = copy_file_or_dir(src_file_path, file, target_dir, allow_override)
        elif mode == "zip":
            msg = archive_file_dir(src_file_path, target_dir)
    except Exception as e:
        msg = (
            f"Exception while copying the file : {src_file_path} -> {target_dir} : {e}"
        )
        printlog(msg, 1)
    t1 = perf_counter()
    time_taken = round(t1 - t0, 4)
    return {"file": file, "mode": mode, "time_taken": time_taken, "message": msg}


def git_commit(project_dir):
    import datetime

    now = datetime.datetime.now()
    here = os.getcwd()
    commit_msg = f"backup-otto at {now.strftime('%d-%m-%Y %H:%M:%S')}"
    cmd = f'git commit -am "{commit_msg}"'
    import os

    # goto to the project directory
    os.chdir(project_dir)
    printlog(cmd)
    os.system(cmd)
    # go back to the original directory
    os.chdir(here)


def start_backup():
    """
    Main method to start the backup
    """
    printhdr("Starting backup")
    printlog(
        f"Homedir : {home_dir} ,Current path : {os.path.curdir}, running backup for {os_name}"
    )
    # Check if os specific file exists otherwise take the default file
    backup_file = get_backup_file_path()

    # Read the backup file for defined mappings
    with open(backup_file, "r") as f:
        # loop for each mapping defined in the yaml file
        data = yaml.safe_load(f)

        mapping_dicts_list = []
        process_df = pd.DataFrame(columns=["file", "mode", "time_taken", "message"])

        for mapping in data["mappings"]:
            name, target_dir, allow_override, allow_commit, sources = mapping.values()
            # Get the local path
            target_dir = get_local_path_with_home_adjusted(target_dir)

            printhdr(f"Mapping : {name}", 2)

            for source in sources:
                base_dir, copy_files_list, archive_files_list = source.values()

                df1 = process_source_files(
                    base_dir,
                    copy_files_list,
                    archive_files_list,
                    target_dir,
                    allow_override,
                )
                print(df1.to_string(index=False))
                process_time = df1["time_taken"].sum().round(3)
                process_df = pd.concat([process_df, df1], ignore_index=True)

                # Commit the changes to git
                t0 = perf_counter()
                git_commit(target_dir)
                t1 = perf_counter()

                # round the time to 2 decimal places
                commit_time = round(t1 - t0, 3)
                # append the dataframe
                mapping_dicts_list.append(
                    {
                        "mapping": name,
                        "target_dir": target_dir,
                        "src_dir": base_dir,
                        "process_time": process_time,
                        "commit_time": commit_time,
                        "time_taken": process_time + commit_time,
                    }
                )
        printhdr("Backup completed")

        bkp_df = pd.DataFrame(mapping_dicts_list)
        # print the summary in tabular format
        printlog(bkp_df.to_string(index=False), 1)
        # save the dataframe to csv
        bkp_df.to_csv("backup_summary.csv", index=False)
        process_df.to_csv("process_summary.csv", index=False)

        return bkp_df


if __name__ == "__main__":
    # copy_bash()
    start_backup()
