from .page import Page
from .page_manager import pages

def pagecreator(root, menu_item, path = []):
    if menu_item['type'] == "menu_item" or path == []:
        new_page = Page(path)
        new_page.rowconfigure(1000, weight=1)
        new_page.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        pages[str(path)] = new_page
        for i, item in enumerate(menu_item["menu_items"]):
            pagecreator(root, item, path + [i])