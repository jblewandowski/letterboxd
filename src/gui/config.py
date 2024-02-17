from parsing_functions import *

page_hierarchy = {
    "type":"main",
    "top_menu_label":"Main Menu",
    "menu_items":[
        {
            "type":"title",
            "label":"Letterboxd Data Visualizer"
        },
        {
            "type":"menu_item",
            "label":"Import Data",
            "top_menu_label":"Import Data",
            "menu_items":[
                {
                    "type":"title",
                    "label":"Data Importer"
                },
                {
                    "type":"text",
                    "label":"Open JSON:"
                },
                {
                    "type":"button",
                    "function":file_open,
                    "label":"Browse Files"
                },
                {
                    "type":"info_text",
                    "label":"\n"
                },
                {
                    "type":"text",
                    "label":"Download Data:"
                },
                {
                    "type":"entry",
                    "label":"Letterboxd Username",
                    "function":download_data
                },
                {
                    "type":"button",
                    "function":download_data,
                    "label":"Download"
                },
                {
                    "type":"info_text",
                    "label":"\n"
                },
                {
                    "type":"text",
                    "label":"\n",
                },
                {
                    "type":"fin_info_text",
                    "label":"The most recently used JSON file is automatically imported.\nDownloaded data is automatically imported and saved as */data/user_letterboxd.json"
                }
            ]
        },
        {
            "type":"menu_item",
            "label":"Visualizer",
            "top_menu_label":"Visualizer",
            "menu_items":[
                {
                    "type":"title",
                    "label":"Select Visualization Type:"
                },
                {
                    "type":"menu_item",
                    "label":"Year Bar Charts",
                    "top_menu_label":"Year Bar Charts",
                    "menu_items":[
                        {
                            "type":"text",
                            "label":"Chart Type:"
                        },
                        {
                            "type":"dropdown",
                            "options":['Average Rating', 'Histogram', 'Histogram with Stacked Bars', 'Rating Proportions'],
                            "function":None
                        },
                        {
                            "type":"text",
                            "label":"Time Interval:"
                        },
                        {
                            "type":"dropdown",
                            "options":["Year", "Decade", "Century", "Millennium"],
                            "function":None
                        },
                        {
                            "type":"text",
                            "label":"\n\n",
                        },
                        {
                            "type":"button",
                            "function":year_charter,
                            "label":"Save Figure"
                        }
                    ]
                },
                {
                    "type":"menu_item",
                    "label":"Categorical Bar Charts",
                    "top_menu_label":"Categorical Bar Charts",
                    "menu_items":[
                        {
                            "type":"text",
                            "label":"Chart Type:"
                        },
                        {
                            "type":"dropdown",
                            "options":[
                                'Standard Bar Chart',
                                'Bars Stacked by Rating',
                                'Rating Proportions',
                                'Average Rating',
                                # 'Rating Line Density Plots',
                                # 'User vs Letterboxd Avg'
                                ],
                            "function":None
                        },
                        {
                            "type":"text",
                            "label":"Category:"
                        },
                        {
                            "type":"dropdown",
                            "options":[
                                'Actor', 
                                'Country', 
                                'Director', 
                                'Editor', 
                                'Genre', 
                                'Cinematographer', 
                                'Spoken Language', 
                                'Composer', 
                                'Original Language', 
                                'Producer', 
                                'Studio', 
                                'Theme', 
                                'Writer'],
                            "function":None
                        },
                        {
                            "type":"text",
                            "label":"Number of Bars:"
                        },
                        {
                            "type":"entry",
                            "label":"Default: 15",
                            "function":None
                        },
                        {
                            "type":"info_text",
                            "label":"",
                        },
                        {
                            "type":"text",
                            "label":"\n\n",
                        },
                        {
                            "type":"button",
                            "function":cat_charter,
                            "label":"Save Figure"
                        }
                    ]
                },
                {
                    "type":"menu_item",
                    "label":"Scatter Plots",
                    "top_menu_label":"Scatter Plots",
                    "menu_items":[
                        {
                            "type":"text",
                            "label":'Coming Soon'
                        },
                        {
                            "type":"text",
                            "label":"\n\n",
                        },
                        {
                            "type":"button",
                            "function":None,
                            "label":"Save Figure"
                        }
                    ]
                },
                {
                    "type":"menu_item",
                    "label":"Other Charts",
                    "top_menu_label":"Other Charts",
                    "menu_items":[
                        {
                            "type":"text",
                            "label":'Coming Soon'
                        },
                        {
                            "type":"text",
                            "label":"\n\n",
                        },
                        {
                            "type":"button",
                            "function":None,
                            "label":"Save Figure"
                        }
                    ]
                }
            ]
        },
        {
            "type":"menu_item",
            "label":"Settings",
            "top_menu_label":"Settings",
            "menu_items":[
                {
                    "type":"title",
                    "label":"Settings & Info"
                }
            ]
        }
    ]
}

colors = {
    "bg": "#212121",
    "bg_d": "#181818",
    "fg": "#fff",
    "fg_f": "#bbb",
    "hover": "#363737"
}

fonts = {
    "title":{
        "family": "Consolas",
        "size":16
    },
    "menu_item":{
        "family": "Consolas",
        "size":12
    },
    "text":{
        "family": "Consolas",
        "size":12
    },
    "button":{
        "family": "Consolas",
        "size":12
    },
    "top_menu":{
        "family": "Consolas",
        "size":10
    },
    "info_text":{
        "family": "Consolas",
        "size":10
    }
}
