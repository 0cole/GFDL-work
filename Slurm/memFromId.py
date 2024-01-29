import math
import subprocess

def main():
    # 1. Give a list of Job IDs
    # 2. For each line in list
    # 3.    Parse the list and call 'sacct --units=K -o MaxRSS -j <JobId> | tail -n 1'
    # 4.    Convert to int and add to running total
    # 5. Return
    
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

    mem_var, mem_stddev = findVar(mem, mem_avg)

    print("Total memory : ", mem_total)
    print("Total successful jobs : ", job_total)
    print("Total failed jobs : ", failed_jobs)
    print("Average memory per job : ", mem_avg)
    print("Variance of jobs : ", mem_var)
    print("Standard Deviation of jobs : ", mem_stddev)

    return 0

def fetchIds(file_path):
    path = file_path
    with open(path, 'r') as file:
        ids = [''.join(char for char in line if char.isdigit()) for line in file]
    return ids

def fetchMemory(jobId):
    sacct_command_prefix = 'sacct --units=K --parsable2 -o MaxRSS,State -j '
    sacct_command_suffix = ' | tail -n 1'
    run = subprocess.run(sacct_command_prefix + str(jobId) + sacct_command_suffix, 
                                   stdout=subprocess.PIPE, shell=True)  
    stdout = run.stdout.decode('utf-8')
    fields = stdout.strip().split('|')
    mem = fields[0]
    state = fields[1]
    if "FAILED" in state:
        return -1

    mem_int = float(''.join(char for char in mem if char.isdigit()))
    
    return mem_int  

def findVar(mem, average):
    N = len(mem)

    sum_squared_diff = sum((x - average) * (x - average) for x in mem)

    variance = sum_squared_diff / N
    stddev = math.sqrt(variance)
    
    return variance, stddev

if __name__ == "__main__":
    main()