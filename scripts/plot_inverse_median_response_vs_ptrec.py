import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_inverse_median_response_vs_ptrec.py --jetCone 4 --jetAlgo puppi --era Summer23 --version V1'

    parser = ArgumentParser(description='Script that plots the inverse of median response vs rec pt for all eta bins, and checks for asymptotic discontinuities in the fits',epilog=usage)

    parser.add_argument("-c", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-a", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")
                    
    parser.add_argument("-v", "--version", dest="version", type=str, required=True,
                    help="Specify version", metavar="VERSION")                

    args = parser.parse_args()

    root_filename = '../condor_AK'+str(args.jet_cone)+args.jet_algo.upper()+'/Files/'+args.era+'_'+args.version+'/'+('L1' if args.jet_algo.lower() == 'chs' else '')+'L2L3_output/l2.root'

    output_dir = '../condor_AK'+str(args.jet_cone)+args.jet_algo.upper()+'/Files/'+args.era+'_'+args.version+'/'+('L1' if args.jet_algo.lower() == 'chs' else '')+'L2L3_output/'
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"The directory {output_dir} does not exist.")
    else:    
        plots_dir = os.path.join(output_dir, 'plots')
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir, exist_ok=True)

    root_file = rt.TFile.Open(root_filename, "READ")
    
    jet_dir = root_file.Get('ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + ('l1' if args.jet_algo.lower() == 'chs' else ''))
    if not jet_dir or not isinstance(jet_dir, rt.TDirectoryFile):
        print('Error: ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + ('l1' if args.jet_algo.lower() == 'chs' else '') + ' directory not found in the ROOT file.')
        root_file.Close()
        exit(1)


    for key in jet_dir.GetListOfKeys():
        obj_name = key.GetName()

        if 'AbsCorVsJetPt_JetEta' in obj_name:
            #if not ('4.191to4.363' in obj_name or '4.889to5.191' in obj_name): continue 
            #if not '-3.314to-3.139' in obj_name: continue         
            print('Processing: '+ obj_name)

            graph = jet_dir.Get(obj_name)
        
            if isinstance(graph, rt.TGraphErrors):
                eta_range = obj_name.replace('AbsCorVsJetPt_JetEta', '').split('to')
                eta_min, eta_max = float(eta_range[0]), float(eta_range[1])
            

                fit = graph.GetFunction('fit')
                if fit:
                    fit.SetLineColor(rt.kRed)
                    fit.SetLineWidth(2)
                                       
                    #Scan each fit in order to detect possible asymptotic discontinuities
                    scan_step = 0.001 if abs(eta_min)<1.305 else 0.0001
                    x = 8.0
                    while x < graph.GetXaxis().GetXmax():
                        y1 = fit.Eval(x)
                        y2 = fit.Eval(x+scan_step)
                        if(abs(y2-y1) > 0.2):
                            print('!!!!!! WARNING: ASYMPTOTIC BEHAVIOR IN ETA BIN ['+str(eta_min)+', '+str(eta_max)+']')
                        x+=scan_step
                        

                c1 = rt.TCanvas("c1", "c1", 800, 700)
                c1.SetLogx(1)
                c1.SetTickx(1)
                c1.SetTicky(1)
                c1.SetRightMargin(0.04)
                c1.SetLeftMargin(0.12)
                c1.SetTopMargin(0.10)
                c1.SetBottomMargin(0.13)

                if(abs(eta_min) <= 1.044):
                    ymin = 0.8
                    ymax = 1.5 if (args.jet_cone == 8 or args.jet_algo.lower()=='chs') else 1.2
                elif(abs(eta_min) <= 1.93):
                    ymin = 0.8
                    ymax = 1.5
                elif(abs(eta_min) >= 2.65 and abs(eta_min) <= 2.964):
                    ymin = 0.8
                    ymax = 2.5    
                else:
                    ymin = 0.8
                    ymax = 2.5 if args.jet_cone == 8 else 1.8       

                lastx, lasty = ctypes.c_double(0), ctypes.c_double(0)
                graph.GetPoint(graph.GetN() - 1, lastx, lasty)
                frame = c1.DrawFrame(6., ymin, lastx.value*1.1, ymax)
                frame.GetXaxis().SetTitle("p_{T}^{rec} [GeV]")
                frame.GetXaxis().SetTitleSize(0.05)
                frame.GetXaxis().SetTitleOffset(1.05)
                frame.GetYaxis().SetTitle("Correction = [median(Response)]^{-1}")
                frame.GetYaxis().SetTitleSize(0.05)
                frame.GetYaxis().SetTitleOffset(1.15)
                frame.GetXaxis().SetLabelSize(0.04)
                frame.GetYaxis().SetLabelSize(0.035)

                if fit:
                    chi2_legend = rt.TLegend(0.4, 0.18, 0.7, 0.33, "")
                    chi2_legend.SetTextSize(0.04)
                    chi2_legend.SetFillColor(0)
                    chi2_legend.SetBorderSize(0)
                    chi_text = f"#chi^{{2}} / ndf = {fit.GetChisquare():.1f} / {fit.GetNDF()}, Prob. = {fit.GetProb():.2f}"
                    chi2_legend.SetHeader("Fit with standard+Gaussian function")
                    chi2_legend.AddEntry(fit, chi_text, "L")
                    chi2_legend.Draw()

                graph.SetMarkerColor(rt.kBlack)
                graph.Draw("P SAME")

                if fit:
                    fit.SetRange(6., lastx)

                cms = rt.TPaveText(0.206, 0.91, 0.406, 0.95, "NDC")
                cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
                cms.SetTextFont(42)
                cms.SetTextSize(0.05)
                cms.SetBorderSize(0)
                cms.SetFillColor(0)
                cms.Draw()

                sample = rt.TPaveText(0.668, 0.91, 0.868, 0.95, "NDC")
                sample.AddText(args.era + ' (13.6 TeV)')
                sample.SetTextFont(42)
                sample.SetTextSize(0.05)
                sample.SetBorderSize(0)
                sample.SetFillColor(0)
                sample.Draw()


                eta_leg = rt.TPaveText(0.65, 0.70, 0.85, 0.85, "NDC")
                eta_leg.SetFillColor(0)
                eta_leg.SetBorderSize(0)
                eta_leg.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
                eta_leg.AddText(f"{eta_min:.3f} < #eta < {eta_max:.3f}")
                eta_leg.SetTextFont(42)
                eta_leg.SetTextSize(0.05)
                eta_leg.Draw()

                output_png = os.path.join(plots_dir, f'InverseOfResponseVsRecPt_AK{args.jet_cone}{args.jet_algo.upper()}_{args.era}_{args.version}_RecEta{eta_min:.3f}to{eta_max:.3f}.png')
                output_pdf = output_png.replace(".png", ".pdf")

                c1.SaveAs(output_png)
                c1.SaveAs(output_pdf)


                del c1

    root_file.Close()

    print("Processing complete. All plots saved.")

if __name__ == '__main__':
    main()
