#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import locale
import logging
import sys
import os
from scipy.stats import norm

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

FV = 1200000.  # future value
N = 1  # number of periods
RF = 0.05  # risk-free rate
SIGMA = .2  # volatility
PV_DEBT = 800000.  # current debt
BANKRUPTCY_COST = 50000.  # cost of bankruptcy

if __name__ == '__main__':

    # TODO: Add command-line arguments to override default parameters

    parser = \
        argparse.ArgumentParser(description='Calculate Bankruptcy Risk.'
                                )

    # parser.add_argument('--start', metavar='N', type=int,
    #                     default=SAMPLE_START,
    #                     help='start sample N days ago')
    # parser.add_argument('--length', metavar='N', type=int,
    #                     default=SAMPLE_LENGTH, help='length of sample')
    #
    # args = parser.parse_args()

    PV = FV / (1 + RF)
    normal_deviate = (PV - PV_DEBT) / PV
    vol_multiple = normal_deviate / SIGMA
    p_bankruptcy = 1 - norm.cdf(vol_multiple)
    bankruptcy_cost = p_bankruptcy * BANKRUPTCY_COST
    pv_w_bankruptcy = PV - bankruptcy_cost
    logging.info(
        'Parameters: FV = %s. N = %d. RF = %0.2f%%. SIGMA = %0.2f. PV_DEBT = %s. BANKRUPTCY_COST = %s.'
            ,
        locale.currency(FV, grouping=True),
        N,
        RF,
        SIGMA,
        locale.currency(PV_DEBT, grouping=True),
        locale.currency(BANKRUPTCY_COST, grouping=True),
        )
    logging.info('Results: PV = %s. normal_deviate = %0.2f. p(bankruptcy) = %0.2f%%. Bankruptcy Cost = %s. PV (with bankruptcy) = %s'
                 , locale.currency(PV, grouping=True), normal_deviate,
                 p_bankruptcy, locale.currency(bankruptcy_cost,
                 grouping=True), locale.currency(pv_w_bankruptcy, grouping=True))
