from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from mpl_arrow import arrow,arrow_absolute,vector

class UnitCell:
    def __init__(self, a, b, gamma):
        self.a = a
        self.b = b
        self.gamma = gamma

    @classmethod
    def from_molecule(cls, molecule, gamma=90., padding=0.15):
        x,y = molecule.x,molecule.y
        y = y - y.min() 

        ypad = padding * (y.max() - y.min())
        y = y + ypad
        b = (y.max() + ypad) / np.sin(np.deg2rad(gamma))

        xpad = padding * (x.max() - x.min())

        tg = np.tan(np.deg2rad(gamma))
        rel_x = x - y / tg
        x = x - rel_x.min() + xpad
        rel_x = x - y / tg
        a = rel_x.max() + xpad

        molecule.x = x
        molecule.y = y

        return cls(a, b, gamma)

    @property
    def O(self):
        return self.orthogonaliztion_matrix

    @property
    def orthogonaliztion_matrix(self):
        a,b = self.a,self.b
        cg = np.cos(np.deg2rad(self.gamma))
        sg = np.sin(np.deg2rad(self.gamma))
        O = np.array([
            [a, b * cg],
            [0., b * sg],
        ])
        return O

    @property
    def F(self):
        return self.fractionalization_matrix

    @property
    def fractionalization_matrix(self):
        return np.linalg.inv(self.O)

    @property
    def B(self):
        return self.indexing_matrix

    @property
    def indexing_matrix(self):
        return self.fractionalization_matrix.T

    def get_hk_limits(self, dmin):
        hmax = np.floor(self.a / dmin)
        kmax = np.floor(self.b / dmin)
        return hmax, kmax

    def get_resolution(self, H):
        Q = self.B @ H.T
        dinv = np.sqrt(
            np.square(Q[...,0,:]) + np.square(Q[...,1,:])
        )
        d = np.reciprocal(dinv)
        return d

    def get_reciprocal_cell(self, dmin):
        hmax,kmax = self.get_hk_limits(dmin)
        h, k = map(np.ndarray.flatten, np.mgrid[-hmax:hmax+1,-kmax:kmax+1])
        H = np.column_stack((h, k))
        Q = self.B@H.T
        d = self.get_resolution(H)
        d[~np.isfinite(d)] = 0.
        idx = d >= dmin
        H = H[idx]
        d = d[idx]
        return H

    def plot_a(self, ax=None, **kwargs):
        O = self.O
        out = arrow(0., 0., O[0,0], O[1, 0], ax=ax, **kwargs)
        return out

    def plot_b(self, ax=None, **kwargs):
        O = self.O
        out = arrow(0., 0., O[0,1], O[1, 1], ax=ax, **kwargs)
        return out

    def crop_cell(self, ax=None, padding=0.15):
        if ax is None:
            ax = plt.gca()
        O = self.O
        cell_edges = np.array([
            [0., 0.],
            O[:,0],
            O[:,0] + O[:,1],
            O[:,1],
            [0., 0.],
        ])
        xmin,ymin = cell_edges.min(0)
        xmax,ymax= cell_edges.max(0)
        xpad = padding * (xmax - xmin)
        ypad = padding * (ymax - ymin)
        xlim = [xmin - xpad, xmax + xpad]
        ylim = [ymin - ypad, ymax + ypad]

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)


    def plot_cell(self, fmt='k--', ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        O = self.O
        cell_edges = np.array([
            [0., 0.],
            O[:,0],
            O[:,0] + O[:,1],
            O[:,1],
            [0., 0.],
        ])
        out = ax.plot(*cell_edges.T, fmt)
        ax.set_aspect('equal')
        center_x,center_y = self.O@[0.5, 0.5]

        xlim = ax.get_xlim()
        offset =  center_x - np.mean(xlim)
        xlim = np.array(xlim) + offset

        ylim = ax.get_ylim()
        offset = center_y - np.mean(ylim) 
        ylim = np.array(ylim) + offset

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        return out

