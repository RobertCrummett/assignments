"""
Code modified from 4Oh4's answer on Stack Overflow 2/27/2018
https://stackoverflow.com/questions/182197/how-do-i-watch-a-file-for-changes
"""
import argparse
from pathlib import Path
from functools import partial
import subprocess
import time

class Watcher(object):
    running = True
    refresh_delay_secs = 1

    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self.cached_stamp = watch_file.stat().st_mtime
        self.file = watch_file
        self.call_func_on_change = partial(call_func_on_change, *args, **kwargs)

    def look(self):
        stamp = self.file.stat().st_mtime
        if stamp != self.cached_stamp:
            if self.call_func_on_change is not None:
                self.call_func_on_change()
            self.cached_stamp = stamp

    def watch(self):
        print(f"Watching {self.file}...")
        while self.running:
            try:
                time.sleep(self.refresh_delay_secs)
                self.look()
            except KeyboardInterrupt:
                print("Finished")
                break
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Unhandled Exception: {e}")

def system_command(*args):
    subprocess.run([a for a in args])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "Watcher")
    parser.add_argument("file", type = Path, help = "the tex file to compile")
    args = parser.parse_args()

    if not args.file.exists():
        raise FileNotFoundError("Couldn't find {args.file}")

    watcher = Watcher(args.file, system_command, "pdftex", args.file, "-interaction=nonstopmode")
    watcher.watch()
