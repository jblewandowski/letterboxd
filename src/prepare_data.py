def prepareData():
    from data_dict import categorical_data_instructions
    import global_data

    categorical_data = {}
    for key in categorical_data_instructions:
        categorical_data[key] = {'unlist':[], 'lookup':{}}
        if key != 'originalLanguage':
            unlist_id = [item for list in global_data.film_df[key].tolist() for item in list]
            unlist = [item for list in global_data.film_df[categorical_data_instructions[key]['tick']].tolist() for item in list]
        else:
            unlist_id = unlist = global_data.film_df[key].tolist()
        
        categorical_data[key]['unlist'] = unlist_id
        categorical_data[key]['lookup'] = dict(list(set(zip(unlist_id, unlist))))

    global_data.categorical_data = categorical_data