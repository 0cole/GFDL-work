import os
import utils
import subprocess
import data_input as d

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

    # Populate jobs dictionary from data file. Only FRE jobs that have a size greater
    # than the memory cutoff will exist after populate finishes
    jobs = utils.populate(temp_data_path, mem_cutoff, name_requirement)

    jobs = utils.sortJobs(jobs)

    utils.outputToCSV(jobs, output_path)
    
    print("Completed, data output to: " + output_path + ", total jobs: ", len(jobs))

    # subprocess.run(["rm", "-f", temp_data_path])


if __name__ == "__main__":
    main()