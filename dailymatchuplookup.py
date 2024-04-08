# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 23:28:13 2022

@author: robin
"""
import pandas as pd
z = []
date = input('What days matchups are you looking for?: ')
url = 'https://www.cbssports.com/fantasy/baseball/probable-pitchers/'
x, y, z = date.split(sep='-', maxsplit=-2)
game = pd.read_html(url+x+y+z+'')
print(game)


