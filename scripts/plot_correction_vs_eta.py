import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_correction_vs_eta.py --jetCone 4 --jetAlgo puppi' 

    parser = ArgumentParser(description='Script that plots the response correction factors vs eta',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
                    
                                                                                     
    args = parser.parse_args()

    pt_indices_values = [(10, 0), (15, 1), (20, 2), (30, 3), (50, 4), (100, 5), (300, 6), (500, 7), (1000, 8), (3000, 9)]

    for pt, idx in pt_indices_values:
    
        print('Processing pt = ' + str(int(pt)) + ' GeV')
    
        c1 = rt.TCanvas("c1", "c1", 800, 700)
        c1.SetLogy(0)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetRightMargin(0.04)
        c1.SetLeftMargin(0.12)
        c1.SetTopMargin(0.10)
        c1.SetBottomMargin(0.13)

        frame = c1.DrawFrame(-5.191, 0.85, 5.191, 2.5 if(pt < 100) else 1.75)
        frame.GetXaxis().SetTitle('#eta^{rec}')
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.05)
        frame.GetXaxis().SetLabelSize(0.04)
        frame.GetXaxis().SetNdivisions(15, 5, 0)
        frame.GetYaxis().SetTitle('Jet response correction factor (C_{R})')
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.15)
        frame.GetYaxis().SetLabelSize(0.035)
        
        cms = rt.TPaveText(0.265, 0.91, 0.465, 0.95, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.065)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        lumi = rt.TPaveText(0.81, 0.91, 0.93, 0.95, "NDC")
        lumi.AddText('(13.6 TeV)')
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.05)
        lumi.SetBorderSize(0)
        lumi.SetFillColor(0)
        lumi.Draw()
    
        info_leg = rt.TPaveText(0.15,0.76,0.25,0.86,"NDC")
        info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        info_leg.AddText('p_{T}^{rec} = ' + str(int(pt)) + ' GeV')     
        info_leg.SetFillColor(0)
        info_leg.SetShadowColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextSize(0.04)
        info_leg.SetTextAlign(11)
        info_leg.Draw()
    
        legend = rt.TLegend(0.42,0.66,0.67,0.86,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.SetBorderSize(0)
    
    
        eras = ['Summer22', 'Summer22EE', 'Summer23', 'Summer23BPix', 'RunIII2024Summer24']
        colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2, rt.kViolet, rt.kOrange+1]    
    
    
        for era, color in zip(eras, colors):
         
            if(era=='RunIII2024Summer24' and (args.jet_cone==8 or args.jet_algo.lower()=='chs')): continue

            root_filename = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/Corrections/L2L3Correction_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + era + '.root' 
        
            print('Processing file: ' + root_filename)
        
            root_file = rt.TFile(root_filename, 'READ')
                
            hist_filename = ('EtaSF_' + str(int(idx)))
        
            print('Processing histogram: ' + hist_filename)
        
            hist = root_file.Get(hist_filename)
                    
            hist.SetDirectory(0)
            hist.SetStats(0)
            hist.SetTitle('')               
            hist.SetLineWidth(2)
            hist.SetLineColor(color) 
            
            if(abs(pt-3000)<1e-6): eta_range = 1.305
            if(abs(pt-1000)<1e-6): eta_range = 2.5
            if(abs(pt-500)<1e-6):  eta_range = 2.853
            if(abs(pt-300)<1e-6):  eta_range = 3.489
            if(abs(pt-100)<1e-6):  eta_range = 4.363
            if(pt < 100):          eta_range = 5.191
            
            hist.GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
            
            hist.Draw('HIST SAME ][')
        
            legend.AddEntry(hist, era, 'L')     
                
                      
        legend.Draw()
        

        output_png = '../ForAN/ResponseCorrectionFactor_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_Pt' + str(int(pt)) + 'GeV.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
