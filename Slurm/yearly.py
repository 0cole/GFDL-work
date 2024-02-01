import os
import utils
import subprocess
import data_input as d
from datetime import timedelta

start_date = d.start

end_date = d.end

mem_cutoff = d.cutoff

name_requirement = d.name

temp_data_path = d.temp

output_path = d.out

def main():
    '''
    Collects the total jobs within a certain window of time and creates an output in JSON format
    of all FRE jobs. The output file name is specified in the global file_path variable. The
    start and end times are specified in the start_date and end_date global variables respectively

    Each entry contains the JobIDRaw (key)
                            JobName
                            Comment
                            Memory
                            Elapsed
                            Node
                            End
                            State
                            ExitCode
                            User
    '''
    jobs = {}
    current_date = start_date
    sacct_command_prefix   = 'sacct -a --parsable2 --units=K -D -n -o JobIDRaw,JobName,Comment,MaxRss,ElapsedRaw,NodeList,End,State,ExitCode,User  '

    # Check if file paths are already in use and ask user if it is alright to delete them if so
    if os.path.isfile(temp_data_path) or os.path.isfile(output_path):
        if utils.removeFile(temp_data_path) or utils.removeFile(output_path):
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

    # Populate jobs dictionary from data file. Only FRE jobs that have a size greater
    # than the memory cutoff will exist after populate finishes
    jobs = utils.populate(temp_data_path, mem_cutoff, name_requirement)

    jobs = utils.sortJobs(jobs)

    utils.outputToCSV(jobs, output_path)
    
    print("Completed, data output to: " + output_path + ", total jobs: ", len(jobs))

    subprocess.run(["rm", "-f", temp_data_path])


if __name__ == "__main__":
    main()