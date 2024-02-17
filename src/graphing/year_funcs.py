from global_data import film_df, userName, user
import matplotlib.pyplot as plt
import json
from pandas import DataFrame, isna, concat
import numpy as np
from .color_funcs import get_color_gradient
from collections import Counter, defaultdict
from matplotlib import colormaps

include_unrated = 0


colors = ['#ecc270', '#f5e67e']
yearEndings = ['', '0s', '00s', '000s']
yearTitles = ['Year', 'Decade', 'Century', 'Millennium']

color = {
    'bg':'#1a1c1f',
    'grid':'#414141',
    'dark_grid':'#2C2D2E',
    'dual_tone':['#78b7ed', '#df8133'],
    'rat_p':['#ecc270', '#f5e67e'],
    'hist_p':['#77d671', '#78b7ec'],
    'r_p':['#ea6b7f', '#df3366'],
    'o_p':['#eab66b', '#df8133'],
    'y_p':['#eae06b', '#dfba33'],
    'g_p':['#96fb8e', '#79da64'],
    'c_p':['#6be9ea', '#33dfc9'],
    'b_p':['#a4edfc', '#78b7ed'],
    'i_p':['#8c6bea', '#4833df'],
    'p_p':['#cb6bea', '#9e33df'],
    'm_p':['#ea6bbf', '#df33bc'],
    'bar_rat':[colormaps['viridis'](i) for i in np.linspace(0, 1, 10)],
    'bar_none':'#5d5f61'
}

color['bar_rat'] = [color['bar_none']] + color['bar_rat']

def yearDF(time):
    years = [year // 10**time for year in film_df['releaseYear']]
    count = Counter(years)
    userRatings = defaultdict(list)
    for year, rating in zip(years, film_df['userRating']):
        userRatings[year].append(rating)
    min_year, max_year = (min(count.keys()), max(count.keys()))
    title = {year : f"{year}{yearEndings[time]}" for year in range(min_year, max_year + 1)} if time else \
            {year : year for year in range(min_year, max_year + 1)}
    df = DataFrame([title, count, userRatings]).transpose().rename(columns={0:'title', 1:'count', 2:'userRatings'}).sort_index().fillna(0)
    return df

def avgYearChart(time, df):
    df['userRatingAvg'] = df.apply(lambda x: sum(x['userRatings']) / x['count'] / 2 if x['count'] else None, axis=1)
    plt.bar('title', 'userRatingAvg', data = df, 
            width = (0.8 if time else 0.5), 
            color = get_color_gradient(colors[0], colors[1], len(df.index)),
            zorder=10)
    plt.grid(axis='y', zorder = 1)
    plt.title(f"{userName}'s Average Rating by {yearTitles[time]}".upper(), fontsize = 18)
    if time == 0:
        plt.xticks([year * 10 for year in range(int((df.index[0] + 9)/10), int(df.index[-1] / 10) + 1)])
        
def YearChart(time, df):
    bar = plt.bar('title', 'count', data = df, 
                  width = (0.8 if time else 0.5), 
                  color = get_color_gradient(colors[0], colors[1], len(df.index)),
                  zorder=10)
    plt.bar_label(bar, df['count'] if time else jakemax(df['count'].tolist()))
    plt.grid(zorder=1)
    plt.title(f"{userName}'s Films Watched by {yearTitles[time]}".upper(), fontsize = 18)

def stackedYearChart(time, df):
    df2 = DataFrame.from_dict(df['userRatings'].apply(lambda x: dict(Counter(x)) if x else {}).tolist()).fillna(0).astype(int)
    for i in range(11): 
        if i not in df2.columns: df2[i] = 0
        df[i] = df2[i].tolist()

    offset = [0] * len(df.index)
    for i in range(11):
        bar = plt.bar(df['title'], df[i], 
                 color = color['bar_rat'][i], edgecolor = color['bg'],
                 label = str(i / 2) if i != 0 else 'None',
                 bottom = offset, zorder=10)
        offset = [sum(x) for x in zip(offset, df[i])]

    plt.grid(zorder=1)
    plt.bar_label(bar, df['count'] if time else jakemax(df['count'].tolist()))
    plt.title(f"{userName}'s Films Watched by {yearTitles[time]}".upper(), fontsize = 18)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [10 - include_unrated - i for i in range(10 + include_unrated)]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], title = 'Rating')

def proportionYearChart(time, df):
    df2 = DataFrame.from_dict(df['userRatings'].apply(lambda x: dict(Counter(x)) if x else {}).tolist()).fillna(0).astype(int)
    for i in range(11): 
        if i not in df2.columns: df2[i] = 0
        df[i] = df2[i].tolist() / df['count']

    offset = [0] * len(df.index)
    for i in range(11):
        bar = plt.bar(df['title'], df[i], 
                 color = color['bar_rat'][i], edgecolor = color['bg'],
                 label = str(i / 2) if i != 0 else 'None',
                 bottom = offset, zorder=10)
        offset = [sum(x) for x in zip(offset, df[i])]

    plt.grid(zorder=1)
    plt.title(f"{userName}'s Films Watched by {yearTitles[time]}\nProportion by Rating".upper(), fontsize = 18)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [10 - include_unrated - i for i in range(10 + include_unrated)]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], title = 'Rating', bbox_to_anchor=(1, 0.9))

def jakemax(lst):
    max_val = max(lst)
    max_ind = lst.index(max_val)
    def clamp(n, largest):
        return max(0, min(n, largest))
    def is_local_max(i, val):
        return val == max(lst[clamp(i-4, len(lst)):clamp(i+4, len(lst))])
    def is_locally_extreme(i, val):
        return val > ((1 / (1 + np.exp(10 * ((val / max_val) - 0.3)))) + 1) * np.average(lst[clamp(i-4, len(lst)):clamp(i+4, len(lst))])
    def is_locally_unique(i, val):
        return lst[clamp(i-4, len(lst)):clamp(i+4, len(lst))].count(val) == 1
    return [f'{val}' if i == max_ind or (val > 3 and is_local_max(i, val) and is_locally_extreme(i, val) and is_locally_unique(i, val)) else '' for i, val in enumerate(lst)]
   
def draw(function, time):
    plt.figure(figsize=(10, 4))
    df = yearDF(time)
    function(time, df)
    plt.tight_layout()
    plt.text(0, 0, f'User: {user}', ha = 'left', va = 'bottom', color = color['dark_grid'], transform=plt.gcf().transFigure)
    import os
    if not os.path.exists(f"saved figures/{user}/"):
        os.makedirs(f"saved figures/{user}/")
    plt.savefig(f"saved figures/{user}/{user}_{yearTitles[time]}_{function.__name__}.png", dpi=300)
    return f"{user}_{yearTitles[time]}_{function.__name__}.png"
    