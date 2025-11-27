import sys
from pathlib import Path
from collections import Counter


def parse_log_line(line: str) -> dict[str, str]:
    """Split a log line into date, time, level, and message."""

    date, time, level, rest = line.split(maxsplit=3)

    return {"date": date, "time": time, "level": level, "message": rest}


def load_logs(file_path: str) -> list[dict[str, str]]:
    """Load and parse all valid log lines from a given file path."""

    path = Path(file_path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            rows: list[dict[str, str]] = []

            for raw in f:
                line = raw.strip()

                if not line:
                    continue

                try:
                    rows.append(parse_log_line(line))

                except ValueError:
                    continue

            return rows

    except FileNotFoundError:
        print("Error: File not found")

    except UnicodeError:
        print("Error: Unicode")

    return []


def filter_logs_by_level(
    logs: list[dict[str, str]], level: str
) -> list[dict[str, str]]:
    """Return only logs that match the given level."""

    filtered_logs = filter(lambda log: log.get("level", "") == level.upper(), logs)

    return list(filtered_logs)


def count_logs_by_level(logs: list[dict[str, str]]) -> dict[str, int]:
    """Count the number of log entries for each log level."""

    counts = Counter(log.get("level", "") for log in logs)
    return dict(counts)


def prepare_for_print(level: str, count: str | int, line_len: int) -> str:
    """Format a single row for aligned console output."""

    return f"{level.ljust(line_len)}| {count}"


def display_log_counts(counts: dict[str, int]) -> None:
    """Print a formatted table of log levels and their counts."""

    COLUMN_WIDTH = 10

    header = prepare_for_print("Level", "Count", COLUMN_WIDTH)
    print(header)
    print("-" * len(header))

    for level, count in counts.items():
        print(prepare_for_print(level, count, COLUMN_WIDTH))


def display_logs_by_level(logs: list[dict[str, str]], level: str) -> None:
    """Print all log entries that correspond to the given log level."""

    print(f"\nLogs by level '{level.upper()}':")

    filtered_logs = filter_logs_by_level(logs, level)

    for log in filtered_logs:
        print(
            f"{log.get('date', '?')} {log.get('time', '?')} - {log.get('message', '')}"
        )


def main():
    """Command-line entry point for the log analysis script."""

    args = sys.argv[1:]

    if not args:
        print("Usage: script.py <file_path> [LEVEL]")
        return

    file_path = args[0]
    parsed_logs = load_logs(file_path)

    if len(parsed_logs) == 0:
        print("No valid log lines found")
        return

    count_logs = count_logs_by_level(parsed_logs)
    display_log_counts(count_logs)

    if len(args) > 1 and args[1]:
        level = args[1]
        display_logs_by_level(parsed_logs, level)


if __name__ == "__main__":
    main()
