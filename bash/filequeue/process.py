#!/usr/bin/env python3
"""
Dummy example for multiprocessing.
"""

import multiprocessing as mp
import argparse
import time

parser = argparse.ArgumentParser(description="Dummy example for multiprocessing.")
parser.add_argument("-j", "--jobs", type=int, default=1, help="Number of jobs to run in parallel.")
parser.add_argument("joblist", nargs="*", help="List of jobs to run.")
args = parser.parse_args()

def process_job(job):
    time.sleep(1)  # Simulate a time-consuming job
    print("Finished job:", job)


with mp.Pool(args.jobs) as pool:
    if args.joblist:
        print("Processing job list:", args.joblist)
        pool.map(process_job, args.joblist)
    else:
        print("No jobs provided. Exiting.")

