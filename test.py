from HydraParser import HydraParser
import sys

if __name__ == "__main__":
    dirname = sys.argv[1]
    pattern = sys.argv[2]
    hydra = HydraParser()

    occurrences = hydra.search(dirname, pattern)
