#!/bin/bash

N_WORKERS=4

# fill the job list with random jobs
for i in {1..100}; do
    echo "my job $i" >> "./jobs.list"
done

for _ in $(seq 1 $N_WORKERS); do
    # start a worker: ./worker <taskfile> <batch_size>
    ./worker.sh "./jobs.list" 8 &
done

wait
echo "All workers have finished processing."


