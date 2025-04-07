import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_median_response_vs_ptptcl_with_ratio.py --jetCone 4 --jetAlgo puppi --MC1 Winter24 --MC2 Summer24 --JEC 0' 

    parser = ArgumentParser(description='Script that plots the median response vs ptptcl (gen pt) for two MC datasets and their ratio',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
            
    parser.add_argument("-MC1", "--MC1", dest="mc_campaign_1", type=str, required=True,
                    help="Specify first MC campaign", metavar="MCCAMPAIGN1")                
                    
    parser.add_argument("-MC2", "--MC2", dest="mc_campaign_2", type=str, required=True,
                    help="Specify second MC campaign", metavar="MCCAMPAIGN2")
                    
    parser.add_argument("-jec", "--JEC", dest="jec", type=int, choices=[0, 1], required=True,
                    help="Specify if JECs are applied (0: No, 1: Yes)", metavar="JEC")                  
    
                                                                                     
    args = parser.parse_args()

    eta_pairs = ['0, 1.3', '1.3, 2.4', '2.4, 2.7', '2.7, 3', '3, 5']
    
    for idx, eta_pair in enumerate(eta_pairs):
        eta_min, eta_max = eta_pair.split(', ')
    
        print('Processing abs eta bin [' + eta_min + ', ' + eta_max + ']')
        
        response_type = 'L1L2L3Closure' if args.jec else 'RawResponse'
        
        root_filename_1 = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/MedianResponses/' + response_type + 'VsPt_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_1 + '.root' 
        root_filename_2 = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/MedianResponses/' + response_type + 'VsPt_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_2 + '.root'
        
        print('Processing file 1: ' + root_filename_1)
        print('Processing file 2: ' + root_filename_2)
        
        root_file_1 = rt.TFile(root_filename_1, 'READ')
        root_file_2 = rt.TFile(root_filename_2, 'READ')
                
        hist_filename = 'ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '/ClosureVsRefPt_JetEta' + eta_min + 'to' + eta_max
        
        print('Processing histogram: ' + hist_filename)
        
        hist_1 = root_file_1.Get(hist_filename)
        hist_2 = root_file_2.Get(hist_filename)
        
    
        c1 = rt.TCanvas('c1_' + str(idx), 'c1_' + str(idx), 900, 1000)
        c1.cd()
        c1.Draw()
        
        top_panel = rt.TPad('top_panel_' + str(idx), 'top_panel_' + str(idx), 0, 0.42, 1, 0.95)
        top_panel.SetTickx(1)
        top_panel.SetTicky(1)
        top_panel.SetLogx(1)
        top_panel.SetRightMargin(0.02)
        top_panel.SetLeftMargin(0.12)
        top_panel.SetTopMargin(0.08)
        top_panel.SetBottomMargin(0.001)
        top_panel.Draw()
        
        bottom_panel = rt.TPad('bottom_panel_' + str(idx), 'bottom_panel_' + str(idx), 0, 0., 1, 0.4)
        bottom_panel.SetTickx(1)
        bottom_panel.SetTicky(1)
        bottom_panel.SetGridx(0)
        bottom_panel.SetGridy(0)
        bottom_panel.SetLogx(1)
        bottom_panel.SetRightMargin(0.02)
        bottom_panel.SetLeftMargin(0.12)
        bottom_panel.SetTopMargin(0.)
        bottom_panel.SetBottomMargin(0.27)
        bottom_panel.Draw()
        
        top_panel.cd()

        top_frame = top_panel.DrawFrame(8, 0.921 if args.jec else 0.65, 5500, 1.079 if args.jec else 1.19)
        top_frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
        top_frame.GetXaxis().SetTitleSize(0)
        top_frame.GetXaxis().SetTitleOffset(1.05)
        top_frame.GetXaxis().SetLabelSize(0)
        top_frame.GetXaxis().SetNdivisions(15, 5, 0)
        top_frame.GetYaxis().SetTitle('median(p_{T}^{rec} / p_{T}^{ptcl})')
        top_frame.GetYaxis().SetTitleSize(0.065)
        top_frame.GetYaxis().SetTitleOffset(0.8)
        top_frame.GetYaxis().SetLabelSize(0.05)
        
        cms = rt.TPaveText(0.235, 0.95, 0.435, 0.97, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.085)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        lumi = rt.TPaveText(0.847, 0.95, 0.937, 0.97, "NDC")
        lumi.AddText('(13.6 TeV)')
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.07)
        lumi.SetBorderSize(0)
        lumi.SetFillColor(0)
        lumi.Draw()
    
        info_leg = rt.TPaveText(0.73,0.05,0.93,0.20,"NDC")
        info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        info_leg.AddText(eta_min + ' < |#eta| < ' + eta_max)     
        info_leg.SetFillColor(0)
        info_leg.SetShadowColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextSize(0.075)
        info_leg.SetTextAlign(31)
        info_leg.Draw()
        
        jec_leg = rt.TPaveText(0.25,0.70,0.35,0.84,"NDC")
        if args.jec:
            jec_leg.AddText("JECs applied")
        else:
            jec_leg.AddText("No JECs")   
            jec_leg.AddText("applied")
        jec_leg.SetFillColor(0)
        jec_leg.SetBorderSize(0)
        jec_leg.SetTextSize(0.075)
        jec_leg.SetTextFont(42)
        jec_leg.SetTextAlign(21)
        jec_leg.Draw()
    
    
        hist_1.SetDirectory(0)
        hist_1.SetStats(0)
        hist_1.SetTitle('')               
        hist_1.SetLineWidth(2)
        hist_1.SetLineColor(rt.kAzure+8) 
        hist_1.SetMarkerColor(rt.kAzure+8)
        hist_1.SetMarkerStyle(rt.kFullCircle)
        hist_1.GetXaxis().SetRangeUser(10, 5500)
        
        hist_2.SetDirectory(0)
        hist_2.SetStats(0)
        hist_2.SetTitle('')               
        hist_2.SetLineWidth(2)
        hist_2.SetLineColor(rt.kSpring)
        hist_2.SetMarkerColor(rt.kSpring)
        hist_2.SetMarkerStyle(rt.kFullCircle)
        hist_2.GetXaxis().SetRangeUser(10, 5500)
        
        hist_1.Draw('PE1 SAME')   
        hist_2.Draw('PE1 SAME') 
        
        legend = rt.TLegend(0.64,0.67,0.84,0.86,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.075)
        legend.SetBorderSize(0)       
        legend.AddEntry(hist_1, args.mc_campaign_1, 'PE')  
        legend.AddEntry(hist_2, args.mc_campaign_2, 'PE')   
        legend.Draw()
        
        line_horiz = rt.TLine(8, 1.0, 5500, 1.0)
        line_horiz.SetLineWidth(2)
        line_horiz.SetLineStyle(rt.kDashed)
        line_horiz.Draw()
        
        if args.jec:
            line_horiz_minus = rt.TLine(8, 0.99, 5500, 0.99)
            line_horiz_minus.SetLineWidth(2)
            line_horiz_minus.SetLineStyle(rt.kDotted)
            line_horiz_minus.Draw()
            line_horiz_plus = rt.TLine(8, 1.01, 5500, 1.01)
            line_horiz_plus.SetLineWidth(2)
            line_horiz_plus.SetLineStyle(rt.kDotted)
            line_horiz_plus.Draw()
                
        
        bottom_panel.cd()
        
        bottom_frame = top_panel.DrawFrame(8, 0.971, 5500, 1.029)
        bottom_frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
        bottom_frame.GetXaxis().SetTitleSize(0.10)
        bottom_frame.GetXaxis().SetTitleOffset(1.1)
        bottom_frame.GetXaxis().SetLabelSize(0)
        bottom_frame.GetXaxis().SetNdivisions(306)
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
        hist_ratio.SetMarkerColor(rt.kBlack)
        hist_ratio.SetMarkerStyle(rt.kFullCircle)
        
        ratio_legend = rt.TLegend(0.37,0.84,0.62,0.96,"")
        ratio_legend.SetTextFont(42)
        ratio_legend.SetTextSize(0.06)
        ratio_legend.SetBorderSize(0)       
        ratio_legend.AddEntry(hist_ratio, args.mc_campaign_2 + '/' + args.mc_campaign_1, 'L')     
        ratio_legend.Draw() 
        
        line_horiz.Draw()
        
        hist_ratio.Draw('PE1 SAME') 
        
        xlab = rt.TLatex()
        xlab.SetTextAlign(22)
        xlab.SetTextSize(0.05)
        xlab.SetTextFont(42)
        xlab.SetTextSize(0.09)
        
        labels = ['10', '30', '100', '300', '1000', '3000']
        
        for label in labels:
            xlab.DrawLatex(float(label), 0.9665, label)
        
        
        jec_type = 'After' if args.jec else 'Before'

        output_png = '../ForAN/MedianResponseVsPt_' + jec_type + 'JECs_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.mc_campaign_1 + '_vs_' + args.mc_campaign_2 + '_AbsEta' + eta_min + 'to' + eta_max + '.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
