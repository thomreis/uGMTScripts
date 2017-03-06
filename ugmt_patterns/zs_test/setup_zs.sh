#!/bin/bash
CONNFILE=/home/utcausr/mp7sw/connection_files/connections-b40.xml
BOARD=ugmt
root_path=/home/utcausr/uGMTScripts/ugmt_patterns/zs_test
ROMENU_FILE=$root_path/../mp7_test/ugmt_ro_zs_menu.py

mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.csr.ctrl.en 1
mp7butler.py -c $CONNFILE rosetup $BOARD --internal --bxoffset 2
mp7butler.py -c $CONNFILE romenu $BOARD $ROMENU_FILE standardMenu
mp7butler.py -c $CONNFILE zsmenu $BOARD $ROMENU_FILE zsStandardMenu
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.csr.ctrl.val_mode 0xc0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.csr.ctrl.cap_en  0x6
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.addr 6
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x000001ff
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x000001ff
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x000001ff
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0003fc00
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0003fc00
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0003fc00
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x00000000

#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
#mp7butler.py -c $CONNFILE write $BOARD readout.readout_zs.ram.mask_data 0x0
