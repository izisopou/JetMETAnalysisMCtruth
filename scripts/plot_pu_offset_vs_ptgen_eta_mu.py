import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_pu_offset_vs_ptgen_eta_mu.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --JEC 1 --DivByPt 1' 

    parser = ArgumentParser(description='Script that plots the pu offset vs pt, eta and mu for a specific MC dataset and jet collection',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
                    
    parser.add_argument("-jec", "--JEC", dest="jec", type=int, choices=[0, 1], required=True,
                    help="Specify if JECs are applied (0: No, 1: Yes)", metavar="JEC") 
                    
    parser.add_argument("-div", "--DivByPt", dest="div_by_pt", type=int, choices=[0, 1], required=True,
                    help="Specify if offset is divided by pt (0: No, 1: Yes)", metavar="DIVBYPT")                   
                    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")                     
                                                                                       
    args = parser.parse_args()
         
    
    root_file_name = '../Offset/Offset' + ('After' if args.jec else 'Without') + 'L1' + ('OverPt' if args.div_by_pt else '') + 'VsPt_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.era + '.root'
    
    root_file = rt.TFile(root_file_name, 'READ')
    
    print('Root file used: ' + root_file_name)
    
    
    etabins = ['BB', 'EI', '1EO', '2EO','FF']
    
    for etabin in etabins:
    
        if etabin == 'BB':
            etaleg = '0.0 < |#eta| < 1.3'
        elif etabin == 'EI':
            etaleg = '1.3 < |#eta| < 2.4'
        elif etabin == '1EO':
            etaleg = '2.4 < |#eta| < 2.7'
        elif etabin == '2EO':
            etaleg = '2.7 < |#eta| < 3.0'
        else:
            etaleg = '3.0 < |#eta| < 5.0'  
            
        
        if args.div_by_pt:
            if args.jet_algo.lower() == 'puppi':
                ymin = -9.9
                ymax = 25
                if etabin == '2EO' : ymax = 60                
            if args.jet_algo.lower() == 'chs':
                if not args.jec:
                    ymin = -9.9
                    ymax = 130
                    if etabin == 'FF': ymax = 300
                    if (etabin == '1EO' or etabin == '2EO'): ymax = 240
                else:
                    ymin = -9.9
                    ymax = 25
        else:
            if args.jet_algo.lower() == 'puppi':
                ymin = -9.9
                ymax = 20
                if etabin == '2EO' : ymax = 40
            if args.jet_algo.lower() == 'chs':
                if not args.jec:
                    ymin = -14.9
                    ymax = 50
                else:
                    ymin = -9.9
                    ymax = 20           
                                    
        
        c1 = rt.TCanvas("c1", "c1", 50, 50, 600, 600)
        c1.SetLogy(0)
        c1.SetLogx(1)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetRightMargin(0.03)
        c1.SetLeftMargin(0.15)
        c1.SetTopMargin(0.07)
        c1.SetBottomMargin(0.13)

        frame = c1.DrawFrame(8, ymin, 5500, ymax)
        frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.05)
        frame.GetYaxis().SetTitle('Average Offset / p_{T}^{ptcl} [%]' if args.div_by_pt else 'Average Offset [GeV]')
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.35)
        frame.GetXaxis().SetLabelSize(0)
        frame.GetYaxis().SetLabelSize(0.035)
    
        cms = rt.TPaveText(0.145, 0.938, 0.145, 0.955, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextAlign(11)
        cms.SetTextSize(0.06)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        lumi = rt.TPaveText(0.868, 0.938, 0.975, 0.955, "NDC")
        lumi.AddText('(13.6 TeV)')
        lumi.SetTextFont(42)
        lumi.SetTextAlign(31)
        lumi.SetTextSize(0.04)
        lumi.SetBorderSize(0)
        lumi.SetFillColor(0)
        lumi.Draw()
    
        #info_leg = rt.TPaveText(0.73, 0.25 if(args.jet_algo.lower() == 'chs' and not args.jec) else  0.15, 0.93, 0.38 if(args.jet_algo.lower() == 'chs' and not args.jec) else  0.28, "NDC")
        info_leg = rt.TPaveText(0.27, 0.64, 0.47, 0.87, "NDC")
        info_leg.SetFillColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextAlign(11)
        info_leg.SetTextSize(0.04)
        info_leg.AddText(args.era)
        info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        info_leg.AddText(etaleg)
        info_leg.AddText('With' + ('out' if not args.jec else ' L1') + ' JECs applied')
        info_leg.Draw()
    
        xlab = rt.TLatex()
        xlab.SetTextAlign(22)
        xlab.SetTextSize(0.05)
        xlab.SetTextFont(42)
        xlab.SetTextSize(0.04)
        
        labels = ['10', '30', '100', '300', '1000', '3000']
        
        for label in labels:
           xlab.DrawLatex(float(label), ymin-0.025*(ymax-ymin), label)
    
        line_horiz = rt.TLine(8, 0, 5500, 0)
        line_horiz.SetLineWidth(2)
        line_horiz.SetLineStyle(rt.kDashed)
        line_horiz.Draw()
        
        if args.jet_algo.lower() == 'puppi' or (args.jet_algo.lower() == 'chs' and args.jec):
            line_horiz_minus = rt.TLine(8, -2, 5500, -2)
            line_horiz_minus.SetLineWidth(2)
            line_horiz_minus.SetLineStyle(rt.kDotted)
            line_horiz_minus.Draw()
            line_horiz_plus = rt.TLine(8, 2, 5500, 2)
            line_horiz_plus.SetLineWidth(2)
            line_horiz_plus.SetLineStyle(rt.kDotted)
            line_horiz_plus.Draw()
    
        legend = rt.TLegend(0.65,0.64,0.94,0.90,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.SetBorderSize(0)

        mubins = ['Mu0', '0', '1', '2', '3', '4']
        mulegs = ['#mu #approx 0', '0 #leq #mu < 20', '20 #leq #mu < 40', '40 #leq #mu < 60', '60 #leq #mu < 80', '80 #leq #mu < 100']
        colors = [rt.kBlack, rt.kRed+1, rt.kBlue-4, rt.kGreen-3, rt.kOrange+1, rt.kViolet] 
    
        for mubin, muleg, color in zip(mubins, mulegs, colors):
        
            if mubin == '4': continue
                        
            hist_name = 'histograms/OffMeantnpuRef_' + etabin + '_' + mubin    
        
            hist = root_file.Get(hist_name)
        
            print('Hist file used: ' + hist_name)
        
            hist.SetDirectory(0)
            if args.div_by_pt: hist.Scale(100)
            hist.SetTitle('')
            hist.SetStats(0)
            hist.SetMarkerColor(color)
            hist.SetMarkerSize(1.0)
            hist.SetMarkerStyle(rt.kFullCircle)
            hist.SetLineColor(color)
            hist.GetXaxis().SetRangeUser(10, 5500)
            
            if not args.div_by_pt:
                for x in range(1,hist.GetNbinsX()+1):
                    if(hist.GetBinError(x)>2): hist.SetBinContent(x,-999)
        
            hist.Draw('PE SAME')
        
            legend.AddEntry(hist, muleg, 'LPE')
        
        
        legend.Draw()    
  

        output_png = '../Offset/plots/Offset' + ('After' if args.jec else 'Without') + 'L1' + ('OverPt' if args.div_by_pt else '') + 'VsPt_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + args.era + '_' + etabin + '.png'  
        output_pdf = output_png.replace('.png', '.pdf')

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
