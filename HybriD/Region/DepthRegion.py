class DepthRegion:
    def __init__(self, chromosome: str, start: int, end: int):
        self.chromosome = chromosome
        self.start = start
        self.end = end

    def __sub__(self, other):
        if self == other:
            return 0
        return self.start - other.end

    def __gt__(self, other):
        if self.chromosome != other.chromosome:
            return False
        if self == other:
            return False
        return self.start - other.end > 0

    def __lt__(self, other):
        if self.chromosome != other.chromosome:
            return False
        if self == other:
            return False
        return self.start - other.end < 0

    def __eq__(self, other):
        if self.chromosome != other.chromosome:
            return False
        return (other.start <= self.start <= other.end) or (other.start <= self.end <= other.end)

    def __repr__(self):
        return self.chromosome + "\t" + str(self.start) + '\t' + str(self.end) + '\n'

    def __str__(self):
        return self.__repr__()
