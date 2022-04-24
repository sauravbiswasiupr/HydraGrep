import re

class PatternSearcher:
    def __init__(self, pattern):
        self.pattern = re.compile("\n.*{}.*\n".format(pattern))

    def search_in_file(self, log_file):
        try:
            f = open(log_file, encoding="utf-8")
            return { "file": str(log_file), "occurrences": re.findall(self.pattern, f.read()) }
        except Exception as e:
            return None
