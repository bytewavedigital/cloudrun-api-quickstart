import os
import sys
import re
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler


def on_modified(logger):
    def inner(event):
        if not re.search(r"/\.", event.src_path):
            logger.debug(f"{event.src_path} has been modified reloading.")
            os.execl(sys.executable, sys.executable, *sys.argv)

    return inner


def reload(file, logger):
    path = os.path.dirname(os.path.abspath(file))
    handler = RegexMatchingEventHandler([r".*"], [], False, True)
    handler.on_modified = on_modified(logger)
    my_observer = Observer()
    my_observer.schedule(handler, path, recursive=True)
    my_observer.start()
