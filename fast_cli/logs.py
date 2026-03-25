"""
`fastmvc logs` — Tail and filter application logs.

Supports JSON-structured logs with filtering by level, service, and time range.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Iterator


def _parse_timestamp(ts_str: str) -> datetime | None:
    """Parse various timestamp formats."""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%d/%b/%Y:%H:%M:%S",
        "%d-%b-%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    return None


def _colorize_level(level: str) -> str:
    """Return colored level string."""
    colors = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "WARN": "\033[33m",       # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "FATAL": "\033[35m",      # Magenta
    }
    reset = "\033[0m"
    color = colors.get(level.upper(), "")
    if color and sys.stdout.isatty():
        return f"{color}{level:8}{reset}"
    return f"{level:8}"


def _format_log_line(data: dict, compact: bool = False) -> str:
    """Format a structured log entry for display."""
    timestamp = data.get("time", data.get("timestamp", data.get("@timestamp", "")))
    level = data.get("level", data.get("severity", "INFO"))
    message = data.get("message", data.get("msg", data.get("log", "")))
    service = data.get("service", data.get("logger", data.get("name", "app")))
    
    if compact:
        return f"[{timestamp}] {_colorize_level(level)} {message}"
    
    extra_fields = []
    for key, value in data.items():
        if key not in ("time", "timestamp", "@timestamp", "level", "severity", 
                       "message", "msg", "log", "service", "logger", "name"):
            if isinstance(value, (str, int, float, bool)):
                extra_fields.append(f"{key}={value}")
    
    extra = " ".join(extra_fields)
    if extra:
        extra = f" | {extra}"
    
    return f"[{timestamp}] {_colorize_level(level)} [{service}] {message}{extra}"


def _read_log_file(path: Path, follow: bool = False) -> Iterator[str]:
    """Read lines from a log file, optionally following new lines."""
    if not path.exists():
        return
    
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                yield line.rstrip("\n")
        return
    
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        if follow:
            # Seek to end and follow new lines
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    import time
                    time.sleep(0.1)
                    continue
                yield line.rstrip("\n")
        else:
            for line in f:
                yield line.rstrip("\n")


def _find_log_files(log_dir: Path, pattern: str | None = None) -> list[Path]:
    """Find log files in directory, optionally matching a pattern."""
    if not log_dir.exists():
        return []
    
    files = []
    for item in log_dir.iterdir():
        if not item.is_file():
            continue
        if pattern and not re.search(pattern, item.name):
            continue
        if item.suffix in (".log", ".gz", ""):
            files.append(item)
    
    # Sort by modification time (newest first)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def tail_logs(
    log_dir: Path | None = None,
    file_pattern: str | None = None,
    level: str | None = None,
    service: str | None = None,
    search: str | None = None,
    since: str | None = None,
    follow: bool = False,
    lines: int = 50,
    json_output: bool = False,
    compact: bool = False,
) -> int:
    """
    Tail and filter application logs.
    
    Returns 0 on success, 1 on error.
    """
    # Default log directories
    if log_dir is None:
        cwd = Path.cwd()
        candidates = [
            cwd / "logs",
            cwd / "log",
            cwd / "var" / "log",
            cwd,
        ]
        for candidate in candidates:
            if candidate.exists():
                log_dir = candidate
                break
        else:
            log_dir = cwd
    
    # Parse time filters
    since_dt = None
    if since:
        if since.endswith("m"):
            since_dt = datetime.now() - timedelta(minutes=int(since[:-1]))
        elif since.endswith("h"):
            since_dt = datetime.now() - timedelta(hours=int(since[:-1]))
        elif since.endswith("d"):
            since_dt = datetime.now() - timedelta(days=int(since[:-1]))
        else:
            try:
                since_dt = datetime.fromisoformat(since)
            except ValueError:
                print(f"Invalid --since format: {since}")
                return 1
    
    # Compile search regex
    search_re = None
    if search:
        try:
            search_re = re.compile(search, re.IGNORECASE)
        except re.error as e:
            print(f"Invalid search pattern: {e}")
            return 1
    
    log_files = _find_log_files(log_dir, file_pattern)
    if not log_files:
        print(f"No log files found in {log_dir}")
        return 0
    
    # Read and process logs
    shown = 0
    buffer: list[tuple[datetime | None, str]] = []
    
    for log_file in log_files[:5]:  # Process up to 5 most recent files
        for line in _read_log_file(log_file, follow=False):
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Plain text log line
                data = {"message": line, "level": "INFO"}
            
            # Apply filters
            if level:
                log_level = data.get("level", data.get("severity", "INFO")).upper()
                if log_level != level.upper():
                    continue
            
            if service:
                log_service = data.get("service", data.get("logger", data.get("name", "")))
                if service.lower() not in log_service.lower():
                    continue
            
            if since_dt:
                ts_str = data.get("time", data.get("timestamp", data.get("@timestamp", "")))
                ts = _parse_timestamp(ts_str) if ts_str else None
                if ts and ts < since_dt:
                    continue
            
            if search_re:
                message = str(data.get("message", data.get("msg", line)))
                if not search_re.search(message):
                    continue
            
            # Format output
            if json_output:
                formatted = line
            else:
                formatted = _format_log_line(data, compact)
            
            ts_str = data.get("time", data.get("timestamp", data.get("@timestamp", "")))
            ts = _parse_timestamp(ts_str) if ts_str else None
            buffer.append((ts, formatted))
    
    # Sort by timestamp and output last N lines
    buffer.sort(key=lambda x: x[0] or datetime.min)
    
    for _, formatted in buffer[-lines:]:
        print(formatted)
        shown += 1
    
    # Follow mode
    if follow and log_files:
        print("\n--- Following new log entries (Ctrl+C to exit) ---\n")
        try:
            for line in _read_log_file(log_files[0], follow=True):
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    data = {"message": line, "level": "INFO"}
                
                # Apply filters in follow mode
                if level:
                    log_level = data.get("level", data.get("severity", "INFO")).upper()
                    if log_level != level.upper():
                        continue
                
                if service:
                    log_service = data.get("service", data.get("logger", data.get("name", "")))
                    if service.lower() not in log_service.lower():
                        continue
                
                if search_re:
                    message = str(data.get("message", data.get("msg", line)))
                    if not search_re.search(message):
                        continue
                
                if json_output:
                    print(line)
                else:
                    print(_format_log_line(data, compact))
        except KeyboardInterrupt:
            print("\n\nStopped following logs.")
    
    return 0


def show_log_stats(log_dir: Path | None = None) -> int:
    """Show statistics about log files."""
    if log_dir is None:
        log_dir = Path.cwd() / "logs"
    
    if not log_dir.exists():
        print(f"Log directory not found: {log_dir}")
        return 1
    
    files = list(log_dir.iterdir())
    files = [f for f in files if f.is_file() and f.suffix in (".log", ".gz", "")]
    
    if not files:
        print(f"No log files in {log_dir}")
        return 0
    
    print(f"\nLog Statistics for: {log_dir}\n")
    print(f"{'File':<40} {'Size':>12} {'Modified':>20}")
    print("-" * 74)
    
    total_size = 0
    for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
        stat = f.stat()
        size = stat.st_size
        total_size += size
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        # Format size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        
        print(f"{f.name:<40} {size_str:>12} {modified:>20}")
    
    print("-" * 74)
    if total_size < 1024 * 1024:
        total_str = f"{total_size / 1024:.1f} KB"
    else:
        total_str = f"{total_size / (1024 * 1024):.1f} MB"
    print(f"{'Total':<40} {total_str:>12}\n")
    
    return 0
