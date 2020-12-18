#!/usr/bin/python
import re
import numpy as np
import statistics
def contig_read(path, output, console):
	with open(path) as file:
		rawdata = file.read()
		contigs = re.split('>alignment[0-9]+',rawdata)
		lengths = [len(cont) for cont in contigs]
		quantiles = [0.25, 0.5, 0.75]
		quantile_values = [np.percentile(contigs, q) for q in quantiles]
		mn = statistics.mean(lengts)
		msg = f"""
		Mean:\t{mn}
		Percentiles -
		-0.25:\t{quantile_values[0]}
		-0.5:\t{quantile_values[1]}
		-0.75:\t{quantile_values[2]}"""
		if console:
			print(msg)
#TODO: if output

if __name__ == "__main__":
	contig_read(sys.argv[1],False,True)
