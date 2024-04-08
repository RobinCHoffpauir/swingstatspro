# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 17:06:32 2021

@author: robin
"""
import pybaseball as pyb
import pandas as pd
pd.options.display.max_columns = None


class Player:
    def __init__(self, fname, lname, year, playerid=None):
        self.year = year
        self.fname = fname
        self.lname = lname
        x = pyb.playerid_lookup(self.lname, self.fname)
        self.id = x['key_mlbam']
        self.bbref = x['key_bbref']
        self.fg_id = x['key_fangraphs']
        self.info = pyb.people().query('playerID in @self.bbref.values')
        self.college = pyb.college_playing().query(
            'playerID in @self.bbref.values')[['schoolID', 'yearID']]
        print(self.info.dropna(axis=1, how='all'))

    def get_batting_stats(self):
        z = pyb.batting()
        return z.query('playerID in @self.bbref.values')

    #def get_matchup(self, opp_pitcher):
        #z = pyb.batting()
        #if
