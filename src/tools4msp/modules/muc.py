# coding: utf-8

import logging
import itertools
import numpy as np
import xarray as xr
import pandas as pd
from os import path
from os import path, listdir
from .casestudy import CaseStudyBase

logger = logging.getLogger(__name__)

# def coexist_rules(use1conf,
#                   use2conf):
#     vscale1, spatial1, time1, mobility1 = use1conf
#     vscale2, spatial2, time2, mobility2 = use2conf
#
#     # Rule 1
#     if vscale1 != 3 and vscale2 != 3 and vscale1 != vscale2:
#         return 0
#     # Rule 2
#     if mobility1 and mobility2:
#         return min(spatial1, spatial2) + min(time1, time2)
#     # Rule 3
#     return max(spatial1, spatial2) + max(time1, time2)


class MUCCaseStudy(CaseStudyBase):
    def __init__(self,
                 csdir=None,
                 rundir=None,
                 name='unnamed'):

        self.potential_conflict_scores = pd.DataFrame()
        super().__init__(csdir=csdir,
                         rundir=rundir,
                         name='unnamed')

    def get_potential_conflict_score(self, use1id, use2id):
        return self.potential_conflict_scores.loc[use1id, use2id]

    def run(self, uses=None, intensity=False, outputmask=None, pivot_layer=None):
        logger.debug("uses = {}".format(uses))
        logger.debug("pivot_layer = {}".format(pivot_layer))
        # TODO using outputmask
        couses_data = []
        muc = xr.DataArray(np.zeros_like(self.grid))
        alluses_iter = self.get_uses().iterrows()
        for _use1, _use2 in itertools.combinations(alluses_iter, 2):
            use1id, use1 = _use1
            use2id, use2 = _use2
            if uses is not None and (use1id not in uses or use2id not in uses):
                continue
            logger.debug("use1id = {}, use2id = {}".format(use1id, use2id))
            if pivot_layer is not None and (use1id != pivot_layer and use2id != pivot_layer):
                continue

            score = self.get_potential_conflict_score(use1id, use2id)
            # convert layers to xarray DataArray
            l1 = xr.DataArray(use1.layer.copy()) if not intensity else xr.DataArray(use1.layer)
            l2 = xr.DataArray(use2.layer.copy()) if not intensity else xr.DataArray(use2.layer)
            if not intensity:
                # set values > 0 (and not null) to 1
                l1 = xr.where((~l1.isnull()) & (l1 > 0), 1, l1)
                l2 = xr.where((~l2.isnull()) & (l2 > 0), 1, l2)

            _score = l1 * l2 * score

            # Apply mask where grid==0 deterministically with xarray
            grid_da = xr.DataArray(self.grid)
            _score = _score.where(grid_da != 0)
            if outputmask is not None:
                _score = _score.where(~xr.DataArray(outputmask))

            muc = muc + _score

            couses_data.append({'u1': use1.code,
                                'u2': use2.code,
                                'score': float(np.nansum(_score)),
                                # convert to int for allowing json serialization
                                'ncells': int(_score[_score > 0].count())
            })
        # Ensure muc has NaNs where grid==0
        muc = muc.where(xr.DataArray(self.grid) != 0)
        self.outputs['muc'] = muc
        self.outputs['muc_couses'] = couses_data
        self.outputs['muc_totalscore'] = muc.sum()
        return True
    #
    # def dump_inputs(self):
    #     self.coexist_scores.to_csv(self.get_outpath('coexist_scores.csv'))

    def load_inputs(self):
        for f in listdir(self.inputsdir):
            filepath = path.join(self.inputsdir, f)
            fname, ext = path.splitext(f)
            if ext == '.json':
                # remove random file suffix
                fname = fname.split('_')[0]
                if fname == 'muc-PCONFLICT':
                    df = pd.read_json(filepath)
                    _df = df.copy()
                    _df.columns = ['score', 'u2', 'u1']
                    df = pd.concat([df, _df], ignore_index=True, sort=False)
                    df = df.pivot('u1', 'u2', values='score')
                    ordered = sorted(df.columns)
                    df = df.reindex(ordered, axis=1)
                    self.potential_conflict_scores = df

    def dump_outputs(self):
        if 'muc' in self.outputs:
            self.outputs['muc'].write_raster(self.get_outpath('muc.tiff'), dtype='float32')
        if 'muc_couses_df' in self.outputs:
            self.outputs['muc_couses_df'].to_csv(self.get_outpath('muc_couses_df.csv'))
