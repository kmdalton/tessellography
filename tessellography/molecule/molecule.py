from sklearn.manifold import MDS
from matplotlib import pyplot as plt
import numpy as np

class Molecule:
    def __init__(self, x, y, elements=None):
        self.elements = elements
        self.x,self.y = x,y

    @classmethod
    def from_3d(cls, x, y, z, elements=None, random_state=1234):
        #TODO: add argument for plane group symmetry and populate cell accordingly
        xyz = np.column_stack((x, y, z))
        x,y = MDS(2, metric=True, random_state=random_state).fit_transform(xyz).T
        return cls(x, y, elements)

    @classmethod
    def from_pdb(cls, pdb_file, heavy=True, random_state=1234):
        x,y,z,elements = [],[],[],[]
        lines = open(pdb_file).readlines()
        for line in lines:
            if line[:4] not in ('ATOM', 'HETA'):
                continue
            element = line[77]
            if heavy and element=='H':
                continue
            x.append(float(line[30:38]))
            y.append(float(line[38:46]))
            z.append(float(line[46:54]))
            elements.append(element)

        x,y,z = np.array(x),np.array(y),np.array(z)
        return cls.from_3d(x, y, z, elements, random_state=random_state)

    def plot(self, ax=None, color_scheme=None):
        if ax is None:
            ax = plt.gca()
        if color_scheme is None:
            color_scheme = {
                'C' : "0.5",
                'N' : 'b',
                'O' : 'r',
            }

        if self.elements is None:
            colors = color_scheme['C']
        else:
            colors = list(map(lambda x: color_scheme.get(x, color_scheme['C']), self.elements))

        ax.scatter(self.x, self.y, c=colors, s=30)
        ax.set_aspect('equal')

