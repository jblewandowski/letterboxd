from tkinter import ttk, W as WEST, SW as SOUTHWEST, Frame
import customtkinter as ctk
from .config import page_hierarchy, colors, fonts
from .page_manager import pages

ctk.set_default_color_theme('src/gui/assets/ctk_theme.json')

class Page(Frame):
    def __init__(self, path=[]):
        Frame.__init__(self)
        self.configure(bg=colors['bg'])
        self.menu = page_hierarchy
        self.path = path
        self.contents = {key : [] for key in self.menu_item_types.keys()}

        for i, path_item in enumerate(self.path):
            label = self.menu['top_menu_label']
            item = ttk.Label(self, text=label, padding=(10, 5), foreground=colors["fg_f"], 
                                background=colors["bg_d"], font=(fonts['top_menu']['family'], fonts['top_menu']['size']))
            item.grid(column=i*2, row=0, columnspan=1)

            item.bind('<Button-1>', lambda e, ind = i: self.superpage(path=self.path[0:ind]))
            item.bind('<Enter>', lambda e, item = item: item.config(foreground=colors["fg"]))
            item.bind('<Leave>', lambda e, item = item: item.config(foreground=colors["fg_f"]))

            seperator = ttk.Label(self, text='>', padding=(0, 5), foreground=colors["fg_f"], 
                                    background=colors["bg_d"], font=(fonts['top_menu']['family'], fonts['top_menu']['size']))
            seperator.grid(column=i*2+1, row=0, columnspan=1)

            self.menu = self.menu['menu_items'][path_item]

        label = self.menu['top_menu_label']
        item = ttk.Label(self, text=label, padding=(10, 5, 1000, 5), foreground=colors["fg"], 
                                    background=colors["bg_d"], font=(fonts['top_menu']['family'], fonts['top_menu']['size']))
        item.grid(column=len(self.path)*2, row=0, columnspan=1000)

        row = 2
        for menu_item in self.menu['menu_items']:
            self.menu_item_types[menu_item['type']](self, menu_item, row)
            row+=1

        # Perhaps position this element on the grid
        ttk.Separator(self).place(x=0, y=30, relwidth=1)

        if not hasattr(self, 'fin_info_text'):
            self._fin_info_text({'label':''})

    def show(self):
        self.lift()
    
    def redraw(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(path=self.path)

    def subpage(self, i):
        path = self.path + [i]
        pages[str(path)].show()
    
    def superpage(self, path):
        pages[str(path)].show()

    def _title(self, menu_item, row):
        font = fonts['title']
        _item = ttk.Label(self, text=f"{menu_item['label']}", padding = 10, foreground=colors['fg'], background=colors['bg'], font=(font['family'], font['size']))
        self.draw_item(_item, row, 'title')

    def _menu_item(self, menu_item, row):
        font = fonts['menu_item']
        _item = ttk.Label(self, text=f"{menu_item['label']}", padding=(40, 5), foreground=colors['fg_f'], background=colors['bg'], font=(font['family'], font['size']))
        _item.bind('<Button-1>', lambda e: self.subpage(i=row-2))
        _item.bind('<Enter>', lambda e: _item.config(foreground=colors['fg'], font=('Consolas', 12, 'underline')))
        _item.bind('<Leave>', lambda e: _item.config(foreground=colors['fg_f'], font=('Consolas', 12)))
        bullet = ttk.Label(self, text=">", padding = (10, 5), foreground=colors['fg_f'], background=colors['bg'], font=(font['family'], font['size']))
        bullet.grid(column = 0, row = row, columnspan = 1000, sticky=WEST)
        self.draw_item(_item, row, 'menu_item')

    def _text(self, menu_item, row):
        font = fonts['text']
        _item = ttk.Label(self, text=f"{menu_item['label']}", padding = 10, foreground=colors['fg'], background=colors['bg'], font=(font['family'], font['size']))
        self.draw_item(_item, row, 'text')

    def _button(self, menu_item, row):
        _item = ctk.CTkButton(self, text=menu_item['label'], command=menu_item['function'])
        _item.grid(**{'padx': 20, 'pady': 5})
        self.draw_item(_item, row, 'button')

    def _dropdown(self, menu_item, row):
        _item = ctk.CTkOptionMenu(self, values=menu_item['options'], width=150, command=menu_item['function'])
        _item.grid(**{'padx': 20, 'pady': 5})
        self.draw_item(_item, row, 'dropdown')

    def _entry(self, menu_item, row):
        font = fonts['text']
        _item = ctk.CTkEntry(self, placeholder_text=menu_item['label'], font=(font['family'], font['size']), width=150)
        _item.grid(**{'padx': 20, 'pady': 5})
        _item.bind('<Return>', menu_item['function'])
        self.draw_item(_item, row, 'entry')

    def _info_text(self, menu_item, row):
        font = fonts['info_text']
        _item = ttk.Label(self, text=menu_item['label'], padding = (10, 5), foreground=colors['fg_f'], background=colors['bg'], font=(font['family'], font['size']))
        self.draw_item(_item, row, 'info_text')
    
    def _fin_info_text(self, menu_item, row=1000):
        self.fin_info_text = ttk.Label(self, text=menu_item['label'], padding = (10, 5), foreground=colors['fg_f'],
                                  background=colors['bg'], font=(fonts['info_text']['family'], fonts['info_text']['size']))
        self.fin_info_text.grid(row=1000, column=0, columnspan=1000, sticky=SOUTHWEST)
    
    def draw_item(self, item, row, item_type):
        item.grid(column = 0, row = row, columnspan = 1000, sticky=WEST)
        self.contents[item_type].append(item)

    menu_item_types = {'title':_title, 'menu_item':_menu_item, 'text':_text, 'button':_button, 'dropdown':_dropdown, "entry":_entry, "info_text":_info_text, 'fin_info_text':_fin_info_text}

        
        

            
        