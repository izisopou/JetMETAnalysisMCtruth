import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser

def get_histogram_median_1d(hist, debug=False):
    if not hist:
        print("ERROR: The histogram is not defined.")
        return (0.0, 0.0)

    nbins = hist.GetXaxis().GetNbins()
    x = np.array([hist.GetXaxis().GetBinCenter(i+1) for i in range(nbins)])
    y = np.array([hist.GetBinContent(i+1) for i in range(nbins)])
    b = np.array([hist.GetXaxis().GetBinLowEdge(i+1) for i in range(nbins)])
    
    median = median_weighted(nbins, x, y, b, debug)
    
    # Error estimation using RMS and effective entries
    error = 1.253 * hist.GetRMS() / np.sqrt(hist.GetEffectiveEntries())
    
    if debug:
        print(f"Error: {error}")
        print(f"RMS: {hist.GetRMS()}")
        print(f"Entries: {hist.GetEffectiveEntries()}")
    
    return (median, error)

def median_weighted(n, a, w, boundaries, debug=False):
    if n <= 0 or a is None:
        return 0
    
    sorted_indices = np.argsort(a)
    a_sorted = a[sorted_indices]
    w_sorted = w[sorted_indices]
    boundaries_sorted = boundaries[sorted_indices]
    
    total_weight = np.sum(w_sorted)
    half_weight = total_weight / 2.0
    
    cumulative_sum = np.cumsum(w_sorted)
    median_index = np.searchsorted(cumulative_sum, half_weight)
    
    if boundaries is not None:
        lower_edge = boundaries_sorted[median_index]
        bin_width = 2 * (a_sorted[median_index] - lower_edge)
        median = lower_edge + (((half_weight - cumulative_sum[median_index - 1]) / w_sorted[median_index]) * bin_width)
    else:
        median = a_sorted[median_index]
    
    return median


def main():
    usage = 'Example: python3 plot_median_response_vs_ptptcl_bpix_fpix.py --jetCone 4 --jetAlgo puppi --MC RunIII2024Summer24 --version V2 --DoBPix 1 --DoFPix 1 --JECvsPhi 1' 

    parser = ArgumentParser(description='Script that plots the response correction factors vs eta',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
    
    parser.add_argument("-MC", "--MC", dest="mc", type=str, required=True,
                    help="Specify MC campaign", metavar="MC")
                   
    parser.add_argument("-v", "--version", dest="version", type=str, required=True,
                    help="Specify JEC version", metavar="VERSION")                
                    
    parser.add_argument("-jecVsPhi", "--JECvsPhi", dest="jec_vs_phi", type=int, choices=[0, 1], required=True,
                    help="Specify if phi-dependent JECs are applied (0: No, 1: Yes)", metavar="JECVSPHI")                     
    
    parser.add_argument("-bpix", "--DoBPix", dest="doBPix", type=int, required=True,
                    help="Specify if BPix area will be used", metavar="DOBPIX")
    
    parser.add_argument("-fpix", "--DoFPix", dest="doFPix", type=int, required=True,
                    help="Specify if FPix area will be used", metavar="DOFPIX")
                                                                                     
    args = parser.parse_args()
    
    jec_type = 'PhiDependent' if args.jec_vs_phi else 'PhiIndependent'
    
    if (args.doBPix and not args.doFPix):
        issue_type = 'ApplyToBPixArea'
        issues = ['BPix']
    elif (args.doFPix and not args.doBPix):
        issue_type = 'ApplyToFPixArea'
        issues = ['FPix']
    elif (args.doBPix and args.doFPix):
        issue_type = 'ApplyToBPixAndFPixAreas'
        issues = ['BPix', 'FPix']
    else:
        issue_type = ''
        issues = []
                
    
    Boundaries = array('d', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 23, 27, 30, 35, 40, 45, 57, 72, 90, 120, 150, 200, 300, 400, 550, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000])
    nBins = len(Boundaries) - 1   
       
    c1 = rt.TCanvas("c1", "c1", 800, 700)
    c1.SetLogy(0)
    c1.SetLogx(1)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetRightMargin(0.04)
    c1.SetLeftMargin(0.12)
    c1.SetTopMargin(0.10)
    c1.SetBottomMargin(0.13)

    frame = c1.DrawFrame(8, 0.901, 5500, 1.099)
    frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(1.05)
    frame.GetXaxis().SetLabelSize(0.)
    frame.GetXaxis().SetNdivisions(15, 5, 0)
    frame.GetYaxis().SetTitle('median(R) = median(p_{T}^{rec} / p_{T}^{ptcl})')
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
    
    mc_leg = rt.TPaveText(0.66,0.20,0.76,0.25, "NDC")
    mc_leg.AddText(args.mc + ' MC')
    mc_leg.SetTextFont(42)
    mc_leg.SetTextSize(0.05)
    mc_leg.SetBorderSize(0)
    mc_leg.SetFillColor(0)
    mc_leg.Draw()
            
    line_horiz = rt.TLine(8, 1.0, 5500, 1.0)
    line_horiz.SetLineWidth(2)
    line_horiz.SetLineStyle(rt.kDashed)
    line_horiz.Draw()
        
    line_horiz_minus = rt.TLine(8, 0.99, 5500, 0.99)
    line_horiz_minus.SetLineWidth(2)
    line_horiz_minus.SetLineStyle(rt.kDotted)
    line_horiz_minus.Draw()
    
    line_horiz_plus = rt.TLine(8, 1.01, 5500, 1.01)
    line_horiz_plus.SetLineWidth(2)
    line_horiz_plus.SetLineStyle(rt.kDotted)
    line_horiz_plus.Draw()       
    
    labels = ['10', '30', '100', '300', '1000', '3000']
        
    xlab = rt.TLatex()
    xlab.SetTextAlign(22)
    xlab.SetTextSize(0.05)
    xlab.SetTextFont(42)
    xlab.SetTextSize(0.05)
    
    for label in labels:
        xlab.DrawLatex(float(label), 0.895, label) 
            
    legend = rt.TLegend(0.18,0.65,0.53,0.89,"")
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.AddEntry(0, 'AK'+str(args.jet_cone)+' '+args.jet_algo.upper(), '')
    legend.AddEntry(0, '#bf{#phi dependent correction}' if args.jec_vs_phi else '#bf{#phi inclusive correction}', '')
    
    
    if(args.doBPix):
        root_filename_BPix = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/' + args.mc + '/' + args.version + '_' + jec_type + '/Step4_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_ApplyToBPixArea/Merged.root'
    
        root_file_BPix = rt.TFile(root_filename_BPix, 'READ')
        
        print('Processing root file: ' + root_filename_BPix)
    
        etabin_low = 25
        etabin_high = 42
        
        hist_BPix = rt.TH1F('hist_BPix', '', nBins, Boundaries) 
        hist_BPix.SetMarkerColor(rt.kRed)
        hist_BPix.SetLineColor(rt.kRed)
        hist_BPix.SetMarkerStyle(20)
        hist_BPix.SetMarkerSize(1)
        hist_BPix.SetLineWidth(2)
        hist_BPix.SetStats(0)
        
        for i in range(nBins):
            ptmin = Boundaries[i]
            ptmax = Boundaries[i + 1]
            
            hist2D = root_file_BPix.Get('ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '/RelRspVsJetEta_RefPt' + str(int(ptmin)) + 'to' + str(int(ptmax)))                        
            
            hist_proj = hist2D.ProjectionY('_proj_BPix_' + str(int(i)), etabin_low, etabin_high, 'e')
            hist_proj.SetDirectory(0) 
            
            if (hist_proj.GetEntries() > 5 and i>=9):
                median, error = get_histogram_median_1d(hist_proj, debug=False)
                hist_BPix.SetBinContent(i+1, median)
                hist_BPix.SetBinError(i+1, error)
            else:
                hist_BPix.SetBinContent(i+1, 0)
                hist_BPix.SetBinContent(i+1, 0)
                
        hist_BPix.GetXaxis().SetRangeUser(10, 5500)
        hist_BPix.Draw('PE SAME')  
        leg_entry = 'BPix area: #scale[0.7]{-1.479 < #eta < 0.087 #wedge -1.22 < #phi < -0.79}'      
        legend.AddEntry(hist_BPix, leg_entry, 'LPE')
    
    
    if(args.doFPix):
        root_filename_FPix = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/' + args.mc + '/' + args.version + '_' + jec_type + '/Step4_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_ApplyToFPixArea/Merged.root'
        
        root_file_FPix = rt.TFile(root_filename_FPix, 'READ')
        
        print('Processing root file: ' + root_filename_FPix)
    
        etabin_low = 19
        etabin_high = 22
        
        hist_FPix = rt.TH1F('hist_FPix', '', nBins, Boundaries) 
        hist_FPix.SetMarkerColor(rt.kOrange+1)
        hist_FPix.SetLineColor(rt.kOrange+1)
        hist_FPix.SetMarkerStyle(20)
        hist_FPix.SetMarkerSize(1)
        hist_FPix.SetLineWidth(2)
        hist_FPix.SetStats(0)
        
        for i in range(nBins):
            ptmin = Boundaries[i]
            ptmax = Boundaries[i + 1]
            
            hist2D = root_file_FPix.Get('ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '/RelRspVsJetEta_RefPt' + str(int(ptmin)) + 'to' + str(int(ptmax)))                        
            
            hist_proj = hist2D.ProjectionY('_proj_FPix_' + str(int(i)), etabin_low, etabin_high, 'e')
            hist_proj.SetDirectory(0) 
            
            if (hist_proj.GetEntries() > 5 and i>=9):
                median, error = get_histogram_median_1d(hist_proj, debug=False)
                hist_FPix.SetBinContent(i+1, median)
                hist_FPix.SetBinError(i+1, error)
            else:
                hist_FPix.SetBinContent(i+1, 0)
                hist_FPix.SetBinContent(i+1, 0)
    
        hist_FPix.GetXaxis().SetRangeUser(10, 5500)
        hist_FPix.Draw('PE SAME') 
        leg_entry = 'FPix area: #scale[0.7]{#splitline{(-2.043 < #eta < -1.566 #wedge 2.44 < #phi < 2.79) #vee}{(-2.043 < #eta < -1.83 #wedge 2.79 < #phi < 3.05)}}'
        legend.AddEntry(hist_FPix, leg_entry, 'LPE')
    
                   
       
                      
    legend.Draw()
        

    output_png = '../OverviewPlotsBPixFPix/MedianResponseVsPt_' + args.mc + '_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + issue_type + '_' + args.version + '_' + jec_type + '.png'
    output_pdf = output_png.replace(".png", ".pdf")

    c1.SaveAs(output_png)
    c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
