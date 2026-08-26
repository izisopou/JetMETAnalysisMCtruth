#!/bin/sh

source $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Setup_FileLocation.sh

hadd -k -f $Step3Output/Merged.root $Step3Output/JRA_*root

jet_l2_correction_x \
   -input $Step3Output/Merged.root \
   -algs ak4pfchsl1 \
   -era Summer23_V1_MC \
   -output l2.root \
   -outputDir Files/Summer23_V1/L1L2L3_output/ \
   -makeCanvasVariable AbsCorVsJetPt:JetEta \
   -l2l3 true \
   -batch true \
   -histMet median \
   -delphes false \
   -maxFitIter 30 \
   -l2calofit DynamicMin \
   -l2pffit standard+Gaussian \
   -ptclipfit true \

mv Files/Summer23_V1/L1L2L3_output/Summer23_V1_MC_L2Relative_AK4PFchsl1.txt Files/Summer23_V1/L1L2L3_output/Summer23_V1_MC_L2Relative_AK4PFchs.txt

