# -*- coding: utf-8 -*-
"""
Created on Sat May  4 22:10:56 2019

@author: Santosh
"""

import preprocess as pp
import findDimensions as fd

width = 24.
path = 'Images\image9.jpeg'

        
edged=pp.init(path)
fd.process(path, edged, width)