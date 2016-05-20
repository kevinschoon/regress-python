import pygal
import numpy as np

from scipy import stats
from pygal.style import CleanStyle


class Model:
    def __init__(self, name, x_title, y_title):
        self.name = name
        self.x_title = x_title
        self.y_title = y_title
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

    def to_dict(self):
        return {
            "name": self.name,
            "x_title": self.x_title,
            "y_title": self.y_title,
            "data": list(zip(
                [int(x) for x in self.x_val],
                [int(y) for y in self.y_val],
                [int(p) for p in self.p_val]
            ))
        }

    @classmethod
    def from_dict(cls, data):
        m = cls(data["name"], data["x_title"], data["y_title"])
        for entry in data["data"]:
            m.add(*entry)
        return m


def model_to_svg(model):
    chart = pygal.XY(stroke=False, style=CleanStyle, x_title=model.x_title, y_title=model.y_title)
    chart.add("", list(zip(model.x_val, model.y_val)))
    chart.add("predictions", list(zip(model.x_val, model.p_val)), stroke=True)
    return chart.render()
