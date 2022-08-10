#!/usr/bin/python3
import re
import numpy as np
import statistics
import sys
def contig_read(path, output, console):
	with open(path) as file:
		rawdata = file.read()
		contigs = re.split('>alignment[0-9]+',rawdata)
		lengths = [len(cont) for cont in contigs[1::]]
		quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
		quantile_values = [np.percentile(lengths, q) for q in quantiles]
		mn = statistics.mean(lengths)
		msg = f"""
Mean:\t{mn}
Percentiles
-0.1:\t{quantile_values[0]}
-0.25:\t{quantile_values[1]}
-0.5:\t{quantile_values[2]}
-0.75:\t{quantile_values[3]}
-0.9:\t{quantile_values[4]}"""
		if console:
			print(msg)
#TODO: if output

#if __name__ == "__main__":#
#	contig_read(sys.argv[1],False,True)
