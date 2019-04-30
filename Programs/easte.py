# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:31:11 2019

@author: Santosh
"""

    
def reemovNestings(l): 
    for i in l: 
        if type(i) == list: 
            reemovNestings(i) 
        else: 
            output.append(i) 
    return output
        
input1 = [1, 2, [3, 4, [5, 6]], 7, 8, [9, [10]]]
output = [] 
print(reemovNestings(input1))