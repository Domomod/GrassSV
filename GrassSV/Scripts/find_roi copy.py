import logging 

class region_of_interest:
    def __init__(self, chromosome, start):
        self.chromosome = chromosome
        self.start = start
        self.end = start

    def set_end(self, end):
        self.end = end

class depthFileParser():
    def __init__(self):
        self.current_roi = None   

    def parseDepthLine(self, line):
        try:
            chromosome, position, depth = line.split()
            return chromosome, int(position), int(depth)
        except ValueError as e:
            logging.exception(
                f"[ValueError] parseDepthLine(): expected a line consisting of 3 words. Recieved '{line}' instead."
            )

    def find_roi(self, inputPath, outputPath, maxCoverage, marginSize=150, minSize=1):
        self.margin_size = marginSize
        self.minSize = minSize
        prevChromosome, prevPosition, prevDepth = None, None, None 
        with open(inputPath, "r") as depthCoverageFile:
            for line in depthCoverageFile:
                chromosome, position, depth = self.parseDepthLine(line)
                if (    depth < maxCoverage
                    and self.current_roi == None
                    ):
                    self.current_roi = region_of_interest(chromosome, position)
                elif    depth < maxCoverage:
                    self.add_to_roi(chromosome, position)
                prevChromosome, prevPosition, prevDepth = chromosome, position, depth
        if self.current_roi != None:
            self.save_self.current_roi()

    def add_to_roi(self, chromosome, position):
        if (    self.current_roi.chromosome == chromosome 
            and position <= self.current_roi.end + self.margin_size + 1
                # The '+ 1' ensures that two recrods, that have a gap between the size of `margin_size` 
                # will be saved as one consecutive region, as they would overlap when we extend their ends 
                # by the `margin_size`. Below example with `margin_size` set to 2:
                # ....[  A  ]..[  B  ]....
                # ..[ extend A]...........
                # ...........[ extend B]..
            ):
            self.current_roi.set_end(position)
        else:
            self.save_current_roi()
            self.current_roi = region_of_interest(chromosome, position)

    def save_current_roi(self):
        # The reported region of interest should be at least the size of `minSize` before extending by `marginSize`
        if (    (self.current_roi.end - self.current_roi.start) <= self.minSize
            ):
            start_margin_applied = max(0, self.current_roi.start - self.margin_size)

            # The reported end coordinate may extend after the true end of the chromosome
            # We allow this, because we only need those coordinates to later check if a read
            # overlaps with a reported region of interest. 
            end_margin_applied = self.current_roi.end + self.margin_size
            outputFile.write(f"{self.current_roi.chromosome}\t{self.current_roi.start}\t{self.current_roi.end}\n")
            self.current_roi = None

def run(input_path, output_path, limit_coverage, margin_size, minimum_size):
    with (  open(output_file, "w+") as outputFile,
            open(inputPath, "r") as inputFile
         ):
         dfParser = depthFileParser()
         dfParser.find_roi(inputFile, outputFile, limit_coverage, margin_size, minimum_size)

