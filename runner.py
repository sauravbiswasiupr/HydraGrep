from argparse import ArgumentParser
import logging
from termcolor import colored

logging.basicConfig(level=logging.INFO, format=None)
logger = logging.getLogger(__name__)

from libs.hydragrep import HydraParser


if __name__ == "__main__":
    hydra = HydraParser()
    parser = ArgumentParser()
    parser.add_argument('-d', dest='basedir', default='.', help='Directory to invoke hydragrep')
    parser.add_argument('-p', dest='pattern', default='bazinga', help='Pattern to search')
    args = parser.parse_args()
    for res in hydra.search(args.basedir, args.pattern):
        if res.get("occurrences"):
            filename = "[{}]".format(res["file"])
            occurrences = res["occurrences"]
            logger.info(colored(filename, 'blue'))
            for i in occurrences:
                logger.info(i.replace(args.pattern, colored(args.pattern, 'green')))
