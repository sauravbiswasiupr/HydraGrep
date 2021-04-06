import os
from queue import Queue
import logging
from time import time

from taskrunner import TaskRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HydraParser(object):
    def __list_files_in_dir(self, dirname):
        try:
            entries = [dirname + "/" + i for i in os.listdir(dirname)]
            filter_fn = lambda x: all([not os.path.isdir(x),
                                       not x.endswith(".md"),
                                       not x.endswith(".gz"),
                                       not x.endswith(".bz2")])
            files = filter(filter_fn, entries)
            files = list(files)
            return files
        except Exception as e:
            print("Exception occurred: {}").format(e)
            raise Exception(e)

    def search(self, dirname, pattern):
        t1 = time()
        queue = Queue()
        files = self.__list_files_in_dir(dirname)
        thread_count = 4 # len(files)

        for x in range(thread_count):
            runner = TaskRunner(queue)
            runner.daemon = True
            runner.start()

        for file in files:
            logger.info("Queuing file: {}".format(file))
            queue.put((file, pattern))

        queue.join()
        t2 = time()
        print("Searching for {} in the directory {} took {} seconds".format(pattern, dirname, (t2-t1)))


if __name__ == "__main__":
    parser = HydraParser()
    parser.search("/var/log", "saurav")