#!/bin/bash
CONN=/home/utcausr/mp7sw/connection_files/connections-b40.xml
address=ugmt
root_path=/home/utcausr/uGMTScripts/ugmt_patterns/zs_test
work_path=$root_path/batch_run_`date +%Y%m%d_%H%M%S`
tmp_path=$root_path/tmp
ROMENU_FILE=$root_path/../mp7_test/ugmt_ro_zs_menu.py
patterns=$root_path/paths/rx_paths.txt

e=0-71

if [ -z ${1+x} ]; then 
	valid=nv
else
	valid=$1
fi

# setup work environment
mkdir -p $tmp_path
mkdir $work_path
mkdir $work_path/error_events

#make list of files to unpack and inject and save it in paths/rx_paths.txt
python $root_path/paths/lists_tx_rx.py

#loop over $patterns
while read rxfile
do
	rm $tmp_path/uncompressed.txt
		
	#magic method to unpack files zipped in python
	printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - $rxfile | gzip -dc > $tmp_path/uncompressed.txt
	
	#mp7butler.py -c $CONN reset $address --clksrc=internal # comment this line if the ZS is configured with SWATCH
	
	#inject uncompressed rx file
	mp7butler.py -c $CONN -v xbuffers $address tx PlayOnce -e $e --inject file://$tmp_path/uncompressed.txt
	mp7butler.py -c $CONN txmgts -e $e --loopback --pattern=none $address
	mp7butler.py -c $CONN rxmgts -e $e $address
	mp7butler.py -c $CONN rxalign -e $e --to-bx 7,5 $address
	mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 0-3 --rxBank 1 --rx 36-71 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
	mp7butler.py -c $CONN rosetup $address --internal --bxoffset 2
	mp7butler.py -c $CONN romenu $address $ROMENU_FILE standardMenu
	#mp7butler.py -c $CONN zsmenu $address $ROMENU_FILE zsStandardMenu # comment this line if the ZS is configured with SWATCH
	#bash setup_zs.sh
	
	echo Pattern:	$rxfile >> $work_path/summary.txt
	echo Bx:	Status: >> $work_path/summary.txt
	
	for i in {14..132}
	do
		#disable zs menu
		mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 0 &>/dev/null
		mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $tmp_path/output_nozs.dat &>/dev/null
		
		#enable zs menu and check whether it is enabled (there were some problems with this)
		mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
		en="$(mp7butler.py -c $CONN -l inspect $address readout.readout_zs.csr.ctrl.en)"

		until [ ${en:(-1)} == 1 ]
		do
			mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
			#mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.ctrl.val_mode
			en="$(mp7butler.py -c $CONN -l inspect $address readout.readout_zs.csr.ctrl.en)"
			echo Zero suppression status ${en:(-1)}
		done

		mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $tmp_path/output_zs.dat &>/dev/null

		#choose normal or validation mode
		if [ $valid == 'v' ]; then
			python $root_path/check_zs_mask_valid.py $tmp_path/output_nozs.dat $tmp_path/output_zs.dat $work_path $i $rxfile
		else
			python $root_path/check_zs_mask.py $tmp_path/output_nozs.dat $tmp_path/output_zs.dat $work_path $i $rxfile
		fi
		echo Bx $i/132 complete
	done
	echo Pattern $rxfile completed
done < $patterns

#script to do short summary in summary.txt file
python $root_path/zs_summary.py $work_path

tail -4 $work_path/summary.txt
echo Test completed
