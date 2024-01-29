import math
import subprocess

def main():
    '''
    Calculate and print statistics based on job memory IDs.

    Computes:
        Total memory between all jobs
        The number of jobs that were run successfully
        The number of jobs that failed at some point (unintended error OR user canceled)
        Average memory per job
        Variance between all jobs
        Standard deviation between all jobs

    Returns:
        int : 0 upon success
    '''
    
    path = './data_test_ids'
    ids = fetchIds(path)
    failed_jobs = 0
    mem = []

    for job_id in ids:
        mem_id = fetchMemory(job_id)
        if mem_id < 0:
            failed_jobs += 1
            continue
        mem.append(mem_id)

    # mem = [fetchMemory(id) for id in ids]

    mem_total = sum(mem)
    job_total = len(mem)
    mem_avg =  mem_total / job_total

    mem_var, mem_stddev = fetchStats(mem, mem_avg)

    print("Total memory : ", mem_total)
    print("Total successful jobs : ", job_total)
    print("Total failed jobs : ", failed_jobs)
    print("Average memory per job : ", mem_avg)
    print("Variance of jobs : ", mem_var)
    print("Standard Deviation of jobs : ", mem_stddev)

    return 0

def fetchIds(file_path):
    '''
    Separates the file passed into unique job IDs

    Args:
        file_path: The path containing the list of Job IDs
    
    Returns:
        An array of the parsed Job IDs
    '''
    path = file_path
    with open(path, 'r') as file:
        ids = [''.join(char for char in line if char.isdigit()) for line in file]
    return ids

def fetchMemory(job_id):
    '''
    Given a job ID, find its corresponding memory.

    Args:
        job_id (int): The individual job ID to access that job's memory

    Returns:
        int or float: The memory in kilobytes if the job is successful.
                      Returns -1 if the job has failed.
    '''
    sacct_command_prefix = 'sacct --units=K --parsable2 -o MaxRSS,State -j '
    sacct_command_suffix = ' | tail -n 1'
    run = subprocess.run(sacct_command_prefix + str(job_id) + sacct_command_suffix, 
                                   stdout=subprocess.PIPE, shell=True)  
    stdout = run.stdout.decode('utf-8')
    fields = stdout.strip().split('|')
    mem = fields[0]
    state = fields[1]
    if "FAILED" in state:
        return -1

    mem_int = float(''.join(char for char in mem if char.isdigit()))
    
    return mem_int  

def fetchStats(mem, average):
    '''
    Finds the variance and standard deviation of all the memories in an array.

    Args:
        mem (array) : the memories to be computed
        average : the average value of all memories
    
    Returns:
        variance (float) : the variance of mem
        stddev (float) : the standard deviation of mem
    '''
    N = len(mem)

    sum_squared_diff = sum((x - average) * (x - average) for x in mem)

    variance = sum_squared_diff / N
    stddev = math.sqrt(variance)

    return variance, stddev

if __name__ == "__main__":
    main()