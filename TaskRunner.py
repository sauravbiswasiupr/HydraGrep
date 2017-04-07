import re
from threading import Thread

from termcolor import colored


class TaskRunner(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            filename, pattern = self.queue.get()
            results = self.parse_log_for_pattern(filename, pattern)
            for i in results:
                print i.replace(pattern, colored(pattern, 'red'))

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
            print e
            return None

    def search(self, directory, pattern):
        try:
            results = []
            files = self.list_files_in_dir(directory)

            for file in files:
                search_res = self.parse_log_for_pattern(file, pattern)
                for res in search_res:
                    results.append(res)

            return results
        except Exception as e:
            print "Unexpected error occurred: {}".format(e)
