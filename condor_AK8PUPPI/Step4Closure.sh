#!/bin/sh --login

#BSUB -q 1nh

WorkDir=$1
File=$2
Output=$3
ID=$4

source $WorkDir/Setup_CMSSW.sh

cp $WorkDir/Files/Summer23_V1/L2L3_output/*.txt .
cp $WorkDir/Files/Summer23_V1/L2L3_output/My*.root .

echo Input files are: $File

hadd -k -f Input.root `echo $File | tr ':' ' '`

# if you apply both L1 and L2L3 txt files then:
#
# -levels 1 2
#
# if you apply only the L2L3 txt file then:
#
# -levels 2
#
# if you don't want to apply any txt file then remove the line entirely.

jet_correction_analyzer_x \
   -inputFilename Input.root \
   -outputDir ./ \
   -path $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK8PUPPI/ \
   -era Summer23_V1_MC \
   -levels 2 \
   -useweight false \
   -algs ak8puppi \
   -drmax 0.4 \
   -evtmax 0 \
   -MCPUReWeighting MyMCPUHisto_Run3Summer23_PremixedPU.root \
   -DataPUReWeighting MyDataPUHisto_2023_erasC_100Bins.root \
   -nbinsrelrsp 60 \
   -relrspmin 0.0 \
   -relrspmax 3.0 \
   -nrefmax 3 \
   -doDZcut true \
   -doNMcut true \
   -doVetoMap true \
   -JetVetoMapRootName JetVetoMap_2023C.root \
   -JetVetoMapHistName jetvetomap_all

cp Closure_ak8puppi.root ${Output}/Closure_ak8puppi${ID}.root

rm *.root

