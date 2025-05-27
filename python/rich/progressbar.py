#!/usr/bin/env python3
import time
import random
from rich.progress import (Progress, BarColumn, TextColumn, TimeElapsedColumn,
                           TimeRemainingColumn, TaskProgressColumn,)
from rich import print


def manual_progress():
    columns = [
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),   # this is the progress as a percentage

            # specifying a TextColumn allows us to format the output
            TextColumn("[progress.percentage]-[progress.elapsed] [{task.completed:.2f}/{task.total}]"),
            "Elapsed:",             # we can specify text as a simple string as well
            TimeElapsedColumn(),    # a beautified version of "{task.elapsed}"
            "Remaining:",
            TimeRemainingColumn(),  # this is just a linear fit: estimate = ceil(remaining / speed)
    ]

    progress = Progress(*columns,
                        refresh_per_second=5,       # automatic refresh every 5 seconds
                        speed_estimate_period=30,   # estimate period used to calculate speed
                        expand=False,               # expand task table to fit width (ugly, so don't)
                        auto_refresh=True)

    # manually start the progress bar
    progress.start()

    tasks = [i for i in range(1, 5)]

    for i in tasks:
        nwork = 100   # 100 units of work per task
        task = progress.add_task(f"Processing item {i}", total=nwork)

        iwork = 0
        while iwork < nwork:
            time.sleep(0.01)

            _work = random.random() # random work (between 0 and 1)

            iwork += _work
            progress.update(task, advance=_work)
            # we can manually call refresh
            # if not, the progress bar will refresh automatically every 5 seconds
            progress.refresh()

        progress.update(task, completed=nwork)
        progress.refresh()

    # stop the progress bar
    progress.stop()


def context_progress():
    columns = [
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[progress.percentage]-[progress.elapsed] [{task.completed:.2f}/{task.total}]"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
    ]
    progress = Progress(*columns,
                        refresh_per_second=5,
                        speed_estimate_period=30,   # estimate period used to calculate speed
                        expand=False,               # expand task table to fit width
                        auto_refresh=True)

    with progress:
        tasks = [i for i in range(1, 5)]

        for i in tasks:
            nwork = 100

            task = progress.add_task(f"Processing item {i}", total=nwork)
            iwork = 0
            while iwork < nwork:
                time.sleep(0.01)

                _work = random.random()
                iwork += _work
                progress.update(task, advance=_work)

                # here we will not call progress.refresh()
                # so the progress bar will refresh automatically every 5 seconds
                # progress.refresh()
            progress.update(task, completed=nwork)
            progress.refresh()

    # No need to call progress.stop() here, as it is handled by the context manager

if __name__ == "__main__":
    print("Manual Progress Bar Example")
    manual_progress()
    print("\nContext Progress Bar Example")
    context_progress()

