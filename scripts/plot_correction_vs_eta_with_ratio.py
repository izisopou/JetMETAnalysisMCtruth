import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_correction_vs_eta_with_ratio.py --jetCone 4 --jetAlgo puppi --MC1 Summer23 --MC2 Summer23BPix' 

    parser = ArgumentParser(description='Script that plots the response correction factors of two sets vs eta, and their ratio',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
            
    parser.add_argument("-MC1", "--MC1", dest="mc_campaign_1", type=str, required=True,
                    help="Specify first MC campaign", metavar="MCCAMPAIGN1")                
                    
    parser.add_argument("-MC2", "--MC2", dest="mc_campaign_2", type=str, required=True,
                    help="Specify second MC campaign", metavar="MCCAMPAIGN2")
    
                                                                                     
    args = parser.parse_args()

    pt_indices_values = [(10, 0), (15, 1), (20, 2), (30, 3), (50, 4), (100, 5), (300, 6), (500, 7), (1000, 8), (3000, 9)]

    for pt, idx in pt_indices_values:
    
        print('Processing pt = ' + str(int(pt)) + ' GeV')
        
        if(abs(pt-3000)<1e-6): eta_range = 1.305
        if(abs(pt-1000)<1e-6): eta_range = 2.5
        if(abs(pt-500)<1e-6):  eta_range = 2.853
        if(abs(pt-300)<1e-6):  eta_range = 3.489
        if(abs(pt-100)<1e-6):  eta_range = 4.363
        if(pt < 100):          eta_range = 5.191
        
        root_filename_1 = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/Corrections/L2L3Correction_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_1 + '.root' 
        root_filename_2 = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/Corrections/L2L3Correction_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_2 + '.root' 
        
        print('Processing file 1: ' + root_filename_1)
        print('Processing file 2: ' + root_filename_2)
        
        root_file_1 = rt.TFile(root_filename_1, 'READ')
        root_file_2 = rt.TFile(root_filename_2, 'READ')
                
        hist_filename = ('EtaSF_' + str(int(idx)))
        
        print('Processing histogram: ' + hist_filename)
        
        hist_1 = root_file_1.Get(hist_filename)
        hist_2 = root_file_2.Get(hist_filename)
        
    
        c1 = rt.TCanvas('c1_' + str(int(pt)), 'c1_' + str(int(pt)), 900, 1000)
        c1.cd()
        c1.Draw()
        
        top_panel = rt.TPad('top_panel_' + str(int(pt)), 'top_panel_' + str(int(pt)), 0, 0.42, 1, 0.95)
        top_panel.SetTickx(1)
        top_panel.SetTicky(1)
        top_panel.SetRightMargin(0.02)
        top_panel.SetLeftMargin(0.12)
        top_panel.SetTopMargin(0.08)
        top_panel.SetBottomMargin(0.001)
        top_panel.Draw()
        
        bottom_panel = rt.TPad('bottom_panel_' + str(int(pt)), 'bottom_panel_' + str(int(pt)), 0, 0., 1, 0.4)
        bottom_panel.SetTickx(1)
        bottom_panel.SetTicky(1)
        bottom_panel.SetGridx(1)
        bottom_panel.SetGridy(1)
        bottom_panel.SetRightMargin(0.02)
        bottom_panel.SetLeftMargin(0.12)
        bottom_panel.SetTopMargin(0.)
        bottom_panel.SetBottomMargin(0.2)
        bottom_panel.Draw()
        
        top_panel.cd()

        top_frame = top_panel.DrawFrame(-5.191, 0.85, 5.191, 2.5 if(pt < 100) else 1.75)
        top_frame.GetXaxis().SetTitle('#eta^{rec}')
        top_frame.GetXaxis().SetTitleSize(0)
        top_frame.GetXaxis().SetTitleOffset(1.05)
        top_frame.GetXaxis().SetLabelSize(0)
        top_frame.GetXaxis().SetNdivisions(15, 5, 0)
        top_frame.GetYaxis().SetTitle('Jet response correction factor (C_{R})')
        top_frame.GetYaxis().SetTitleSize(0.065)
        top_frame.GetYaxis().SetTitleOffset(0.8)
        top_frame.GetYaxis().SetLabelSize(0.05)
        
        cms = rt.TPaveText(0.213, 0.945, 0.413, 0.965, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.08)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        lumi = rt.TPaveText(0.847, 0.945, 0.937, 0.965, "NDC")
        lumi.AddText('(13.6 TeV)')
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.07)
        lumi.SetBorderSize(0)
        lumi.SetFillColor(0)
        lumi.Draw()
    
        info_leg = rt.TPaveText(0.15,0.71,0.25,0.86,"NDC")
        info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        info_leg.AddText('p_{T}^{rec} = ' + str(int(pt)) + ' GeV')     
        info_leg.SetFillColor(0)
        info_leg.SetShadowColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextSize(0.06)
        info_leg.SetTextAlign(11)
        info_leg.Draw()
    
    
        hist_1.SetDirectory(0)
        hist_1.SetStats(0)
        hist_1.SetTitle('')               
        hist_1.SetLineWidth(2)
        hist_1.SetLineColor(rt.kRed-4) 
        hist_1.GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
        
        hist_2.SetDirectory(0)
        hist_2.SetStats(0)
        hist_2.SetTitle('')               
        hist_2.SetLineWidth(2)
        hist_2.SetLineColor(rt.kBlue-4)
        hist_2.GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
        
        hist_1.Draw('HIST SAME ][')   
        hist_2.Draw('HIST SAME ][') 
        
        legend = rt.TLegend(0.42,0.715,0.67,0.865,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.06)
        legend.SetBorderSize(0)       
        legend.AddEntry(hist_1, args.mc_campaign_1, 'L')  
        legend.AddEntry(hist_2, args.mc_campaign_2, 'L')   
        legend.Draw()
        
        
        bottom_panel.cd()
        
        bottom_frame = top_panel.DrawFrame(-5.191, 0.851, 5.191, 1.149)
        bottom_frame.GetXaxis().SetTitle('#eta^{rec}')
        bottom_frame.GetXaxis().SetTitleSize(0.10)
        bottom_frame.GetXaxis().SetTitleOffset(0.9)
        bottom_frame.GetXaxis().SetLabelSize(0.07)
        bottom_frame.GetXaxis().SetNdivisions(15, 5, 0)
        bottom_frame.GetYaxis().SetTitle('Ratio')
        bottom_frame.GetYaxis().SetTitleSize(0.10)
        bottom_frame.GetYaxis().SetTitleOffset(0.6)
        bottom_frame.GetYaxis().SetLabelSize(0.07)
        bottom_frame.GetYaxis().CenterTitle(1)
                
        
        hist_ratio = hist_2.Clone()
        hist_ratio.Divide(hist_1)
        hist_ratio.SetDirectory(0)
                       
        hist_ratio.SetLineWidth(2)
        hist_ratio.SetLineColor(rt.kBlack)
        hist_ratio.GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
        
        ratio_legend = rt.TLegend(0.37,0.88,0.62,0.92,"")
        ratio_legend.SetTextFont(42)
        ratio_legend.SetTextSize(0.06)
        ratio_legend.SetBorderSize(0)       
        ratio_legend.AddEntry(hist_ratio, args.mc_campaign_2 + '/' + args.mc_campaign_1, 'L')     
        ratio_legend.Draw() 
        
        line_horiz = rt.TLine(-5.191, 1.0, 5.191, 1.0)
        line_horiz.SetLineWidth(2)
        line_horiz.SetLineStyle(rt.kDashed)
        line_horiz.SetLineColor(rt.kRed)
        line_horiz.Draw()
        
        hist_ratio.Draw('HIST SAME ][') 
        
        

        output_png = '../ForAN/ResponseCorrectionFactor_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_1 + '_vs_' + args.mc_campaign_2 + '_Pt' + str(int(pt)) + 'GeV.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
