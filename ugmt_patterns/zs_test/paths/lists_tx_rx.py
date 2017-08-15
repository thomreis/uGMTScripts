import os

#patterns_root = '/home/utcausr/test_patterns/TTJets_13TeV_RunIISpring16DR80_PUSpring16'
#patterns_root = '/home/utcausr/test_patterns/TT_13TeV_RunIIFall15DR76-25nsFlat10to25TSG'
patterns_root = '/home/utcausr/test_patterns/JPsiToMuMu_Pt20to120_EtaPhiRestricted'
#patterns_root = '/home/utcausr/test_patterns/TT_TuneCUETP8M1_13TeV'
files_tx = list()
files_rx = list()

for f in os.listdir( patterns_root ):
	if f.startswith( 'tx' ): 
		files_tx.append( os.path.join( patterns_root, f ) )
	elif f.startswith( 'rx' ):
		files_rx.append( os.path.join( patterns_root, f ) )
	else:
		continue
files_tx.sort()
files_rx.sort()


if not len(files_tx) == len(files_rx):
	print 'Number of RX and TX files not the same'
	quit()

with open( '/home/utcausr/uGMTScripts/ugmt_patterns/zs_test/paths/tx_paths.txt', 'w' ) as tx_f:
	for f in files_tx:
		tx_f.write( f + '\n'  )

with open( '/home/utcausr/uGMTScripts/ugmt_patterns/zs_test/paths/rx_paths.txt', 'w' ) as rx_f:
	for f in files_rx:
		rx_f.write( f + '\n' )
