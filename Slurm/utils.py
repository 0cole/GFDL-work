import os
import csv
import json

def populate(jobs, temp_data_path):
    '''
    Reads from the file that is created with all the output from the 'sacct' commands. Executes once
    and creates entries in the jobs dictionary. Afterwards, filters out all the non-FRE jobs. This
    means any job without the substring 'fre/' in its comment is excluded.

    Args:
        jobs (dict) : Dictionary to be populated with all the FRE jobs
        temp_data_path (string) : Path that contains the output from the sacct calls that needs to be parsed

    Returns:
        int : 0 upon success
    '''
    with open(temp_data_path, 'r') as file:
        iterator = iter(file)
        for line in iterator:
            # Split the line into fields based on '|'
            fields = line.strip().split('|')

            # If not FRE job then do not include in dictionary
            if 'fre/' not in fields[2]:
                continue

            
            next_fields = next(iterator).strip().split('|')

            JobId = fields[0]
            name = fields[1]
            comment = fields[2]
            memory = next_fields[3]
            elapsed = fields[4]
            node = fields[5]
            end = fields[6]

            if memory == "":
                memory = "0"
            else:
                # MaxRSS is represented originally as ****K for kilobytes
                if "K" in memory:
                    memory = memory.rstrip("K")

            if (elapsed==""):
                elapsed="0"

            # Create a dictionary entry with JobId as the keys
            jobs[JobId] = {
                'JobName': name,
                'Comment': comment,
                'Memory': int(memory),
                'Elapsed': int(elapsed),
                'Node' : node,
                'End' : end
            }
    return 0

def sortJobs(jobs, mem_cutoff):
    '''
    Sorts the jobs by MaxRSS and filters out all the jobs that have an exit state of "FAILED"

    Args:
        jobs (dict) : the jobs to be filtered
        mem_cutoff (int) : the desired MaxRSS cutoff number. Jobs with a MaxRSS less than the cutoff
                           number will be filtered out and not included in the filtered dict

    Returns:
        sorted_jobs (dict) : a dictionary containing all the jobs that have a MaxRSS greater than the
                             mem_cutoff and do not have an exit state of "FAILED"
    '''
    remove_jobs = []

    sorted_jobs = dict(sorted(jobs.items(), key=lambda item: item[1]['Memory']))

    sorted_jobs = dict(reversed(list(sorted_jobs.items())))

    for jobId in sorted_jobs:
        job_data = jobs.get(jobId)
        if job_data['Memory'] < mem_cutoff:
            remove_jobs.append(jobId)

    for jobId in remove_jobs:
        sorted_jobs.pop(jobId)

    return sorted_jobs

def removeFile(path):
    '''
    Removes a file if it exists.

    Args:
        path (string) : the path name of the file to be removed
    '''
    if os.path.isfile(path):
        os.remove(path)
        print(f"*** Removed {path} ***")

def outputToJSON(jobs, file_path):
    """
    Creates and writes to a .json File. Destination is specified in the variable file_path.

    Args:
        jobs (dict) : Dictionary of all FRE jobs
        file_path (string) : The path name that the data should be written to
    """
    json_obj = json.dumps(jobs, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_obj)

def outputToCSV(jobs, file_path):
    """
    Creates and writes to a .csv File. Destination is specified in the variable file_path.

    Args:
        jobs (dict) : Dictionary of all FRE jobs
        file_path (string) : The path name that the data should be written to
    """
    field_names = ['JobName', 'Comment', 'Memory', 'Elapsed', 'Node', 'End']

    with open(file_path, "w") as csvfile:

        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_writer.writerows(jobs.values())

        # for row in zip(*jobs.values()):
        #     print(row)
        #     csv_writer.writerow(row)