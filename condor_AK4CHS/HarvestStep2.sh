#!/bin/sh

source $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Setup_FileLocation.sh

hadd -k -f $Step2Output/output_ak4pfchs.root $Step2Output/Result_*.root

 jet_synchfit_x \
   -inputDir  $Step2Output/ \
   -outputDir `pwd`/Files/Summer23_V1/L1_output/ \
   -algo1 ak4pfchs \
   -algo2 ak4pfchs \
   -highPU false \
   -useNPU false \
   -functionType ak4 \
   -era Summer23_V1_MC



