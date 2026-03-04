#!/usr/bin/env python3
import argparse
import base64
import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE_CHECK_TIME = 30

def relative_path(fpath: str) -> str:
    return os.path.relpath(fpath, SOURCE_DIR).replace(os.sep, "/")

def encode_file_contents(fpath: str) -> str:
    with open(fpath, "rb") as f:
        return base64.b64encode(f.read()).decode()

def create_or_update_file(fpath: str):
    rel_path = relative_path(fpath)
    encoded_content = encode_file_contents(fpath)
    try:
        # We try and create first, since we don't know what current state the other directory is in
        r = requests.post(
            f"{SERVER_URL}/directory/create",
            json={"path": rel_path, "content": encoded_content},
            timeout=10
        )
        if r.status_code == 409:
            # If we know the file exists (which is a 409), then we can just update it now
            r = requests.post(
                f"{SERVER_URL}/directory/update",
                json={"path": rel_path, "content": encoded_content},
                timeout=10
            )
        r.raise_for_status()
        print(f"Synced file: {rel_path}")
    except Exception as e:
        print(f"An error occurred whilst syncing {rel_path}: {e}")

def delete_file(fpath: str):
    """Send delete request to server for a file."""
    rel_path = relative_path(fpath)
    try:
        r = requests.post(f"{SERVER_URL}/directory/delete", json={"path": rel_path}, timeout=10)
        if r.status_code not in (200, 404):
            r.raise_for_status()
        print(f"Deleted file: {rel_path}")
    except Exception as e:
        print(f"An error occurred whilst deleting {rel_path}: {e}")

class DirectoryWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            create_or_update_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            create_or_update_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            delete_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            delete_file(event.src_path) # old file name
            create_or_update_file(event.dest_path)  # new file name

def initial_directory_sync():
    # We want to make sure all files are synced with the app on startup.
    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            create_or_update_file(full_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Sync local directory to remote FastAPI directory API"
    )
    parser.add_argument("source", help="Source directory to monitor")
    parser.add_argument(
        "--app", required=True, help="URL of the FastAPI app"
    )
    args = parser.parse_args()

    SOURCE_DIR = os.path.abspath(args.source)
    SERVER_URL = args.app.rstrip("/")

    initial_directory_sync()
    print(f"Starting application and syncing source dir {SOURCE_DIR} to destination dir handled by server {SERVER_URL}")
    watcher_class = DirectoryWatcher()
    observer = Observer()
    observer.schedule(watcher_class, path=SOURCE_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(FILE_CHECK_TIME)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()