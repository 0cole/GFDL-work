import os
import re
import csv
import json
import subprocess
from datetime import timedelta

def generate(start_date, end_date, temp_data_path):
    '''
    Queries the SLURM database all the jobs from the start_date 
    to the end_date and caches them in a file. Only call this once. 
    Include the desired path name for this cache when calling the 
    function as well as the start date. Do not overlap years.
    '''
    current_date = start_date
    sacct_command_prefix = 'sacct -a --parsable2 --units=K -D -n -o ' + \
                           'JobIDRaw,JobName,Comment,MaxRss,ElapsedRaw, ' + \
                           'NodeList,End,State,ExitCode,User '

    # Check if file paths are already in use and ask user if it is alright to delete them if so
    if os.path.isfile(temp_data_path):
        if removeFile(temp_data_path):
            return

    # When there is more than 1 week from the current_date to the end_date
    while current_date + timedelta(days=6) < end_date:

        end_of_week = current_date + timedelta(days=6)
        start = f'--starttime={current_date.strftime("%Y-%m-%d")}-00:00:00 '
        end = f'--endtime={end_of_week.strftime("%Y-%m-%d")}-23:59:59'

        print(f"collecting from : {start}to {end}")

        subprocess.run(sacct_command_prefix + start + end + ' >> ' + temp_data_path, shell=True)

        current_date += timedelta(weeks=1)

    # When there is less than 1 week from the current_date to the end_date
    if current_date + timedelta(days=6) >= end_date:

        start = f'--starttime={current_date.strftime("%Y-%m-%d")}-00:00:00 '
        end = f'--endtime={end_date.strftime("%Y-%m-%d")}-23:59:59'
        
        print(F"collecting from : {start}to {end}")

        subprocess.run(sacct_command_prefix + start + end 
                       + ' >> ' + temp_data_path, shell=True)

def populate(temp_data_path, mem_cutoff, name_requirement):
    '''
    Reads from the file that is created with all the output from the 'sacct'
    commands. Executes once and creates entries in the jobs dictionary. 
    Afterwards, filters out all the non-FRE jobs. This means any job without 
    the substring 'fre/' in its comment is excluded. Returns a dict with
    the valid jobs.

    Note:
        MaxRSS is represented originally as ****K for kilobytes, and 
        located on the job step which is the following line
    '''
    jobs = {}

    with open(temp_data_path, 'r') as file:
        iterator = iter(file)

        for line in iterator:
            fields = line.strip().split('|')

            next_fields = next(iterator).strip().split('|')

            JobId, name, comment, _, elapsed, node, end, state, exitcode, user = fields
            memory = next_fields[3].rstrip("K") if "K" in next_fields[3] else "0"
            elapsed = elapsed if elapsed else "0"

            # if name_requirement not in name:
            #     continue

            if "Baudilio" not in user:
                continue

            # if int(memory) < mem_cutoff:
            #     continue

            # Create a dictionary entry with JobId as the keys
            jobs[JobId] = {
                'id' : JobId,
                'JobName': name,
                'Comment': comment,
                'Memory': int(memory),
                'Elapsed': int(elapsed),
                'Node' : node,
                'End' : end,
                'State' : state,
                'ExitCode' : exitcode,
                'User' : user
            }

    return jobs

def sortJobs(jobs):
    '''
    Sorts and returns the jobs in job dict by maxRSS.
    '''
    sorted_jobs = dict(sorted(jobs.items(), key=lambda item: item[1]['Memory']))

    sorted_jobs = dict(reversed(list(sorted_jobs.items())))

    return sorted_jobs

def removeFile(path):
    '''
    Removes a file if it exists. Asks the user before doing so and user must 
    reply with either 'y' or 'n'. Returns True if deleting and False if user
    wants to keep file.
    '''
    if os.path.isfile(path) == False:
        return False

    result = removeHelper(path)

    if result == -2:
        print("Quitting")
        return True
    elif result == -1:
        print(f"File {path} does not exist, internal error")
        return True
    return False

def removeHelper(path):
    '''
    Helper for removeFile. Returns 0 upon successful delete, and a negative
    number if failed or if user does not want file deleted.
    '''
    verify = ""
    while verify not in {"y", "n"}:
        verify = input("Are you sure you would like to remove" + path + 
                       "? please enter either y/n : ")

    if verify == "n":
        return -2
    else:
        if os.path.isfile(path):
            os.remove(path)
            print(f"*** Removed {path} ***")
            return 0
    return -1

def outputToJSON(jobs, file_path):
    """
    Creates and writes to a .json File. Destination is specified in 
    the variable file_path.
    """
    json_obj = json.dumps(jobs, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_obj)

def outputToCSV(jobs, file_path):
    """
    Creates and writes to a .csv File. Destination is specified in 
    the variable file_path.
    """
    field_names = ['id', 'JobName', 'Comment', 'Memory', 'Elapsed',
                   'Node', 'End', 'State', 'ExitCode', 'User']

    with open(file_path, "w") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_writer.writerows(jobs.values())

