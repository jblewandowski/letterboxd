def import_previous():
    from json import load
    from gui.page_manager import pages
    try:
        with open('data/previous.json') as file:
            last_used = load(file)
    except:
        pages['[]'].fin_info_text.config(text='Warning: Failed to import data from previous session.')
        return

    try:
        with open(f"data/{last_used['user']}_letterboxd.json") as file:
            film_dict = load(file)['data']
    except:
        pages['[]'].fin_info_text.config(text='Warning: Failed to import data from previous session.')
        return
    
    import global_data
    from pandas import DataFrame
    global_data.film_dict = film_dict
    global_data.film_df = DataFrame(film_dict.values())
    global_data.user = last_used['user']
    global_data.userName = last_used['userName']
    global_data.accessed = last_used['accessed']

    from prepare_data import prepareData
    prepareData()
    pages['[]'].fin_info_text.config(text=f'Data for {global_data.user} currently loaded.')