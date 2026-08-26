import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob
import shutil


def main():
    usage = 'Example: python3 create_input_histos_for_pu_offset.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V2_PhiIndependent --JEC 0 --DivByPt 1'

    parser = ArgumentParser(description='Script extracting the pileup (mu) distribution of an MC dataset',epilog=usage)
    
    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")
                   
    parser.add_argument("-v", "--version", dest="version", type=str, required=True,
                    help="Specify version", metavar="VERSION")  
                    
    parser.add_argument("-div", "--DivByPt", dest="div_by_pt", type=int, choices=[0, 1], required=True,
                    help="Specify if offset is divided by pt (0: No, 1: Yes)", metavar="DIVBYPT")   
                    
    parser.add_argument("-jec", "--JEC", dest="jec", type=int, choices=[0, 1], required=True,
                    help="Specify if JECs are applied (0: No, 1: Yes)", metavar="JEC")                                                      

    args = parser.parse_args()
    
    #Get the root file that contains the distribution for mu = 0
    root_file_name_mu0 = '../condor_AK' + str(args.jet_cone) + args.jet_algo.upper() + '/Files/' + args.era + '_' + args.version + '/Offset' + ('After' if args.jec else 'Without') + 'L1_mu0/' + ('DividedByPt' if args.div_by_pt else 'NotDividedByPt') + '/canvases_synchplot_ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '.root'    
    root_file_mu0 = rt.TFile(root_file_name_mu0, 'READ')
    
    #Get the standard root file and open it so that we can save the distributions for mu = 0 here
    old_name = '../condor_AK' + str(args.jet_cone) + args.jet_algo.upper() + '/Files/' + args.era + '_' + args.version + '/Offset' + ('After' if args.jec else 'Without') + 'L1/' + ('DividedByPt' if args.div_by_pt else 'NotDividedByPt') + '/canvases_synchplot_ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '.root'
    new_name = '../Offset/Offset' + ('After' if args.jec else 'Without') + 'L1' + ('OverPt' if args.div_by_pt else '') + 'VsPt_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.era + '.root'
    
    shutil.copy(old_name, new_name)
    
    root_file = rt.TFile(new_name, 'UPDATE')
    
    eta_regions = ['BB', 'EI', '1EO', '2EO', 'FF']
    
    for eta_region in eta_regions:
        hist = root_file_mu0.Get('histograms/OffMeantnpuRef_' + eta_region + '_0')
        hist.SetName('OffMeantnpuRef_' + eta_region + '_Mu0')
        root_file.cd('histograms')
        hist.Write()
    
    root_file.Close()        
    
    print('Copied root file ' + old_name +' to ' + new_name)
    print('Used root file for mu = 0: ' + root_file_name_mu0)
    print('Wrote histograms for mu = 0 to: ' + new_name)
    

if __name__ == '__main__':
    main()
