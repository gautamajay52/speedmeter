from rich.progress import (BarColumn, DownloadColumn, Progress, SpinnerColumn,
                           TaskProgressColumn, TextColumn, TimeElapsedColumn,
                           TimeRemainingColumn, TransferSpeedColumn)


def human_size(size_in_bytes) -> str:
    if not size_in_bytes:
        return "0B"

    SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

    for unit in SIZE_UNITS:
        if abs(size_in_bytes) < 1024:
            return f"{round(size_in_bytes, 2)}{unit}"
        size_in_bytes /= 1024

    return "tooBigtoHandle"


progress = Progress(
    TimeElapsedColumn(),
    TextColumn("{task.description}"),
    TransferSpeedColumn(),
    SpinnerColumn(),
    BarColumn(),
    TaskProgressColumn(),
    DownloadColumn(binary_units=True),
    TimeRemainingColumn(compact=True),
)
