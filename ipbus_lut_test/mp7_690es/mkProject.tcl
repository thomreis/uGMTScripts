# Autogenerated project build script
# Tue Apr  1 12:29:33 2014

project new top
source /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/mp7_690es.tcl
source /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/common/firmware/cfg/settings_v7.tcl
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/ipbus_package.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_data_types.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_null_algo/firmware/hdl/mp7_payload.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_reg_types.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_readout/firmware/hdl/mp7_readout_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/syncreg_r.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/syncreg_w.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_syncreg_v.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_readout/firmware/hdl/fake_roc.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_readout/firmware/hdl/mp7_readout.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_mezzanine/firmware/hdl/mezzanine_out_lvds.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/ngc/gth_quad_wrapper_jj.ngc
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/cgn/virtex7_rx_buf.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b virtex7_rx_buf.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/virtex7_rx_buf.xco
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/ultimate_crc_1_0/rtl/vhdl/ucrc_par.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/ultimate_crc_1_0/rtl/vhdl/ucrc_pkg.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/sc_protocol/ext_align_gth_spartan.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/common/drp_mux.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/packages/package_utilities.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/packages/package_types.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/packages/package_links.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/gth_10g/quad_wrapper_gth.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/gth_10g/mgt_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/freq_ctr_div.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_drp_bridge.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/drp_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/ipbus_fabric_sel.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_links/firmware/hdl/gth_10g/mp7_mgt.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_counters_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/bunch_ctr.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_ported_dpram36.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_ctrlreg_v.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_util/firmware/hdl/del_array.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_daqmux.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_derand.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_chan_buffer.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_new_buffers.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_counters.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/ipbus_decode_mp7_datapath.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_datapath/firmware/hdl/mp7_datapath.vhd
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/cgn/ttc_history_fifo.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b ttc_history_fifo.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/ttc_history_fifo.xco
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/freq_ctr.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ttc_history.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ttc_decoder.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ttc_ctrs.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ttc_cmd.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ttc_clocks.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/ipbus_decode_mp7_ttc.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ttc/firmware/hdl/mp7_ttc.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/ipbus_trans_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/ipbus_reg_v.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/opencores_i2c/firmware/hdl/i2c_master_bit_ctrl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/opencores_i2c/firmware/hdl/i2c_master_byte_ctrl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/opencores_i2c/firmware/hdl/i2c_master_registers.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/opencores_i2c/firmware/hdl/i2c_master_top.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/opencores_i2c/firmware/hdl/ipbus_i2c_master.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_xpoint/firmware/hdl/xpoint.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_xpoint/firmware/hdl/mp7_xpoint.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ctrl/firmware/hdl/board_id.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ctrl/firmware/hdl/ipbus_decode_mp7_ctrl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_ctrl/firmware/hdl/mp7_ctrl.vhd
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/cgn/tri_mode_eth_mac_v5_5.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b tri_mode_eth_mac_v5_5.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/tri_mode_eth_mac_v5_5.xco
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/cgn/gtwizard_v2_5_gbe_gth.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b gtwizard_v2_5_gbe_gth.xco -p coregen.cgp >& coregen.out
cd ..
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/cgn/gig_eth_pcs_pma_v11_5.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b gig_eth_pcs_pma_v11_5.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/gig_eth_pcs_pma_v11_5.xco
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth_gt.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth/example_design/gtwizard_v2_5_gbe_gth_gtrxreset_seq.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth/example_design/gtwizard_v2_5_gbe_gth_sync_block.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth/example_design/gtwizard_v2_5_gbe_gth_rx_startup_fsm.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth/example_design/gtwizard_v2_5_gbe_gth_tx_startup_fsm.vhd
xfile add ipcore_dir/gtwizard_v2_5_gbe_gth/example_design/gtwizard_v2_5_gbe_gth_init.vhd
xfile add ipcore_dir/gig_eth_pcs_pma_v11_5/example_design/gig_eth_pcs_pma_v11_5_sync_block.vhd
xfile add ipcore_dir/gig_eth_pcs_pma_v11_5/example_design/gig_eth_pcs_pma_v11_5_reset_sync.vhd
xfile add ipcore_dir/gig_eth_pcs_pma_v11_5/example_design/gig_eth_pcs_pma_v11_5_block.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/gen_hdl/gig_eth_pcs_pma_v11_5/gig_eth_pcs_pma_v11_5_transceiver_gth.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/hdl/emac_hostbus_decl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_eth/firmware/hdl/eth_7s_1000basex_gth.vhd
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/cgn/sdpram_32x9_16x10.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b sdpram_32x9_16x10.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/sdpram_32x9_16x10.xco
exec mkdir -p ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/cfg/coregen.cgp ipcore_dir
exec cp /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/cgn/sdpram_16x10_32x9.xco ipcore_dir
cd ipcore_dir
exec coregen -r -b sdpram_16x10_32x9.xco -p coregen.cgp >& coregen.out
cd ..
xfile add ipcore_dir/sdpram_16x10_32x9.xco
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/uc_pipe_interface.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/uc_spi_interface.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_slaves/firmware/hdl/trans_buffer.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_infra/firmware/hdl/uc_if.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_util/firmware/hdl/ipbus_clock_div.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/ipbus_stretcher.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/transactor_cfg.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/transactor_sm.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/transactor_if.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/transactor.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/trans_arb.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_txtransactor_if_simple.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_tx_mux.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_status_buffer.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_rxtransactor_if_simple.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_rxram_shim.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_rxram_mux.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_rarp_block.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_packet_parser.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_ipaddr_block.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_dualportram_tx.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_dualportram_rx.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_dualportram.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_do_rx_reset.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_clock_crossing_if.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_byte_sum.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_build_status.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_build_resend.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_build_ping.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_build_payload.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_build_arp.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_buffer_selector.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/udp_if_flat.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_core/firmware/hdl/ipbus_ctrl.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/ipbus_util/firmware/hdl/clocks_7s_serdes.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_infra/firmware/hdl/ipbus_decode_mp7_infra.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/components/mp7_infra/firmware/hdl/mp7_infra.vhd
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/common/firmware/ucf/area_constraints.ucf
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/common/firmware/ucf/clock_constraints.ucf
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/common/firmware/ucf/mp7_pins.ucf
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/ucf/mp7.ucf
xfile add /home/scratch/vhdl/uGMT/dev/ipbus_lut_test/cactusupgrades/boards/mp7/base_fw/mp7_690es/firmware/hdl/mp7_690es.vhd
project set top rtl top
project close
