import numpy as np

class UnitCell:
    def __init__(self, a, b, gamma, deg=True):
        self.a = a
        self.b = b
        self.gamma = gamma
        self.deg = deg

    @property
    def _gamma_radians(self):
        if self.deg:
            return np.deg2rad(self.gamma)
        return self.gamma

    @property
    def orthogonalization(self):
        g = self._gamma_radians
        c = np.cos(g)
        s = np.sin(g)
        O = np.array([
            [self.a, c * b],
            [0., s * b],
        ])
        return O

    @property
    def fractionalization(self):
        return np.linalg.inv(self.O)

    @property
    def reciprocal_orthogonalization(self):
        return self.fractionalization.T

    @property
    def B(self):
        return self.reciprocal_orthogonalization

    @property
    def O(self):
        return self.orthogonalization

    @property
    def F(self):
        return self.fractionalization

