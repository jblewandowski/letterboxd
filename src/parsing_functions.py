import global_data
from gui.page_manager import pages


def file_open():
    current_page = pages['[1]']
    from tkinter import filedialog
    fileName = filedialog.askopenfilename()
    if not fileName.endswith('_letterboxd.json'):
        current_page.contents['info_text'][0].config(text=f"Invalid file.\nPlease try again.")
        return

    from os import path
    from time import strftime, localtime
    fileCreationDate = strftime('%Y-%m-%d', localtime(path.getctime(fileName)))
    if fileCreationDate < '2024-02-16':
        current_page.contents['info_text'][0].config(text=f"Failed to import data.\nSelected JSON file is outdated. Please redownload data using the module below.")
        return
    
    try:
        from json import load, dump
        with open(fileName) as file:
            file = load(file)
            film_dict = file['data']
            user_info = file['info']
            user = user_info['user']
        if not fileName.endswith(f'data/{user}_letterboxd.json'):
            with open(f'data/{user}_letterboxd.json', 'w') as file:
                dump({'info':user_info, 'data':film_dict}, file, indent=4)
        with open(f'data/previous.json', 'w') as file:
                dump(user_info, file, indent=4)

        from pandas import DataFrame
        film_df = DataFrame(film_dict.values())
        
        global_data.film_dict = film_dict
        global_data.film_df = film_df
        global_data.user = user
        global_data.userName = user_info['userName']
        global_data.accessed = user_info['accessed']

        from prepare_data import prepareData
        prepareData()

        current_page.contents['info_text'][0].config(text=f"Successfully imported {fileName.split('/')[-1]}\n")
        pages['[]'].fin_info_text.config(text=f'Data for {global_data.user} currently loaded.')

    except:
        current_page.contents['info_text'][0].config(text=f"Failed to import data\n")
        return

def download_data(*args):
    current_page = pages['[1]']
    user = current_page.contents['entry'][0].get().lower().strip()
    if global_data.user == user and global_data.already_downloaded == True:
        return
    
    from user_validation import user_validation
    userName = user_validation(user)
    if not userName:
        current_page.contents['info_text'][1].config(text=f"User {user} not valid\nPlease try again")
        return
    
    global_data.user = user
    global_data.userName = userName
    current_page.contents['info_text'][1].config(text=f"Downloading...\n")

    def fuck():
        try:
            from scraper import scrape
            film_dict, t = scrape(user)

            from datetime import date
            user_info = {
                'user':global_data.user,
                'userName':global_data.userName,
                'fileName':f'data/{user}_letterboxd.json',
                'accessed':str(date.today())}
            
            from json import dump
            with open(f'data/{user}_letterboxd.json', 'w') as file:
                dump({'info':user_info, 'data':film_dict}, file, indent=4)
            with open(f'data/previous.json', 'w') as file:
                dump(user_info, file, indent=4)

            from pandas import DataFrame
            film_df = DataFrame(film_dict.values())
            global_data.film_dict = film_dict
            global_data.film_df = film_df

            from prepare_data import prepareData
            prepareData()

            current_page.contents['info_text'][1].config(text=f"Successfully downloaded and imported Letterboxd data for {global_data.userName}\nTime elapsed: {t:0.2f} seconds")
            pages['[]'].fin_info_text.config(text=f'Data for {global_data.user} currently loaded.')

        except:
            current_page.contents['info_text'][1].config(text=f"Failed to download data\nBother Jake about it")
    
    from threading import Thread
    Thread(target=fuck).start()

def year_charter(*args):
    current_page = pages['[2, 1]']
    from graphing.year_funcs import YearChart, avgYearChart, stackedYearChart, proportionYearChart, draw

    func_dict = {
        'Histogram':YearChart,
        'Histogram with Stacked Bars':stackedYearChart,
        'Rating Proportions':proportionYearChart,
        'Average Rating':avgYearChart,
    }

    time_dict = {
        'Year':0,
        'Decade':1,
        'Century':2,
        'Millennium':3
    }

    func_drop = current_page.contents['dropdown'][0].get()
    time_drop = current_page.contents['dropdown'][1].get()
    title = draw(func_dict[func_drop], time_dict[time_drop])
    current_page.fin_info_text.config(text=f"Successfully saved {title} to /saved figures/{global_data.user}/")

def cat_charter(*args):
    current_page = pages['[2, 2]']
    from graphing.cat_funcs import BarChart, averageBarChart, stackedBarChart, proportionBarChart, draw
    
    func_dict = {
        'Standard Bar Chart':BarChart,
        'Bars Stacked by Rating':stackedBarChart,
        'Rating Proportions':proportionBarChart,
        'Average Rating':averageBarChart,
        'Rating Line Density Plots':print,
        'User vs Letterboxd Avg':print
    }
    
    param_dict = {
        'Actor': 'actors_id', 
        'Country': 'countryOfOrigin', 
        'Director': 'director_id', 
        'Editor': 'editor_id', 
        'Genre': 'genre', 
        'Cinematographer': 'cinematography_id', 
        'Spoken Language': 'language', 
        'Composer': 'composer_id', 
        'Original Language': 'originalLanguage', 
        'Producer': 'producer_id', 
        'Studio': 'productionCompany_id', 
        'Theme': 'theme', 
        'Writer': 'writer_id'
    }
    
    func_drop = current_page.contents['dropdown'][0].get()
    param_drop = current_page.contents['dropdown'][1].get()
    try:
        bar_entry = 15 if current_page.contents['entry'][0].get().strip() == '' else int(current_page.contents['entry'][0].get().strip())
        current_page.contents['info_text'][0].config(text=f"")
    except:
        current_page.contents['info_text'][0].config(text=f"Please input a numerical value for the number of bars.")
        return

    title = draw(func_dict[func_drop], param_dict[param_drop], bar_entry)
    current_page.fin_info_text.config(text=f"Successfully saved {title} to /saveed figures/{global_data.user}/")

# def input_updater(*args):
#     cat_page = pages['[2, 2]']
#     year_page = pages['[2, 1]']

#     cat_page_inputs = []
#     for input_option in cat_page.contents['dropdown']:
#         cat_page_inputs.append

#     print(args)