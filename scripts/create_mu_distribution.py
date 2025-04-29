import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 create_mu_distribution.py --era Run3Winter25'

    parser = ArgumentParser(description='Script extracting the pileup (mu) distribution of an MC dataset',epilog=usage)
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")         

    args = parser.parse_args()
    
    fout_name = '../Histos_PU/MyMCPUHisto_' + args.era + '_PremixedPU.root'
    fout = rt.TFile(fout_name, 'RECREATE')
    
    path_pattern = '/eos/cms/store/group/phys_jetmet/ilias/Run3MCtruthSamples/NoRawPtCut/' + args.era + '/*/PremixedPU/*/0000/JRA_*.root'
    file_list = glob.glob(path_pattern)
    file_list.sort()
    tree = rt.TChain('ak4puppi/t')
    
    for f in file_list:
        print(f'Adding file: {f}')
        tree.Add(f)
    
    print(f'Number of files = {len(file_list)}')

    tnpus = rt.std.vector('float')()

    tree.SetBranchAddress('tnpus', rt.AddressOf(tnpus))

    pileup = rt.TH1F('pileup', '', 120, 0., 120.)

    print(f'Entries = {tree.GetEntries()}')

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if (i % 1000000 == 0):
            print(f"Processed {i} / {tree.GetEntries()} events")

        if len(tnpus) > 12:
            pileup.Fill(tnpus[12])


    print('Writing output file: ' + fout_name)

    fout.cd()
    pileup.Write()
    

if __name__ == '__main__':
    main()
