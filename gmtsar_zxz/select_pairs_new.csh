#!/bin/csh -f

# Select pairs according to the given threshold in time and baseline
# # used for time series analysis

#Zhao Xuan, Nov 16 2023 

  if ($#argv != 4) then
    echo ""
    echo "Usage: select_pairs.csh baseline_table.dat threshold_time_min threshold_time_max threshold_baseline"
    echo "  generate the input file for intf_tops.csh with given threshold of time and baseline"
    echo ""
    echo "  outputs:"
    echo "    intf.in baseline.ps baseline.pdf"
    echo ""
    exit 1
  endif  

  set file = $1
  set dt1 = `echo $2 | awk '{print $0}'`
  set dt2 = `echo $3 | awk '{print $0}'`
  set db = `echo $4 | awk '{printf $0}'`
  
  # which select_pairs.py
  set pygmtsar = '/home/xuanz/bin/gmtsar_z' 
  # loop over possible pairs
    rm intf.in


  python $pygmtsar/select_pairs.py $file $dt1 $dt2 $db


  awk '{print 2014+$3/365.25, $5, $1}' < $1 > text
  set region = `gmt gmtinfo text -C | awk '{print $1-0.5, $2+0.5, $3-50, $4+50}'`
  gmt pstext text -JX8.8i/6.8i -R$region[1]/$region[2]/$region[3]/$region[4] -D0.2/0.2 -X1.5i -Y1i -K -N -F+f8,Helvetica+j5 > baseline.ps
  gmt psxy tmp -R -J -K -O >> baseline.ps

  awk '{print $1,$2}' < text > text2
  gmt psxy text2 -Sp0.2c -G0 -R -JX -Ba0.5:"year":/a50g00f25:"baseline (m)":WSen -O >> baseline.ps
  gmt psconvert baseline.ps -Tg
  
  rm baseline.ps 
  #rm tmp b_line2
  rm text text2
