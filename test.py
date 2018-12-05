#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np

drdz = np.array([1, 2, 3, 4, 4, 5, 4, 3, 4, np.nan, np.nan])
drdz = map(lambda x: x * 1e-4, drdz)
depth = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

#inds = np.nonzero(~np.isnan(drdz))
#inds = inds.astype(int)
#
#depth= depth[inds[0]]
#drdz= drdz[inds]

inds = np.where(~np.isnan(drdz))
depth= depth[inds]

