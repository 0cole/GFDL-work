import subprocess
import json
from datetime import datetime, timedelta

# Initial date
start_date = datetime(2023, 1, 1)

# End date
end_date = datetime(2023, 1, 31)

# Temporary data path
temp_data_path = './data_temp'

# Output JSON filepath
file_path = "./data_output.json"

def main():
    '''
    Collects the total jobs within a certain window of time and creates an output in JSON format
    of all FRE jobs. The output file name is specified in the global file_path variable. The 
    start and end times are specified in the start_date and end_date global variables respectively

    Each entry contains the JobIDRaw, JobName, MaxRSS (Memory), and Elapsed (time spent running).
    '''
    jobs = {}
    current_date = start_date
    sacct_command_prefix   = 'sacct -a --parsable2 -D -o JobIDRaw,JobName,Comment,MaxRss,ElapsedRaw '

    # When there is more than 1 week from the current_date to the end_date
    while current_date + timedelta(days=6) <= end_date:

        end_of_week = current_date + timedelta(days=6)
        start = f'--starttime={current_date.strftime("%Y-%m-%d")} '
        end = f'--endtime={end_of_week.strftime("%Y-%m-%d")}'

        print("collecting from : " + start + "to " + end)

        subprocess.run(sacct_command_prefix + start + end + ' >> ' + temp_data_path, shell=True)

        current_date += timedelta(weeks=1)

    # When there is less than 1 week from the current_date to the end_date
    if current_date + timedelta(days=6) > end_date:

        start = f'--starttime={current_date.strftime("%Y-%m-%d")} '
        end = f'--endtime={end_date.strftime("%Y-%m-%d")}'
        
        print("collecting from : " + start + " to " + end)

        subprocess.run(sacct_command_prefix + start + end + ' >> ' + temp_data_path, shell=True)

    # Populate jobs dictionary from data file. Only FRE jobs will exist after populate finishes
    job_count = populate(jobs)

    outputToFile(jobs)
    
    print("Completed, data output to: " + file_path + ", total jobs: " + str(job_count))

    # Remove temp file
    subprocess.run(["rm", "-f", temp_data_path])

def populate(jobs):
    '''
    Reads from the file that is created with all the output from the 'sacct' commands. Executes once
    and creates entries in the jobs dictionary. Afterwards, filters out all the non-FRE jobs. This
    means any job without the substring 'fre/' in its comment is excluded.

    Args:
        jobs: Dictionary to be populated with all the FRE jobs

    Returns:
        The total number of FRE jobs included in the JSON file
    '''
    job_count = 0

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

            if (memory=='') :
                memory='0'
            else: 
                memory = memory[0:len(memory)-1]
            if (elapsed=='') :
                elapsed='0'

            # Create a dictionary entry with JobId as the keys
            jobs[JobId] = {
                'JobName': name,
                'Comment': comment,
                'Memory': memory + ' kilobytes',
                'Elapsed': elapsed + ' seconds'
            }
            job_count += 1

    return job_count

def outputToFile(jobs):
    """
    Creates and writes to a .json File. Destination is specified in the global variable file_path.

    Args:
        jobs: Dictionary of all FRE jobs
    """
    json_obj = json.dumps(jobs, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_obj)

if __name__ == "__main__":
    main()