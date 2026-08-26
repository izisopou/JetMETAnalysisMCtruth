import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_correction_vs_eta_vs_jetAlgo_with_ratio.py --MC Winter25' 

    parser = ArgumentParser(description='Script that plots the response correction factors of an MC campaign vs eta for the three jet algos, and their ratio',epilog=usage)
            
    parser.add_argument("-MC", "--MC", dest="mc_campaign", type=str, required=True,
                    help="Specify MC campaign", metavar="MCCAMPAIGN")
    
                                                                                     
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
        
        jet_algos = ['ak4puppi', 'ak8puppi', 'ak4pfchs']
        jet_algos_names = ['AK4 PUPPI', 'AK8 PUPPI', 'AK4 CHS']
        colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2]  
    
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
        #bottom_panel.SetGridy(1)
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
        
        cms = rt.TPaveText(0.22, 0.948, 0.42, 0.968, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.08)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        lumi = rt.TPaveText(0.92, 0.935, 0.99, 0.955, "NDC")
        lumi.AddText(args.mc_campaign + ' (13.6 TeV)')
        lumi.SetTextFont(42)
        lumi.SetTextAlign(31)
        lumi.SetTextSize(0.07)
        lumi.SetBorderSize(0)
        lumi.SetFillColor(0)
        lumi.Draw()
    
        info_leg = rt.TPaveText(0.15,0.71,0.25,0.86,"NDC")
        info_leg.AddText('p_{T}^{rec} = ' + str(int(pt)) + ' GeV')     
        info_leg.SetFillColor(0)
        info_leg.SetShadowColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextSize(0.06)
        info_leg.SetTextAlign(11)
        info_leg.Draw()
        
        legend = rt.TLegend(0.42,0.715,0.67,0.865,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.06)
        legend.SetBorderSize(0)   
        
        hist_i = 0
        
        hist = [None] * len(jet_algos)
        
        for jet_algo, jet_algo_name, color in zip(jet_algos, jet_algos_names, colors):
        
            root_filename = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/Corrections/L2L3Correction_' + jet_algo_name.replace(" ", "") + '_' + args.mc_campaign + '.root' 
            print('Processing file: ' + root_filename)
            
            root_file = rt.TFile(root_filename, 'READ')
            
            hist_filename = ('EtaSF_' + str(int(idx)))
        
            print('Processing histogram: ' + hist_filename)
        
            hist[hist_i] = root_file.Get(hist_filename)
        
            hist[hist_i].SetDirectory(0)
            hist[hist_i].SetStats(0)
            hist[hist_i].SetTitle('')               
            hist[hist_i].SetLineWidth(2)
            hist[hist_i].SetLineColor(color) 
            hist[hist_i].GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
        
            hist[hist_i].Draw('HIST SAME ][')  
                   
            legend.AddEntry(hist[hist_i], jet_algo_name, 'L')  
            
            hist_i = hist_i + 1   
        
        legend.Draw()
        
        
        bottom_panel.cd()
        
        bottom_frame = bottom_panel.DrawFrame(-5.191, 0.821, 5.191, 1.179)
        bottom_frame.GetXaxis().SetTitle('#eta^{rec}')
        bottom_frame.GetXaxis().SetTitleSize(0.10)
        bottom_frame.GetXaxis().SetTitleOffset(0.9)
        bottom_frame.GetXaxis().SetLabelSize(0.07)
        bottom_frame.GetXaxis().SetNdivisions(15, 5, 0)
        bottom_frame.GetYaxis().SetTitle('Ratios')
        bottom_frame.GetYaxis().SetTitleSize(0.10)
        bottom_frame.GetYaxis().SetTitleOffset(0.6)
        bottom_frame.GetYaxis().SetLabelSize(0.07)
        bottom_frame.GetYaxis().CenterTitle(1)
        
        ratio_legend = rt.TLegend(0.37,0.83,0.62,0.97,"")
        ratio_legend.SetTextFont(42)
        ratio_legend.SetTextSize(0.06)
        ratio_legend.SetBorderSize(0)
        
        line_horiz = rt.TLine(-5.191, 1.0, 5.191, 1.0)
        line_horiz.SetLineWidth(2)
        line_horiz.SetLineStyle(rt.kDashed)
        line_horiz.Draw()        
        line_horiz_minus = rt.TLine(-5.191, 0.99, 5.191, 0.99)
        line_horiz_minus.SetLineWidth(2)
        line_horiz_minus.SetLineStyle(rt.kDotted)
        line_horiz_minus.Draw()
        line_horiz_plus = rt.TLine(-5.191, 1.01, 5.191, 1.01)
        line_horiz_plus.SetLineWidth(2)
        line_horiz_plus.SetLineStyle(rt.kDotted)
        line_horiz_plus.Draw()
        
        ratio_hists = []
        
        for i in range(1, len(hist)):
                        
            hist_ratio = hist[i].Clone()
            hist_ratio.Divide(hist[0])
            hist_ratio.SetDirectory(0)
                       
            hist_ratio.SetLineWidth(2)
            hist_ratio.SetLineColor(rt.kMagenta if i==1 else rt.kCyan-7)
            hist_ratio.GetXaxis().SetRangeUser(-1.*eta_range, eta_range)
            hist_ratio.GetYaxis().SetRangeUser(0, 3)
            
            hist_ratio.Draw('HIST SAME ][') 
        
            ratio_legend.AddEntry(hist_ratio, jet_algos_names[i] + '/' + jet_algos_names[0], 'L') 
            
            ratio_hists.append(hist_ratio)
                
        ratio_legend.Draw()   
        
        print('HERE')      
        

        output_png = '../Plots/Corrections/ResponseCorrectionFactor_' + args.mc_campaign + '_' + '_vs_'.join(name.replace(' ', '') for name in jet_algos_names) + '_Pt' + str(int(pt)) + 'GeV.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
