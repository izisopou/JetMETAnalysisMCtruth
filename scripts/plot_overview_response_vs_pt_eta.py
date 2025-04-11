import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_overview_response_vs_pt_eta.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V2_PhiIndependent --JEC 1 --ymin 0.92 --ymax 1.08' 

    parser = ArgumentParser(description='Script that plots the overview jet response vs pt and eta for a specific MC dataset and jet collection',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
                    
    parser.add_argument("-jec", "--JEC", dest="jec", type=int, choices=[0, 1], required=True,
                    help="Specify if JECs are applied (0: No, 1: Yes)", metavar="JEC")  
                    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")
                    
    parser.add_argument("-v", "--version", dest="version", type=str, required=True,
                    help="Specify version", metavar="VERSION")  
                                                                                 
    parser.add_argument("-ymin", "--ymin", dest="ymin", type=float, required=True,
                    help="Specify min Y axis value", metavar="YMIN")
    
    parser.add_argument("-ymax", "--ymax", dest="ymax", type=float, required=True,
                    help="Specify max Y axis value", metavar="YMAX")                
    
    args = parser.parse_args()
    
    type_corr = ('L1' if args.jet_algo.lower() == 'chs' else '')+'L2L3_Closure_VetoBPixAndFPixAreas' if args.jec else 'Response_NoCorrectionsApplied'
    
    root_file_name = '../condor_AK'+str(args.jet_cone)+args.jet_algo.upper()+'/Files/'+args.era+'_'+args.version+'/' + type_corr + '/ClosureVsRefPt.root'
    
    root_file = rt.TFile(root_file_name, 'READ')
    
    print('Root file used: ' + root_file_name)
    
    jet_dir_name = 'ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + ('l1' if args.jet_algo.lower() == 'chs' else '')
    
    c1 = rt.TCanvas("c1", "c1", 50, 50, 600, 600)
    c1.SetLogy(0)
    c1.SetLogx(1)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetRightMargin(0.03)
    c1.SetLeftMargin(0.15)
    c1.SetTopMargin(0.07)
    c1.SetBottomMargin(0.13)

    frame = c1.DrawFrame(8, args.ymin, 5500, args.ymax)
    frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(1.05)
    frame.GetYaxis().SetTitle('median(R) = median(p_{T}^{rec} / p_{T}^{ptcl})')
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(1.35)
    frame.GetXaxis().SetLabelSize(0)
    frame.GetYaxis().SetLabelSize(0.035)
    
    cms = rt.TPaveText(0.18, 0.775, 0.28, 0.865, "NDC")
    cms.AddText("#splitline{#bf{CMS}}{#splitline{#scale[0.7]{#it{Simulation}}}{#scale[0.7]{#it{Preliminary}}}}")
    cms.SetTextFont(42)
    cms.SetTextAlign(11)
    cms.SetTextSize(0.065)
    cms.SetBorderSize(0)
    cms.SetFillColor(0)
    cms.Draw()

    lumi = rt.TPaveText(0.868, 0.938, 0.975, 0.955, "NDC")
    lumi.AddText(args.era + ' (13.6 TeV)')
    lumi.SetTextFont(42)
    lumi.SetTextAlign(31)
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(0)
    lumi.SetFillColor(0)
    lumi.Draw()
    
    info_leg = rt.TPaveText(0.73, 0.15, 0.93, 0.25, "NDC")
    info_leg.SetFillColor(0)
    info_leg.SetBorderSize(0)
    info_leg.SetTextFont(42)
    info_leg.SetTextAlign(31)
    info_leg.SetTextSize(0.04)
    info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
    info_leg.AddText('With' + ('out' if not args.jec else '') + ' JECs applied')
    info_leg.Draw()
    
    xlab = rt.TLatex()
    xlab.SetTextAlign(22)
    xlab.SetTextSize(0.05)
    xlab.SetTextFont(42)
    xlab.SetTextSize(0.04)
        
    labels = ['10', '30', '100', '300', '1000', '3000']
        
    for label in labels:
       xlab.DrawLatex(float(label), args.ymin-0.025*(args.ymax-args.ymin), label)
    
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
    
    legend = rt.TLegend(0.63,0.68,0.92,0.90,"")
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.SetBorderSize(0)

    eta_pairs = ['0, 1.3', '1.3, 2.4', '2.4, 2.7', '2.7, 3', '3, 5']
    colors = [rt.kGreen+3, rt.kBlue-4, rt.kViolet, rt.kRed+1, rt.kOrange+1] 
    styles = [rt.kFullCircle, rt.kFullStar, rt.kFullSquare, rt.kFullTriangleUp, rt.kFullTriangleDown]
    sizes = [1.0, 1.3, 0.8, 1.0, 1.0]
    
    for eta_pair, color, style, size in zip(eta_pairs, colors, styles, sizes):
        
        eta_min, eta_max = eta_pair.split(', ')
                
        hist_name = jet_dir_name + '/ClosureVsRefPt_JetEta' + eta_min + 'to' + eta_max    
        
        hist = root_file.Get(hist_name)
        
        print('Hist file used: ' + hist_name)
        
        hist.SetDirectory(0)
        hist.SetTitle('')
        hist.SetStats(0)
        hist.SetMarkerColor(color)
        hist.SetMarkerSize(size)
        hist.SetMarkerStyle(style)
        hist.SetLineColor(color)
        hist.GetXaxis().SetRangeUser(10, 5500)
        
        hist.Draw('PE SAME')
        
        legend.AddEntry(hist, f'{float(eta_min):.1f} < |#eta| < {float(eta_max):.1f}', 'LPE')
        
        
    legend.Draw()    

    if args.jec:
        name = (('' if args.jet_algo.lower() == 'puppi' else 'L1') + 'L2L3ClosureVsPt')
    else:
        name = 'RawResponseVsPt' if args.jet_algo.lower() == 'puppi' else 'ResponseAfterL1VsPt'   

    output_png = '../OverviewPlots/' + name +  '_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.era + '_' + args.version + '.png'  
    output_pdf = output_png.replace('.png', '.pdf')

    c1.SaveAs(output_png)
    c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
