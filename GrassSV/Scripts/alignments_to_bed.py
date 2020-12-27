
def export_to_bed(input_path, output_path):
    from GrassSV.Region.Load.csv_loader import correct_ref_name
    input = open(input_path, "r")

    with open(output_path, "w") as output:
        for line in input:
            line = line.split("\t")
            if (line[0].isnumeric()):

                chromosome=correct_ref_name(line[4])
                start=line[0]
                end=line[1]

                output.write(" ".join([
                    chromosome, start, end
                ]) + "\n")