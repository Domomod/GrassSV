class DepthRegion:
    def __init__(self, chromosome: str, start: int, end: int):
        self.chromosome = chromosome
        self.start = start
        self.end = end

    def __repr__(self):
        return self.chromosome + "\t" + str(self.start) + '\t' + str(self.end) + '\n'

    def __str__(self):
        return self.__repr__()
