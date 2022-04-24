import concurrent.futures
import glob
import os
from pathlib import Path
import sys
import logging
from time import time
from time import time

logging.basicConfig(level=logging.INFO, format=None)
logger = logging.getLogger(__name__)

from libs.pattern_searcher import PatternSearcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

IGNORED_FILE_TYPE_EXTENSIONS = frozenset([".md", ".gz", ".bz2", ".zip", ".pdf", ".jpg", ".png", ".txt", ".css", ".pyc"])
IGNORED_FOLDERS = frozenset(["node_modules", "Library", "Envs"])
IGNORED_FILES = lambda x: not x.suffix in IGNORED_FILE_TYPE_EXTENSIONS

THREAD_COUNT = 1
MAX_DEPTH = 10

class HydraParser(object):
    def __list_files_in_dir(self, dirname):
        try:
            entries = [i.resolve() for i in Path(dirname).iterdir()]
            return list(filter(IGNORED_FILES, entries))
        except Exception as e:
            logger.error("Exception occurred: {}", e)
            sys.exit(1)

    def get_home_dir(self):
        return str(Path.home())
    
    def accessible(self, dir):
        return os.path.isdir(dir) and os.access(dir, os.R_OK) and not os.path.basename(dir).startswith(".") \
            and not any([os.path.basename(dir).startswith(i) for i in IGNORED_FOLDERS])

    
    def build_directory_index(self, dir):
        t1 = time()
        results = self._fast_scandir(dir)
        t2 = time()
        print("Time required to build directory index: {} seconds".format((t2-t1)))
        return results
    
    def _fast_scandir(self, dirname):
        if not dirname:
            return []
        if not self.accessible(dirname):
            return []
        subfolders= [f.path for f in os.scandir(dirname) if os.path.isdir(f.path)]
        
        for dirname in list(subfolders):
            subfolders.extend(self._fast_scandir(dirname))
        return subfolders

    def recursively_get_files(self, dirname, results, level_count):
        if level_count == MAX_DEPTH or not self.accessible(dirname):
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
        pattern_searcher = PatternSearcher(pattern)
        results = list(filter(lambda f: os.path.isfile(f), glob.iglob("{}{}**".format(os.path.abspath(dirname), os.path.sep), recursive=True)))
        chunksize = 512
        logger.info("Processing all files under {} in chunks of {} files".format(dirname, chunksize))

        # run parallel searches using a concurrent process pool executor
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            futures = executor.map(pattern_searcher.search_in_file, results, chunksize=int(chunksize))
            for future in futures:
                yield future or  {}
