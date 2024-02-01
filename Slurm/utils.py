import os
import re
import csv
import json

def populate(temp_data_path, mem_cutoff):
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

            if 'fre/' not in fields[2]:
                continue

            next_fields = next(iterator).strip().split('|')

            JobId, name, comment, _, elapsed, node, end, state = fields
            memory = next_fields[3].rstrip("K") if "K" in next_fields[3] else "0"
            elapsed = elapsed if elapsed else "0"

            if int(memory) < mem_cutoff:
                continue

            # Get job type that is embedded in the job name
            patterns = {
                "ocean": r'ocean_.*?(\d+)',
                "refineDiag": r'refineDiag',
            }

            for keyword, pattern in patterns.items():
                if keyword in name:
                    match = re.search(pattern, name)
                    type = match.group(0) if match else keyword
                    type = re.sub(r'\d+$', '', type).replace("_", " ") if keyword == "ocean" else type
                    break
            else:
                type = ""

            # Create a dictionary entry with JobId as the keys
            jobs[JobId] = {
                'JobName': name,
                'Comment': comment,
                'Memory': int(memory),
                'Elapsed': int(elapsed),
                'Node' : node,
                'End' : end,
                'State' : state,
                'Type' : type
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
    field_names = ['JobName', 'Comment', 'Memory', 'Elapsed',
                   'Node', 'End', 'State', 'Type']

    with open(file_path, "w") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_writer.writerows(jobs.values())

