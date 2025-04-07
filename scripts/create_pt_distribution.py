import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 create_pt_distribution.py --era Run3Winter25'

    parser = ArgumentParser(description='Script extracting the gen pt distribution of an MC dataset',epilog=usage)
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")         

    args = parser.parse_args()
    
    fout_name = '../Histos_Pt/GenPT_' + args.era + '_PremixedPU.root'
    fout = rt.TFile(fout_name, 'RECREATE')
    
    path_pattern = '/eos/cms/store/group/phys_jetmet/ilias/Run3MCtruthSamples/NoRawPtCut/' + args.era + '/*/PremixedPU/*/0000/JRA_*.root'
    file_list = glob.glob(path_pattern)
    file_list.sort()
    tree = rt.TChain('ak4puppi/t')
    
    for f in file_list:
        print(f'Adding file: {f}')
        tree.Add(f)
    
    print(f'Number of files = {len(file_list)}')

    AllGenJetsPt = rt.std.vector('float')()
    
    tree.SetBranchAddress('AllGenJetsPt', rt.AddressOf(AllGenJetsPt))

    nBins = 43
    Boundaries = array('d', [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 23, 27,
    30, 35, 40, 45, 57, 72, 90, 120, 150, 200, 300, 400, 550, 750, 1000,
    1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000])

    h_GenPT = rt.TH1F('h_GenPT', '', nBins, Boundaries)
    h_GenPT_3leading = rt.TH1F('h_GenPT_3leading', '', nBins, Boundaries)

    print(f'Entries = {tree.GetEntries()}')

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if (i % 1000000 == 0):
            print(f"Processed {i} / {tree.GetEntries()} events")

        for ijet, pt in enumerate(AllGenJetsPt):
            h_GenPT.Fill(pt)
            if ijet <= 2:
                h_GenPT_3leading.Fill(pt) 

    print('Writing output file: {fout_name}')

    fout.cd()
    h_GenPT.Write()
    h_GenPT_3leading.Write()
    

if __name__ == '__main__':
    main()
