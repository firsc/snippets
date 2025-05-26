#!/bin/bash
set -e

pop_lines() {
    local taskfile="$1"
    local batch_size="$2"

    local lockfile="${taskfile}.lock"
    local lines=()

    # acquire lock
    exec 200>"$lockfile"
    flock 200

    if [[ -s "$taskfile" ]]; then
        readarray -t lines < <(head -n "$batch_size" "$taskfile")

        # remove the lines from the taskfile
        sed -i "1,${batch_size}d" "$taskfile"

        flock -u 200
        exec 200>&-

        # return lines into stdout
        printf "%s\n" "${lines[@]}"
        return 0
    else
        flock -u 200
        exec 200>&-
        return 1
    fi
}

worker() {
    local taskfile="$1"
    local batch_size="$2"

    while true; do
        # get lines and check exit status
        readarray -t batch < <(pop_lines "$taskfile" "$batch_size")

        # filter any empty lines
        local batch_filtered=()
        for line in "${batch[@]}"; do
            if [[ -n "$line" ]]; then
                batch_filtered+=("$line")
            fi
        done

        if [[ ${#batch_filtered[@]} -eq 0 ]]; then
            echo "No valid tasks in batch. Exiting"
            break
        fi

        echo "Processing batch of size ${#batch_filtered[@]}"
        $process -j "${#batch_filtered[@]}" "${batch_filtered[@]}"
    done
}

# dummy process which accepts:
# # -j <number of jobs> <job1> <job2> ...
process="python ./process.py"


if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <taskfile> <batch_size>"
    exit 1
fi

worker "$1" "$2"

