import matplotlib.pyplot as plt
from json import load

with open('src/graphing/settings.json') as file:
    settings = load(file)
colors = settings['colors']

plt.rcParams.update({'axes.edgecolor':colors['bg'],
                     'axes.facecolor':colors['bg'],
                     'figure.facecolor':colors['bg'],
                     'xtick.color':colors['tick'],
                     'ytick.color':colors['tick'],
                     'grid.color':colors['grid'],
                     'text.color':colors['text'],
                     'axes.labelcolor':colors['text']})

plt.rcParams.update({'font.family':'sans-serif',
                     'font.sans-serif':'Tw Cen MT',
                     'axes.titlesize':18,
                     'axes.labelsize':12})
