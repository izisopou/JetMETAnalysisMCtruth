#!/bin/sh --login

#BSUB -q 1nh

WorkDir=$1
File=$2
Output=$3
ID=$4

source $WorkDir/Setup_CMSSW.sh

cp $WorkDir/Files/Summer23_V1/L1L2L3_output/*.txt .
cp $WorkDir/Files/Summer23_V1/L1L2L3_output/*.root .

echo Input files are: $File

hadd -k -f Input.root `echo $File | tr ':' ' '`

jet_correction_analyzer_x \
   -inputFilename Input.root \
   -outputDir ./ \
   -path $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/ \
   -era Summer23_V1_MC \
   -levels 1 2 \
   -useweight false \
   -algs ak4pfchs \
   -drmax 0.2 \
   -evtmax 0 \
   -nbinsrelrsp 60 \
   -relrspmin 0.0 \
   -relrspmax 3.0 \
   -MCPUReWeighting MyMCPUHisto_Run3Summer23_PremixedPU.root \
   -DataPUReWeighting MyDataPUHisto_2023_erasC_100bins.root \
   -nrefmax 3 \
   -doDZcut true \
   -doNMcut false \
   -doVetoMap false \
   -JetVetoMapRootName JetVetoMap_2023C.root \
   -JetVetoMapHistName jetvetomap_all

cp Closure_ak4pfchs.root ${Output}/Closure_ak4pfchs${ID}.root

rm *.root

