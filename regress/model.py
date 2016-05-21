import numpy as np

from scipy import stats


class Model:
    def __init__(self, name, x_title, y_title, description):
        self.name = name
        self.x_title = x_title
        self.y_title = y_title
        self.description = description
        self.x_val = []
        self.y_val = []
        self.p_val = []

    def add(self, x_val, y_val, p_val=None):
        self.x_val.append(x_val)
        self.y_val.append(y_val)
        if p_val:  # Data already underwent regression
            self.p_val.append(p_val)

    def regress(self):
        x_val = np.array([x for x in self.x_val])
        y_val = np.array([y for y in self.y_val])
        slope, intercept, _, _, _ = stats.linregress(x_val, y_val)
        self.p_val = slope * x_val + intercept

    def data(self):
        return list(zip(
            [int(x) for x in self.x_val],
            [int(y) for y in self.y_val],
            [float(p) for p in self.p_val],
        ))

    def to_dict(self):
        return {
            "name": self.name,
            "x_title": self.x_title,
            "y_title": self.y_title,
            "description": self.description,
            "data": self.data()
        }


