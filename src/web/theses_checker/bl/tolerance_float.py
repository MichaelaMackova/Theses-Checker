#----------------------------------------------------------------------------
# File          : tolerance_float.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 29.01.2025
# Last Updated  : 29.01.2025
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

import numpy

class ToleranceFloat:
    def __init__(self, number):
        self.number = number
        self.__rtol=1e-05
        self.__atol=1e-08

    def __eq__(self, other : 'ToleranceFloat'):
        return numpy.isclose(self.number, other.number, rtol=self.__rtol, atol=self.__atol, equal_nan=False)
    
    def __ne__(self, other : 'ToleranceFloat'):
        return not self.__eq__(other)
    
    def __lt__(self, other : 'ToleranceFloat'):
        return self.number < other.number
    
    def __le__(self, other : 'ToleranceFloat'):
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other : 'ToleranceFloat'):
        return self.number > other.number
    
    def __ge__(self, other : 'ToleranceFloat'):
        return self.__gt__(other) or self.__eq__(other)
    
    def __str__(self):
        return str(self.number)
    
    def __repr__(self):
        return str(self.number)
        