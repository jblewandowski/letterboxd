def start():
    from .page_manager import pages
    pages['[]'].show()

    from global_data import root
    root.mainloop()