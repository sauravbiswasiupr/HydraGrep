import concurrent.futures
from pathlib import Path
import sys
import logging
from time import time
from argparse import ArgumentParser

from pattern_searcher import PatternSearcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

IGNORED_FILE_TYPE_EXTENSIONS = frozenset([".md", ".gz", ".bz2", ".zip", ".pdf", ".jpg", ".png", ".js", ".txt", ".css"])
IGNORED_FILES = lambda x: not x.suffix in IGNORED_FILE_TYPE_EXTENSIONS
OPTIMIZED_CHUNKSIZE = 500

THREAD_COUNT = 1
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
            if file.parts[-1].startswith("."):
                continue
            elif file.is_dir():
                self.recursively_get_files(file, results, level_count + 1)
            else:
                results.append(file)

    def search(self, dirname, pattern):
        t1 = time()
        results = list()
        self.recursively_get_files(dirname, results, 0)
        print("results: ", len(results))
        pattern_searcher = PatternSearcher(pattern)
        # run parallel searches using a concurrent process pool executor
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(pattern_searcher.search_in_file, results, chunksize=OPTIMIZED_CHUNKSIZE)

        t2 = time()
        print("Searching for {} in the directory {} took {} seconds".format(pattern, dirname, (t2-t1)))


if __name__ == "__main__":
    hydra = HydraParser()
    parser = ArgumentParser()
    parser.add_argument('-d', dest='basedir', default='.', help='Directory to invoke hydragrep')
    parser.add_argument('-p', dest='pattern', default='bazinga', help='Pattern to search')
    args = parser.parse_args()
    hydra.search(args.basedir, args.pattern)