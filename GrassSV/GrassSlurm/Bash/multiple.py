#!/usr/bin/python3
import random
import string
import os
import sys

BED_FILE = ""
FILE = "/media/tmp/out.fsa"
TEMP_FILE = "/media/tmp/temp.fsa"
# FILE = "out.fsa"
# TEMP_FILE = "temp.fsa"
SIZE = 10000

class Chromosome:
    def __init__(self, tab):
        self.name = tab[0]
        self.length = int(tab[1])
        self.regions = []
        self.points = []

    def __str__(self):
        return self.name + ":" + str(self.length)

    def __repr__(self):
        return self.__str__()

    def generate_regions_points(self, how_much_regions, how_much_points, size):
        def point_in_regions(point_to_check):
            for region in self.regions:
                if region[0][0] <= point_to_check <= region[0][1]:
                    return True
            return False

        end = 0
        for i in range(how_much_regions):
            start = random.randint(end, end + size + int((self.length - end) / how_much_regions))
            end = start + size
            self.regions.append(((start, end), (start, end)))

        for _ in range(how_much_points):
            while point_in_regions(point := random.randint(size, self.length - size)):
                pass
            self.points.append((point, point))
        self.points = sorted(self.points)

    def move_points_and_regions(self, after, size):
        for i in range(len(self.regions)):
            region = self.regions[i]
            if region[1][0] > after:
                self.regions[i] = ((region[0][0], region[0][1]), (region[1][0] + size, region[1][1] + size))
        for i in range(len(self.points)):
            point = self.points[i]
            if point[1] > after:
                self.points[i] = (point[0], point[1] + size)


def load_chroms() -> [Chromosome]:
    with open("genome.lengths") as file:
        chrom = [Chromosome(chrom.split("\t")) for chrom in file.read().split("\n")]
    return chrom


def duplications(chromosomes):
    chromosome = random.choice(chromosomes)
    while len(chromosome.regions) == 0:
        chromosome = random.choice(chromosomes)
    region = chromosome.regions[0]
    start = region[1][0]
    end = start+SIZE
    chromosome.regions = chromosome.regions[1:]
    chromosome.move_points_and_regions(end, SIZE)
    comm = f"python3 $GRASSUTILS/fastadna.py {FILE} -v {chromosome.name} {start}:{end} | python3 $GRASSUTILS/fastadna.py {FILE} -i {chromosome.name} {start} > {TEMP_FILE}"
    os.system(comm)
    comm = f"cat {TEMP_FILE} > {FILE}"
    os.system(comm)
    log("DUP", chromosome.name, region[0][0], region[0][1])


def insert(chromosomes):
    chromosome = random.choice(chromosomes)
    while len(chromosome.points) == 0:
        chromosome = random.choice(chromosomes)
    start = chromosome.points[0]
    chromosome.points = chromosome.points[1:]
    chromosome.move_points_and_regions(start[1], SIZE)
    comm = f"python3 $GRASSUTILS/fastadna.py {FILE} -ir {chromosome.name} {start[1]} {SIZE} > {TEMP_FILE}"
    os.system(comm)
    comm = f"cat {TEMP_FILE} > {FILE}"
    os.system(comm)
    # log("INS", chromosome.name, start[0], SIZE)
    log(f"INS{SIZE}", chromosome.name, start[0] - 1, start[0] + 1)


def delete(chromosomes):
    chromosome = random.choice(chromosomes)
    while len(chromosome.regions) == 0:
        chromosome = random.choice(chromosomes)
    region = chromosome.regions[0]
    start = region[1][0]
    end = start+SIZE
    chromosome.regions = chromosome.regions[1:]
    chromosome.move_points_and_regions(end, -SIZE)
    comm = f"python3 $GRASSUTILS/fastadna.py {FILE} -d {chromosome.name} {start}:{end} > {TEMP_FILE}"
    os.system(comm)
    comm = f"cat {TEMP_FILE} > {FILE}"
    os.system(comm)
    log("DEL", chromosome.name, region[0][0], region[0][1])


def invert(chromosomes):
    chromosome = random.choice(chromosomes)
    while len(chromosome.regions) == 0:
        chromosome = random.choice(chromosomes)
    region = chromosome.regions[0]
    start = region[1][0]
    end = start+SIZE
    chromosome.regions = chromosome.regions[1:]
    comm = f"python3 $GRASSUTILS/fastadna.py {FILE} -r {chromosome.name} {start}:{end} > {TEMP_FILE}"
    os.system(comm)
    comm = f"cat {TEMP_FILE} > {FILE}"
    os.system(comm)
    log("INV", chromosome.name, region[0][0], region[0][1])


def translocate(chromosomes, which):
    chromosome = random.choice(chromosomes)
    while len(chromosome.regions) == 0 or len(chromosome.points) == 0:
        chromosome = random.choice(chromosomes)
    region = chromosome.regions[0]
    start = region[1][0]
    end = start+SIZE
    where_to = chromosome.points[0]
    chromosome.points = chromosome.points[1:]
    chromosome.regions = chromosome.regions[1:]
    chromosome.move_points_and_regions(end, -SIZE)
    chromosome.move_points_and_regions(where_to[1], SIZE)
    comm = f"python3 $GRASSUTILS/fastadna.py {FILE} -t {chromosome.name} {start}:{end} {where_to[1]} > {TEMP_FILE}"
    os.system(comm)
    comm = f"cat {TEMP_FILE} > {FILE}"
    os.system(comm)
    log(f"TRANS:FROM{which}", chromosome.name, region[0][0], region[0][1])
    log(f"TRANS:TO{which}", chromosome.name, where_to[0], SIZE)


def log(what, chromosom, start, end):
    chromosom = chromosom.replace("\\", "")
    with open(BED_FILE, "a+") as file:
        file.write(f"{chromosom} {start} {end} {what}\n")


if __name__ == '__main__':
    sv_type= int(sys.argv[1])
    FILE= sys.argv[2]
    TEMP_FILE= sys.argv[3]
    BED_FILE= sys.argv[4]
    chromosomes = load_chroms()
    point_num = 200 if sv_type==6 else 500
    for chromosome in chromosomes:
        region_num_per_chrom = int(chromosome.length / 15000)
        chromosome.generate_regions_points(region_num_per_chrom, int(point_num / len(chromosomes)) + 2, SIZE)
    much = 500 if sv_type!=-1 else 100
    SIZE = 0
    for i in range(much):
        if sv_type==6:
            SIZE += 500 if i % 10 == 0 else 0
        else:
            SIZE += 500 if i % 50 == 0 else 0
        if sv_type==1 or sv_type==6:
            duplications(chromosomes)
        if sv_type==2 or sv_type==6: 
            delete(chromosomes)
        if sv_type==3 or sv_type==6:
            translocate(chromosomes, i)
        if sv_type==4 or sv_type==6: 
            insert(chromosomes)
        if sv_type==5 or sv_type==6: 
            invert(chromosomes)
