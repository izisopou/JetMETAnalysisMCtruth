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
    usage = 'Example: python3 plot_response_distributions.py --jetCone 4 --jetAlgo puppi --JEC 0 --JetPtMin 30 --JetPtMax 35' 

    parser = ArgumentParser(description='Script that plots the response distributions before or after JEC applied',epilog=usage)

    parser.add_argument("-cone", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-algo", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
                    
    parser.add_argument("-jec", "--JEC", dest="jec", type=int, choices=[0, 1], required=True,
                    help="Specify if JECs are applied (0: No, 1: Yes)", metavar="JEC")  
                    
    parser.add_argument("-PtMin", "--JetPtMin", dest="jet_pt_min", type=float, required=True,
                    help="Specify jet pt min", metavar="JETPTMIN")
                      
    parser.add_argument("-PtMax", "--JetPtMax", dest="jet_pt_max", type=float, required=True,
                    help="Specify jet pt max", metavar="JETPTMAX")   
                                                                                 
    
    args = parser.parse_args()

    eta_pairs = ['0, 1.3', '1.3, 2.4', '2.4, 2.7', '2.7, 3', '3, 5']
    
    for eta_pair in eta_pairs:
        eta_min, eta_max = eta_pair.split(', ')
        
        if(args.jet_pt_min > 300 and abs(float(eta_min))>=2.4): continue
    
        eras = ['Summer22', 'Summer22EE', 'Summer23', 'Summer23BPix', 'RunIII2024Summer24']
        colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2, rt.kViolet, rt.kOrange+1]    
    
        c1 = rt.TCanvas("c1", "c1", 800, 700)
        c1.SetLogy(0)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetRightMargin(0.04)
        c1.SetLeftMargin(0.12)
        c1.SetTopMargin(0.10)
        c1.SetBottomMargin(0.13)

        frame = c1.DrawFrame(0, 0, 3.5, 1)
        frame.GetXaxis().SetTitle('Response = p_{T}^{rec} / p_{T}^{ptcl}')
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.05)
        frame.GetYaxis().SetTitle('Normalized to unity')
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetLabelSize(0.035)
    
        legend = rt.TLegend(0.67,0.17,0.92,0.72,"")
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.SetBorderSize(0)
    
        ymax = 0
    
        for era, color in zip(eras, colors):
         
            if(era=='RunIII2024Summer24' and (args.jet_cone==8 or args.jet_algo.lower()=='chs')): continue

            root_filename = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/ResponseDistributions/' + ('' if args.jec else 'Un') + 'CorrectedResponses_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_' + era + '.root' 
        
            print('Processing file: ' + root_filename)
        
            root_file = rt.TFile(root_filename, 'READ')
                
            hist_filename = ('ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + '/RelRspVsRefPt_JetEta' + eta_min + 'to' + eta_max)
        
            print('Processing histogram: ' + hist_filename)
        
            hist2D = root_file.Get(hist_filename)
        
            ptbin = -999
        
            for i in range(1, hist2D.GetNbinsX() + 1):
                bin_low = hist2D.GetXaxis().GetBinLowEdge(i)
                bin_high = hist2D.GetXaxis().GetBinLowEdge(i+1)

                if (abs(bin_low-args.jet_pt_min)<1e-6 and abs(bin_high-args.jet_pt_max)<1e-6):
                    ptbin = i

        
            hist = hist2D.ProjectionY('h_' + era, ptbin, ptbin, 'e')
        
            hist.SetDirectory(0)
        
            hist.Scale(1./hist.Integral())               
            hist.SetLineWidth(2)
            hist.SetLineColor(color) 
            hist.Draw('HIST SAME')
        
            if(hist.GetMaximum() > ymax): ymax = hist.GetMaximum()
        
            median, error = get_histogram_median_1d(hist, debug=False)
        
            leg_entry = '#splitline{%s}{#splitline{#scale[0.7]{Median = %.3f}}{#scale[0.7]{Mean = %.3f}}}' % (era, median, hist.GetMean())
        
            legend.AddEntry(hist, leg_entry, 'L')     
                
                      
        legend.Draw()
    
        frame.GetYaxis().SetRangeUser(0, ymax*1.1)
    
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
    
        info_leg = rt.TPaveText(0.73, 0.71, 0.93, 0.86, "NDC")
        info_leg.SetFillColor(0)
        info_leg.SetBorderSize(0)
        info_leg.SetTextFont(42)
        info_leg.SetTextAlign(31)
        info_leg.SetTextSize(0.04)
        info_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        info_leg.AddText(eta_min + ' < |#eta| < ' + eta_max)
        info_leg.AddText(str(int(args.jet_pt_min)) + ' < p_{T}^{ptcl} < ' + str(int(args.jet_pt_max)) + ' GeV')
        info_leg.Draw()
    
        lvert = rt.TLine(1, 0, 1, ymax*1.1)
        lvert.SetLineWidth(2)
        lvert.SetLineStyle(rt.kDashed)
        lvert.Draw()


        output_png = '../ForAN/' + ('' if args.jec else 'Un') + 'CorrectedResponses_AK' + str(args.jet_cone) + args.jet_algo.upper() + '_JetAbsEta' + eta_min + 'to' + eta_max + '_JetPt' + str(int(args.jet_pt_min)) + 'to' + str(int(args.jet_pt_max)) + '.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)



if __name__ == '__main__':
    main()
