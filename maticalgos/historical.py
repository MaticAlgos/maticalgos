# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 01:22:06 2022

@author: neera
"""

import requests
import datetime
import pandas as pd

class historical: 
    def __init__(self, email):
        self.email = email
        self.url = "http://historical.maticalgos.com"
        self.check_login = False
    
    def login(self, password):
        self.s = requests.Session()
        payload_dict = {"email": self.email, "password": str(password)}
        r = self.s.post(self.url + '/login', json = payload_dict)
        n = r.json()
        if n['Login_details'] == "failed": 
            raise Exception(n['error'])
        self.check_login = True
    
    def reset_password(self):
        payload = {"email": self.email}
        r = requests.post(self.url + "/reset", json = payload)
        n = r.json()
        if n['reset-password'] == "Failed":
            raise Exception(n['error'])
        
    def get_data(self, symbol, dat):
        if type(dat) == datetime.date: 
            if symbol != "nifty" and symbol != "banknifty":
                raise Exception("Data available only for nifty and banknifty")
            else: 
                nam = "BNF" if symbol == "banknifty" else "NF" if symbol == "nifty" else None
                if self.check_login == False:
                    raise Exception('User not logged in.')
                dt = dat.strftime("%Y%m%d")
                r = self.s.get(self.url + f"/historicalapi/{nam}/{dt}")
                n = r.json()
                
                if n['status'] == False:
                    raise Exception(n['error'])
                else:
                    df = pd.DataFrame.from_dict(n['data'])
                    return df
        else: 
            raise Exception("Please enter date in datetime.date format")
    
