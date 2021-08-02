#!/usr/bin/env python

import os
import argparse
import numpy as np

from utils.data.fileio import _read_root
from utils.data.tools import _get_variable_names
from utils.data.preprocess import _build_new_variables, _apply_selection
from sklearn.metrics import roc_curve, auc

import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)


def plot_loss(outdir, name, indir=None):
    if indir:
        # save the loss in a numpy file
        loss_vals_training = np.load('%s/loss_vals_training.npy' % indir)
        loss_vals_validation = np.load('%s/loss_vals_validation.npy' % indir)
    else:
        # or load the loss array manually
        loss_vals_training = np.array([0.001, 0.0002])
        loss_vals_validation = np.array([0.001, 0.0002])
    epochs = np.array(range(len(loss_vals_training)))

    f, ax = plt.subplots(figsize=(10, 10))
    ax.plot(epochs, loss_vals_training, label='Training')
    ax.plot(epochs, loss_vals_validation, label='Validation', color='green')
    leg = ax.legend(loc='upper right', title=name, borderpad=1, frameon=False, fontsize=16)
    leg._legend_box.align = "right"
    ax.set_ylabel('Loss')
    ax.set_xlabel('Epoch')
    ax.set_xlim(0, np.max(epochs))
    f.savefig('%s/Loss_%s.png' % (outdir, indir.replace('/', '')))
    f.savefig('%s/Loss_%s.pdf' % (outdir, indir.replace('/', '')))
    plt.clf()


def plot_accuracy(outdir, name, indir=None):
    if indir:
        acc_vals_validation = np.load('%s/acc_vals_validation.npy' % indir)
    else:
        acc_vals_validation = np.array([0.001, 0.0002])
    epochs = np.array(range(len(acc_vals_validation)))
    f, ax = plt.subplots(figsize=(10, 10))
    ax.plot(epochs, acc_vals_validation, label='Validation', color='green')
    leg = ax.legend(loc='upper right', title=name, borderpad=1, frameon=False, fontsize=16)
    leg._legend_box.align = "right"
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epoch')
    ax.set_xlim(0, np.max(epochs))
    ax.set_ylim(0.8, 0.95)
    f.savefig('%s/Acc_%s.png' % (outdir, indir.replace('/', '')))
    plt.clf()

# return input by classes (signal and background)
def roc_input(table, var, label_sig, label_bkg):
    scores_sig = np.zeros(table[var].shape[0])
    scores_bkg = np.zeros(table[var].shape[0])
    scores_sig = table[var][(table[label_sig] == 1)]
    scores_bkg = table[var][(table[label_bkg] == 1)]
    predict = np.concatenate((scores_sig, scores_bkg), axis=None)
    siglabels = np.ones(scores_sig.shape)
    bkglabels = np.zeros(scores_bkg.shape)
    truth = np.concatenate((siglabels, bkglabels), axis=None)
    return truth, predict

# get roc for a table with given scores, a label for signal, and one for background
def get_roc(table, scores, label_sig, label_bkg):
    fprs = {}
    tprs = {}
    for score_name, score_label in scores.items():
        truth, predict = roc_input(table, score_name, label_sig['label'], label_bkg['label'])
        fprs[score_label], tprs[score_label], threshold = roc_curve(truth, predict)
    return fprs, tprs

# plot roc
def plot_roc(label_sig, label_bkg, fprs, tprs):
    plt.clf()

    def get_round(x_effs, y_effs, to_get=[0.01, 0.02, 0.03]):
        effs = []
        for eff in to_get:
            for i, f in enumerate(x_effs):
                if round(f, 2) == eff:
                    effs.append(y_effs[i])
                    print(round(f, 2), y_effs[i])
                    break
        return effs

    markers = ['v', '^', 'o', 's']
    ik = 0
    for k, it in fprs.items():
        plt.plot(fprs[k], tprs[k], lw=2.5, label=r"{}, AUC = {:.1f}%".format(k, auc(fprs[k], tprs[k])*100))
        x_effs = [0.01, 0.02, 0.03]
        y_effs = get_round(fprs[k], tprs[k])
        print(x_effs, y_effs)
        plt.scatter(x_effs, y_effs, marker=markers[ik], label=k)
        ik += 1

    # if we want to compare to given efficiencies add those here
    x_eff_tag = None
    y_eff_tag = None
    # x_eff_tag = [0.01,0.02,0.03] # background efficiency
    # y_eff_tag = [0.7,0.75,0.8] # signal efficiency
    if x_eff_tag is not None and y_eff_tag is not None:
        plt.scatter(x_eff_tag, y_eff_tag, marker='d', label=r'h$\rightarrow e\tau$')

    plt.legend(loc='upper left')
    plt.grid(which='minor', alpha=0.2)
    plt.grid(which='major', alpha=0.5)
    plt.ylabel(r'Tagging efficiency %s' % label_sig['legend'])
    plt.xlabel(r'Mistagging rate %s' % label_bkg['legend'])
    plt.savefig("roc_%s.pdf" % label_sig['label'])
    plt.xscale('log')
    plt.savefig("roc_%s_xlog.pdf" % label_sig['label'])
    plt.xscale('linear')

# plot jet variables after a selection on the tagger
def plot_features_qcd(table, scores, label_sig, label_bkg, name, features=['fj_sdmass', 'fj_pt']):
    labels = {'fj_msoftdrop': r'$m_{SD}$',
              'fj_pt': r'$p_{T}$',
              }
    feature_range = {'fj_msoftdrop': [[30, 260], [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260]],
                     'fj_pt': [[200, 2500], [200, 251, 316, 398, 501, 630, 793, 997, 1255, 1579, 1987, 2500]],
                     }

    def computePercentiles(data, percentiles):
        mincut = 0.
        tmp = np.quantile(data, np.array(percentiles))
        tmpl = [mincut]
        for x in tmp:
            tmpl.append(x)
        perc = [0.]
        for x in percentiles:
            perc.append(x)
        return perc, tmpl

    for score_name, score_label in scores.items():
        bkg = (table[label_bkg['label']] == 1)
        var = table[score_name][bkg]
        percentiles = [0.97, 0.98, 0.99, 0.995, 0.9995]
        per, cuts = computePercentiles(table[score_name][bkg], percentiles)
        for k in features:
            fig, ax = plt.subplots(figsize=(10, 10))
            bins = feature_range[k][1]
            for i, cut in enumerate(cuts):
                c = (1-per[i])*100
                lab = '%.3f%% mistag-rate' % c
                ax.hist(table[k][bkg][var > cut], bins=bins, lw=2, density=True, range=feature_range[k][0],
                        histtype='step', label=lab)
            ax.legend(loc='best')
            ax.set_xlabel(labels[k]+' (GeV)')
            ax.set_ylabel('Number of events (normalized)')
            ax.set_title('%s dependence' % labels[k])
            plt.savefig("%s_%s.pdf" % (k, score_label))

# plot tagger response
def plot_response(table, scores, label_sig, label_bkg, name):
    for score_name, score_label in scores.items():
        plt.clf()
        bins = 100
        var = table[score_name]
        data = [var[(table[label_sig['label']] == 1)],
                var[(table[label_bkg['label']] == 1)]]
        labels = [label_sig['legend'],
                  label_bkg['legend']]
        for j in range(0, len(data)):
            plt.hist(data[j], bins, log=False, histtype='step', density=True, label=labels[j], fill=False, range=(-1., 1.))
        plt.legend(loc='best')
        plt.xlim(0, 1)
        plt.xlabel('%s Response' % score_label)
        plt.ylabel('Number of events (normalized)')
        plt.title('NeuralNet applied to test samples')
        plt.savefig("%s_%s_disc.pdf" % (score_label, label_sig['label']))


def main(args):
    # include background labels here
    label_bkg = {
        'qcd': {'legend': 'QCD',
                'label':  'QCD_label'},
        'top': {'legend': 'Top',
                'label':  'fj_isTop'},
    }
    # include signal labels here
    label_sig = {
        '4q': {'legend': 'H(WW) 4q',
               'label': 'fj_H_WW_4q_4q',
               'scores': 'H4q'},
        '3q': {'legend': 'H(WW) 3q',
               'label': 'fj_H_WW_4q_3q',
               'scores': 'H3q'},
        'bb': {'legend': 'H(bb)',
               'label': 'fj_H_bb',
               'scores': 'Hbb'},
        'elenuqq': {'legend': 'H(WW) ele',
                    'label':  'fj_H_WW_elenuqq',
                    'scores': 'Helenuqq'},
        'munuqq': {'legend': 'H(WW) mu',
                   'label':  'fj_H_WW_munuqq',
                   'scores': 'Hmunuqq'},
    }

    # choose one channel for which to make the roc curve
    # channel = key of label_sig or label_bkg dict
    label_sig = label_sig[args.channel]
    label_bkg = label_bkg[args.bkg]

    # compute all new variables that are not included in the inference file
    #
    # for scores:
    #  we expect all scores to sum up to 1, e.g. given two signals in the event (signal 1 and 2) and one background process (background 1):
    #  score_signal_1 + score_signal_2 + score_background_1 = 1
    #  then nn_signal_1 = score_signal_1 / (score_signal_1 + score_background_1) = score_signal_1 / (1 - score_signal_2)

    funcs = {
        'score_Hbb': 'score_fj_H_bb/(1-score_fj_H_cc-score_fj_H_qq)',
        'PN_H4qvsQCD': 'fj_PN_H4qvsQCD',
        # 'score_H4q': 'score_fj_H_WW_4q/(1-score_fj_H_WW_elenuqq-score_fj_H_WW_munuqq)',
        'score_H4q': 'score_label_4q/(score_label_4q+score_fj_isQCD)',
        # 'score_Helenuqq': 'score_fj_H_WW_elenuqq/(1-score_fj_H_WW_4q-score_fj_H_WW_munuqq)',
        # 'score_Hmunuqq': 'score_fj_H_WW_munuqq/(1-score_fj_H_WW_4q-score_fj_H_WW_elenuqq)',
        'PN_HbbvsQCD': 'fj_PN_XbbvsQCD',
    }

    # include old PN version for comparison (only available for AK8)
    if args.jet == "AK8":
        funcs['deepAK8MD_H4q'] = 'fj_deepTagMD_H4qvsQCD'
        funcs['deepAK8_H'] = 'fj_deepTag_HvsQCD'
        funcs['PN_Xbb'] = 'fj_PN_XbbvsQCD'

    # inputfiles and names should have same shape
    inputfiles = args.input.split(',')
    names = args.name.split(',')

    # make dict of branches to load
    lfeatures = ['fj_msoftdrop', 'fj_pt']
    sameshape = True
    sh = []
    # check if the input files have the same shape
    for n, name in enumerate(names):
        table = _read_root(inputfiles[n], lfeatures)
        for k in table.keys():
            sh.append(table[k].shape)
            if n > 0 and table[k].shape != sh[0]:
                sameshape = False

    # go to plot directory
    cwd = os.getcwd()
    odir = os.path.join(args.odir, args.tag)
    os.system('mkdir -p %s' % odir)
    os.chdir(odir)

    # now build tables
    for n, name in enumerate(names):
        scores = {'score_%s' % label_sig['scores']: '%s %s' % (name, label_sig['scores'])}
        if args.channel == '4q':
            scores['PN_H4qvsQCD'] = 'PN H4qvsQCD'
            if args.jet == "AK8":
                scores['deepAK8MD_H4q'] = 'DeepAK8 MD H4q'
                scores['deepAK8_H'] = 'DeepAK8 H'
        elif args.channel == 'bb':
            scores['PN_HbbvsQCD'] = 'PN HbbvsQCD'
        else:
            if args.jet == "AK8":
                scores['fj_lsf3'] = 'LSF'

        loadbranches = set()
        for k, kk in scores.items():
            # load scores
            if k in funcs.keys():
                loadbranches.update(_get_variable_names(funcs[k]))
            else:
                loadbranches.add(k)

            # load features
            loadbranches.add(label_bkg['label'])
            loadbranches.add(label_sig['label'])
            for k in lfeatures:
                loadbranches.add(k)
            loadbranches.add('fj_genH_mass')
        print(loadbranches)

        table = _read_root(inputfiles[n], loadbranches)
        config_selection = None
        config_selection = '((fj_isQCD==1) | ((label_4q==1) & (fj_genH_mass!=125)))'
        if config_selection:
            _apply_selection(table, config_selection)
        print(table)
        if(n == 0 or (not sameshape)):
            _build_new_variables(table, {k: v for k, v in funcs.items() if k in scores.keys()})
            newtable = table
            newscores = scores
        else:
            for k in table:
                newtable[k] = table[k]
            for k in scores:
                newscores[k] = scores[k]

        if not sameshape:
            fprs, tprs = get_roc(table, scores, label_sig, label_bkg)
            if n == 0:
                newfprs = fprs
                newtprs = tprs
            else:
                for k in fprs:
                    newfprs[k] = fprs[k]
                    newtprs[k] = tprs[k]
            plot_response(table, scores, label_sig, label_bkg, name+args.channel)
            plot_features_qcd(table, scores, label_sig, label_bkg, name+args.channel, lfeatures)
            # plot_features_signal(table, scores, label_sig, label_bkg, name+args.channel, lfeatures_signal)

    if sameshape:
        newfprs, newtprs = get_roc(newtable, newscores, label_sig, label_bkg)
        plot_response(newtable, newscores, label_sig, label_bkg, args.channel)
        plot_features_qcd(newtable, newscores, label_sig, label_bkg, args.channel, lfeatures)

    plot_roc(label_sig, label_bkg, newfprs, newtprs)
    os.chdir(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file(s)')
    parser.add_argument('--name', help='name ROC(s)')
    parser.add_argument('--tag', help='folder tag')
    parser.add_argument('--odir', help='odir')
    parser.add_argument('--channel', help='channel')
    parser.add_argument('--jet', default="AK8", help='jet type')
    args = parser.parse_args()

    main(args)
