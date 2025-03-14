import scipy
import numpy as np
from dataclasses import dataclass

@dataclass
class StatsTester(object):
    def __init__(self, array):
        self.array = array
    
    def __post_init__(self):
        self.skew = scipy.stats.skew(self.array)
        self.severe_skew = abs(self.skew) > 0.5
        self.mean = np.mean(self.array)
        self.std_dev = np.std(self.array)
        self.p10 = np.percentile(self.array, 10)
        self.p25 = np.percentile(self.array, 25)
        self.p50 = np.percentile(self.array, 50)
        self.p75 = np.percentile(self.array, 75)
        self.p90 = np.percentile(self.array, 90)
    
    def normal_dist_stats(self):
        return [
            (0.05, self.mean - self.std_dev * 2),
            (0.225, self.mean - self.std_dev),
            (0.5, self.mean),
            (0.225, self.mean + self.std_dev),
            (0.05, self.mean + self.std_dev * 2)
        ]

    def skewed_dist_stats(self):
        return [
            (0.1, self.p10),
            (0.2, self.p25),
            (0.5, self.p50),
            (0.2, self.p75)
            (0.1, self.p90)
        ]

class Inflation(StatsTester):
    

class Rates(StatsTester):
    pass
