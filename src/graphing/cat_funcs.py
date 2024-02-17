from global_data import userName, categorical_data, film_df, user
from data_dict import categorical_data_instructions
import matplotlib.pyplot as plt
from matplotlib import colormaps
from pandas import DataFrame, notnull, isnull
import numpy as np
from .color_funcs import get_color_gradient
from collections import Counter

include_unrated = 0

colors = ['#ecc270', '#f5e67e']

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
 
def barlistmaker(param, bars):
    df = DataFrame([categorical_data[param]['lookup'], Counter(categorical_data[param]['unlist'])]).transpose().rename(columns={0:'title', 1:'count'})
    df = df.sort_values(by = ['count', 'title'], ascending = [True, False])[-bars:]
    df['userRating'] = [film_df[film_df.apply(lambda x: i in x[param], axis = 1)]['userRating'] for i in df.index]
    df['ratingValue'] = [film_df[film_df.apply(lambda x: i in x[param], axis = 1)].loc[notnull(film_df['userRating'])]['ratingValue'] for i in df.index]
    df['userRatingAvg'] = [np.mean(i) / 2 if len(i) > 0 else 0 for i in df['userRating']]
    df['ratingValueAvg'] = [np.mean(i) if len(i) > 0 else 0 for i in df['ratingValue']]
    return df

def barnum(param, bars):
    if bars >= 0:
        if len(categorical_data[param]['lookup']) < bars:
            return len(categorical_data[param]['lookup'])
        return 18 if param == 'genre' else bars
    else: 
        return sum(i >= -bars for i in Counter(categorical_data[param]['unlist']).values())
    
def BarChart(param, df, bars):
    bar = plt.barh('title', 'count', data = df, color = get_color_gradient(colors[0], colors[1], bars), zorder=10)
    plt.bar_label(bar, color = 'white', fontsize = '8', padding=2)
    plt.grid(axis='x', zorder=1)
    plt.title(f"Films Watched by {categorical_data_instructions[param]['title']}".upper(), fontsize = 18)

def stackedBarChart(param, df, bars):
    mini_df = film_df[['userRating', param]]
    for i in range(11):
        df2 = mini_df[isnull(mini_df['userRating'])] if i == 0 else mini_df.loc[(mini_df['userRating'] == i)]
        _count = Counter([item for items in df2[param] for item in items])
        df[str(i)] = [_count[id] for id in df.index]

    bar = plt.barh('title', 'count', data = df, color = 'white', zorder=9)
    plt.bar_label(bar, color = 'white', fontsize = '8', padding=2)

    offset = [0] * bars
    for i in range(11):
        plt.barh(df['title'], df[str(i)], 
                 color = color['bar_rat'][i], edgecolor = color['bg'],
                 label = str(i / 2) if i != 0 else 'None',
                 left = offset, zorder=10)
        offset = [sum(x) for x in zip(offset, df[str(i)])]

    plt.grid(axis='x', zorder=1)
    plt.title((f"{userName}'s {bars} most watched {categorical_data_instructions[param]['title_p']}" if param != 'genre' else 
               f"{userName}'s films watched by genre").upper(), fontsize = 18)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [10 - include_unrated - i for i in range(10 + include_unrated)]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], title = 'Rating')

def proportionBarChart(param, df, bars):
    mini_df = film_df[['userRating', param]]
    sorter = {}
    for i, rating in enumerate([5.5] + list(range(1, 11))):      # Unrated films take rating of 5.5 (2.75) in sorting calculation
        df2 = mini_df[isnull(mini_df['userRating'])] if i == 0 else mini_df.loc[(mini_df['userRating'] == i)]
        _count = Counter([item for items in df2[param] for item in items])
        df[str(i)] = [_count[id] / df['count'][id] for id in df.index]
        sorter[i] = [_count[id] * rating**2 for id in df.index]
    df['sorter'] = [sum([sorter[j][i] for j in range(11)]) / df['count'][i] for i in range(bars)]
    df = df.sort_values(by = 'sorter')
        
    offset = [0] * bars
    for i in range(11):
        plt.barh(df['title'], df[str(i)], 
                    color = color['bar_rat'][i], edgecolor = color['bg'],
                    label = str(i / 2) if i != 0 else 'None', 
                    left = offset, zorder=1)
        offset = [sum(x) for x in zip(offset, df[str(i)])]

    plt.grid(axis='x', zorder=20, linestyle = 'dashed')
    plt.title((f"{userName}'s {bars} most watched {categorical_data_instructions[param]['title_p']}\n weighted ranking, Proportion by Rating" if param != 'genre' else 
               f"{userName}'s films watched by genre\n weighted ranking, Proportion by Rating").upper(), fontsize = 16)
    plt.margins(y = 0.25 / bars)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [10 - include_unrated - i for i in range(10 + include_unrated)]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], title = 'Rating', bbox_to_anchor=(1, 0.9))

def averageBarChart(param, df, bars):
    df = df.sort_values(by = 'userRatingAvg')
    bar = plt.barh('title', 'userRatingAvg', data = df, color = get_color_gradient(colors[0], colors[1], bars), zorder=10)
    plt.bar_label(bar, color = 'white', fontsize = '8', padding=2, fmt='%.2f')
    plt.grid(axis='x', zorder=1)
    plt.title(f"{userName}'s Average Rating by {categorical_data_instructions[param]['title']}".upper(), fontsize = 18)

def draw(function, param, bars = 15):
    bars = barnum(param, bars)
    plt.figure(figsize=(8, 1.5 + bars / 4.5))
    df = barlistmaker(param, bars)
    function(param, df, bars)
    plt.tight_layout()
    plt.text(0, 0, f'User: {user}', ha = 'left', va = 'bottom', color = color['dark_grid'], transform=plt.gcf().transFigure)
    import os
    if not os.path.exists(f"saved figures/{user}/"):
        os.makedirs(f"saved figures/{user}/")
    plt.savefig(f"saved figures/{user}/{user}_{categorical_data_instructions[param]['title']}_{function.__name__}_{bars}.png", dpi=300)
    return f"{user}_{categorical_data_instructions[param]['title']}_{function.__name__}_{bars}.png"