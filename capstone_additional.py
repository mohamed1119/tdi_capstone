#!/usr/bin/python

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Taken fron http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
state_abbreviations = {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}

states = state_abbreviations.values()
states.sort()

import re

pattern = re.compile(r'.*Net generation : (.+) : (.+) : electric power.*annual.*"2017",([0-9\.]+)')

power_data = {}

# parse datasets for relevant information
with open('datasets/ELEC.txt', 'r') as textfile:
    for line in textfile:
        m = pattern.match(line)
        if m:
            fueltype = m.group(1)
            state = m.group(2)
            if (state == 'District Of Columbia'):
                state = 'District of Columbia'
            pgen = float(m.group(3))
            try:
                power_data[state]
            except:
                power_data[state] = {'conventional hydroelectric': 0.0, 'other renewables (total)': 0.0, 'all fuels': 0.0}

            power_data[state][fueltype] = pgen

percent_renewable = map(lambda s: 100.0*(power_data[s]['conventional hydroelectric'] + power_data[s]['other renewables (total)'])/power_data[s]['all fuels'], states)

plt.rcParams['font.size'] = 8
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

x = np.arange(len(states))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(5.0, 5.0))
rects1 = ax.bar(x, percent_renewable, width*2, color='Green', label='Electricity Demand')

ax.set_xlim( (-0.5, 0.0 + len(states) ) )

ax.set_ylabel('% of Electricity Generation that is Renewable')
ax.set_title('Percentage of Renewable Energy Generation by State')
ax.set_xlabel('State')
ax.set_xticks(x)
ax.set_xticklabels(states, verticalalignment="top", horizontalalignment="center", rotation=90, fontsize=8)

fig.tight_layout()

plt.savefig( "Percent-Renewable.pdf", bbox_inches="tight" )

