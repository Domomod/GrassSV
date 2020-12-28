from GrassSV.Region.BioRegion import Region


def load(filename):
    record_set = []
    with open(filename, 'r') as file:
        ref_idx = 0
        start_idx = 1
        end_idx = 2
        line = file.readline()
        i = 0
        while line:
            row = line.split()
            start = int(row[start_idx])
            end = int(row[end_idx])
            region = Region(start=start,
                            end=end,
                            ref=row[ref_idx],
                            region_name='RoI' + str(i),
                            region_type='RegionOfInterest',
                            qualifiers={"length": abs(end - start)}
                            )
            i += 1
            record_set.append(region)
            line = file.readline()

    return record_set


# Preview of functions declared inside this file
if __name__ == "__main__":
    record_set = load("data/regions-of-interest/duzyZeroCoverage")
    pass
