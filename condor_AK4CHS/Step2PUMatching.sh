#!/bin/sh --login

#BSUB -q 1nh
export DISPLAY=localhost0.0
WorkDir=$1
NoPUFile=$2
PUFile=$3
Output=$4
ID=$5

source $WorkDir/Setup_CMSSW.sh

if [[ $NoPUFile != *":"* ]]; then
   cp $NoPUFile NoPUFile.root
else
   hadd -f -k NoPUFile.root `echo $NoPUFile | tr ':' ' '`
fi

if [[ $PUFile != *":"* ]]; then
   cp $PUFile PUFile.root
else
   hadd -f -k PUFile.root `echo $PUFile | tr ':' ' '`
fi

cp $WorkDir/Files/Summer23_V1/L1_output/*.txt .
cp $WorkDir/Files/Summer23_V1/L1_output/*.root .

echo Current directory content
ls
echo

jet_match_x \
   -basepath // \
   -samplePU PUFile.root \
   -sampleNoPU NoPUFile.root \
   -algo1 ak4pfchs \
   -algo2 ak4pfchs \
   -iftest false \
   -maxEvts 20000000 \
   -ApplyJEC true \
   -JECpar Summer23_V1_MC_L1FastJet_AK4PFchs.txt \
   -outputPath ./ \
   -npvRhoNpuBinWidth 20 \
   -NBinsNpvRhoNpu 6 \
   -useweight false \
   -nrefmax 3 \
   -doNotSave false \
   -doDZcut false \
   -doVetoMap true \
   -JetVetoMapName JetVetoMap_2023C.root

mv output_ak4pfchs.root ${Output}/Result_${ID}.root

# When you want to examine the raw pileup offset:
#   -ApplyJEC false \
#
# When you want to examine the corrected pileup offset:
#
#   -ApplyJEC true \
#   -JECpar Summer23_V1_MC_L1FastJet_AK4PFchs.txt \


