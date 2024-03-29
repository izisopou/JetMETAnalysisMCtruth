#!/bin/sh --login

#BSUB -q 1nh

WorkDir=$1
Files=$2
Output=$3
ID=$4

source $WorkDir/Setup_CMSSW.sh

cp $WorkDir/L2L3_output/*.txt .
cp $WorkDir/L2L3_output/My*.root .

echo Input files are: $Files

hadd -k -f Input.root `echo $Files | tr ':' ' '`

# We do not have L1 corrections for PUPPI so the following lines are commented out

#jet_apply_jec_x \
#   -input Input.root \
#   -output JRA_jecl1.root \
#   -jecpath ./ \
#   -era Winter22Run3 \
#   -levels 1 \
#   -algs ak8puppi \
#   -L1FastJet true \
#   -saveitree false

cp $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/config/jra_dr_finebinning.config jra.config

jet_response_analyzer_x jra.config \
   -input Input.root \
   -nbinsabsrsp 0 \
   -nbinsetarsp 0 \
   -nbinsphirsp 0 \
   -nbinsrelrsp 60 \
   -doflavor false \
   -flavorDefinition phys \
   -MCPUReWeighting MyMCPUHisto_Winter22Run3_Flat2018_PremixedPU.root \
   -MCPUHistoName pileup \
   -DataPUReWeighting MyDataPUHisto_2022.root \
   -DataPUHistoName pileup \
   -output jra.root \
   -useweight false \
   -nrefmax 3 \
   -algs ak8puppi \
   -drmax 0.4 \
   -relrspmin 0.0 \
   -relrspmax 3.0 \
   -doDZcut true \
   -doNMcut true

cp jra.root ${Output}/JRA_jecl1${ID}.root

rm *.root


