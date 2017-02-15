import sys

ones, zeros = 0, 0

with open( sys.argv[1]+'/summary.txt', 'a+' ) as summ:
	for line in summ:
		if line[0].isdigit():
			try:
				status = line.strip().split( '\t' )[1].strip()
				if status == '0':
					zeros += 1
				else:
					ones += 1
			except:
				print line
				continue
	print >>summ, '-'*30, '\nSuccesses:\t', ones, '\t', round( 100*ones/float(ones + zeros), 2 ), '%\nFailures:\t', zeros, '\t', round( 100*zeros/float(ones + zeros), 2 ), '%\nSum:\t', ones + zeros
