# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:21:39 2018

@author: vostok
"""

import requests
from bs4 import BeautifulSoup

def strip_whitespace(text):
    text = text.replace('\n', '')
    text = ' '.join(text.split())
    return text

def parse_single(table):
    
    def single_generator(table):
        tds = table.find_all('td')
        
        if len(tds) == 2 and tds[0].span.text == '+': # should be a notam row
            
            # first row with actual notam text should be inside the first span
            yield strip_whitespace(tds[1].span.text) 
            
            # rest of rows, with LOWER/UPPER, FROM/TO and possible SCHEDULE
            # these should be inside one p each
            ps = tds[1].find_all('p')
            for p in ps:
                yield strip_whitespace(p.text) 
    
    single_list = list(single_generator(table))
    
    return single_list

def area_names(notam):
    all_areas = re.findall('EF[DR]\d+\S+', notam)
    return all_areas




url = 'https://www.ais.fi/ais/bulletins/envfrm.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tables = [t for t in soup.find_all('table')]

for table in tables:
    lines = parse_single(table)
    
    if len(lines):
        print(lines[0])
        print(area_names(lines[0]))
        print()

