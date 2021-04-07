import re
from threading import Thread
import logging

from termcolor import colored

logging.basicConfig(level=logging.INFO, format=None)
logger = logging.getLogger(__name__)

class TaskRunner(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            filename, pattern = self.queue.get()
            results = self.parse_log_for_pattern(filename, pattern)
            if results:
                logger.info(colored(filename, 'green'))
                for i in results:
                    logger.info(i.replace(pattern, colored(pattern, 'red')))

            self.queue.task_done()

    def search_occurrences(self, pattern, text):
        p = re.compile(".*{}.*".format(pattern))
        occurrences = []

        for line in text:
            matches = p.search(line)
            if matches:
                occurrences.append(matches.group(0))

        return occurrences

    def parse_log_for_pattern(self, log_file, pattern):
        try:
            f = open(log_file)

            return self.search_occurrences(pattern, f.readlines())
        except Exception as e:
            print(e)
            return None
