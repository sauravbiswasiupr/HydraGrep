from pathlib import Path
import sys
from queue import Queue
import logging
from time import time

from taskrunner import TaskRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

IGNORED_FILE_TYPE_EXTENSIONS = frozenset([".md", ".gz", ".bz2", ".zip", ".pdf", ".jpg", ".png"])
IGNORED_FILES = lambda x: not x.suffix in IGNORED_FILE_TYPE_EXTENSIONS

THREAD_COUNT = 16
MAX_DEPTH = 4

class HydraParser(object):
    def __list_files_in_dir(self, dirname):
        try:
            entries = [i.resolve() for i in Path(dirname).iterdir()]
            return list(filter(IGNORED_FILES, entries))
        except Exception as e:
            logger.error("Exception occurred: {}", e)
            sys.exit(1)
    
    def recursively_get_files(self, dirname, results, level_count):
        if level_count == MAX_DEPTH:
            return
        
        files = self.__list_files_in_dir(dirname)
        for file in files:
            if file.is_dir():
                self.recursively_get_files(file, results, level_count + 1)
            else:
                results.append(file)

    def search(self, dirname, pattern):
        t1 = time()
        queue = Queue()
        results = list()
        self.recursively_get_files(dirname, results, 0)

        for x in range(THREAD_COUNT):
            runner = TaskRunner(queue)
            runner.daemon = True
            runner.start()

        for file in results:
            queue.put((file, pattern))

        queue.join()
        t2 = time()
        print("Searching for {} in the directory {} took {} seconds".format(pattern, dirname, (t2-t1)))


if __name__ == "__main__":
    parser = HydraParser()
    parser.search("/Users/saurav/Projects", "test")