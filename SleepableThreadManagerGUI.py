import ttk
from Tkinter import *
from ttk import Treeview
from SleepableThreadManager import *


class SleepableThreadManagerGUI:
    ui = None  # Main UI Window

    top = None  # Top UI frame
    center = None  # Middle UI frame
    bottom = None  # Bottom UI frame

    manager = None  # Sleepable thread manager

    ui_update_thread = None  # UI Update thread

    thread_dropdown = None  # Dropdown to select threads
    function_dropdown = None  # Dropdown to select functions

    thread_selected = None  # Variable for the thread selection
    function_selected = None  # Variable for the function selection

    create_thread_button = None  # Create a thread
    remove_thread_button = None  # Removed specified thread
    remove_all_button = None  # Remove all threads

    start_thread_button = None  # Start specified thread
    start_all_button = None  # Start all threads

    restart_thread_button = None  # Restart specified thread
    restart_all_button = None  # Restart all threads

    sleep_thread_button = None  # Sleep specified thread
    sleep_all_button = None  # Sleep all threads

    stop_thread_button = None  # Stop specified thread
    stop_all_button = None  # Stop all threads

    set_thread_function_button = None  # Set specified thread to specified funciton
    set_all_function_button = None  # Set all threads to specified funciton

    info_tree_view = None  # Tree view for thread info
    output_textbox = None  # Output textbox for the UI thread to write to

    def __init__(self):
        self.manager = SleepableThreadManager()

        self.ui = Tk()
        self.ui.title('Sleepable Thread Manager')
        self.ui.geometry('550x600')

        self.function_selected = StringVar(self.ui)
        self.thread_selected = StringVar(self.ui)

        self.thread_selected.set('Select a Thread...')
        self.function_selected.set('Select a Function...')

        # create all of the main containers
        self.top = Frame(self.ui, width=300, height=50, pady=5)
        self.center = Frame(self.ui, bg='yellow', width=300, height=100, padx=0, pady=0)
        self.bottom = Frame(self.ui, bg='orange', width=300, height=20, pady=0)

        # main window
        self.ui.grid_columnconfigure(0, weight=1)  # expand main column when main ui resizes
        self.top.grid(row=0, sticky="ew")  # Stick top frame to east/west
        self.center.grid(row=1, sticky="ew")  # Stick center frame to east/west
        self.bottom.grid(row=2, sticky="nsew")  # Stick bottom frame to north/south/easy/west
        self.ui.grid_rowconfigure(2, weight=1)  # Expand bottom panel when main ui resizes

        # top frame component config
        self.top.grid_rowconfigure(0, weight=1)  # Expand first row when top frame resizes
        self.top.grid_rowconfigure(1, weight=1)  # Expand second row when top frame resizes
        self.top.grid_columnconfigure(1, weight=1)  # Expand second column when top frame resizes

        # center frame component config
        self.center.grid_columnconfigure(0, weight=1)  # Expand column one when middle frame resizes
        self.center.grid_columnconfigure(1, weight=1)  # Expand column two when middle frame resizes
        self.center.grid_columnconfigure(2, weight=1)  # Expand column two when middle frame resizes
        self.center.grid_columnconfigure(3, weight=1)  # Expand column two when middle frame resizes

        # bottom frame component config
        self.bottom.grid_rowconfigure(0, weight=1)  # Expand row 1 when bottom frame resizes
        self.bottom.grid_rowconfigure(1, weight=1)  # Expand row 2 when bottom frame resizes
        self.bottom.grid_rowconfigure(1, weight=2)  # Expand row 2 when bottom frame resizes
        self.bottom.grid_columnconfigure(0, weight=1)  # Expand column 1 when bottom frame resizes

        # create widgets for top frame
        thread_label = Label(self.top, text='Thread name:')
        function_label = Label(self.top, text='Function name:')
        self.thread_dropdown = OptionMenu(self.top, self.thread_selected, self.thread_selected.get())
        self.function_dropdown = OptionMenu(self.top, self.function_selected, *self.manager.function_mappings.keys())

        # layout the widgets in the top frame
        thread_label.grid(row=0, column=0)
        function_label.grid(row=1, column=0)
        self.thread_dropdown.grid(row=0, column=1, columnspan=3, sticky="ew")
        self.function_dropdown.grid(row=1, column=1, columnspan=3, sticky="ew")

        # create widgets for center frame
        self.create_thread_button = Button(self.center, text="Create Thread", command=self.create_thread,
                                           background='light blue')
        self.remove_thread_button = Button(self.center, text="Remove Thread", command=self.remove_thread,
                                           background='deep sky blue')
        self.remove_all_button = Button(self.center, text="Remove All", command=self.remove_all,
                                        background='steel blue')

        self.start_thread_button = Button(self.center, text="Start Thread", command=self.start_thread,
                                          background='green')
        self.start_all_button = Button(self.center, text="Start All", command=self.start_all, background='green3')

        self.restart_thread_button = Button(self.center, text="Restart Thread", command=self.restart_thread,
                                            background='orange')
        self.restart_all_button = Button(self.center, text="Restart All", command=self.restart_all,
                                         background='orange3')

        self.sleep_thread_button = Button(self.center, text="Sleep Thread", command=self.sleep_thread,
                                          background='yellow')
        self.sleep_all_button = Button(self.center, text="Sleep All", command=self.sleep_all, background='yellow3')

        self.wake_thread_button = Button(self.center, text="Wake Thread", command=self.wake_thread, background='orange')
        self.wake_all_button = Button(self.center, text="Wake All", command=self.wake_all, background='orange3')

        self.stop_thread_button = Button(self.center, text="Stop Thread", command=self.stop_thread, background='red')
        self.stop_all_button = Button(self.center, text="Stop All", command=self.stop_all, background='red3')

        self.set_thread_function_button = Button(self.center, text="Set Thread Function",
                                                 command=self.set_thread_function, background='purple')
        self.set_all_function_button = Button(self.center, text="Set All Functions", command=self.set_all_function,
                                              background='purple3')

        # layout the widgets in the center frame
        self.create_thread_button.grid(row=0, column=0, sticky='ew')
        self.remove_thread_button.grid(row=0, column=1, sticky='ew')
        self.remove_all_button.grid(row=0, column=2, columnspan=2, sticky='ew')

        self.set_thread_function_button.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.set_all_function_button.grid(row=1, column=2, columnspan=2, sticky='ew')

        self.start_thread_button.grid(row=2, column=0, sticky='ew')
        self.start_all_button.grid(row=2, column=2, sticky='ew')

        self.restart_thread_button.grid(row=2, column=1, sticky='ew')
        self.restart_all_button.grid(row=2, column=3, sticky='ew')

        self.stop_thread_button.grid(row=4, column=0, columnspan=2, sticky='ew')
        self.stop_all_button.grid(row=4, column=2, columnspan=2, sticky='ew')

        self.sleep_thread_button.grid(row=3, column=0, sticky='ew')
        self.sleep_all_button.grid(row=3, column=2, sticky='ew')

        self.wake_thread_button.grid(row=3, column=1, sticky='ew')
        self.wake_all_button.grid(row=3, column=3, sticky='ew')

        # create widgets for bottom frame
        self.info_tree_view = Treeview(self.bottom, columns=('Function', 'Status'))
        self.info_tree_view.heading('#0', text='Thread Name')
        self.info_tree_view.heading('#1', text='Function Name')
        self.info_tree_view.heading('#2', text='Status')
        self.info_tree_view.column('#0', width=100, stretch=NO)
        self.info_tree_view.column('#1', width=75)
        self.info_tree_view.column('#2', width=100, stretch=NO)
        self.output_textbox = Text(self.bottom, background="white", font=("Helvetica", 8))

        self.output_scrollbar = Scrollbar(self.bottom, command=self.output_textbox.yview)
        self.info_scrollbar = Scrollbar(self.bottom, command=self.info_tree_view.yview)

        # layout for the widgets in the bottom frame
        self.info_tree_view.grid(row=0, column=0, sticky='nsew')
        self.info_scrollbar.grid(row=0, column=1, sticky="nse")
        self.info_tree_view.config(yscrollcommand=self.info_scrollbar.set)

        self.output_textbox.grid(row=2, column=0, sticky='nsew')
        self.output_scrollbar.grid(row=2, column=1, sticky="nse")
        self.output_textbox.config(yscrollcommand=self.output_scrollbar.set)

        self.ui_update_thread = SleepableThread(work_wait=0.1)
        self.ui_update_thread.set_thread_work(self.refresh_output)
        self.ui_update_thread.start_thread()

        # Mainloop
        self.ui.mainloop()

    def refresh_tree_view(self):
        self.info_tree_view.delete(*self.info_tree_view.get_children())
        for item in self.manager.threads.items():
            self.info_tree_view.insert('', 'end', text=item[0], values=
            (str(item[1].work_function), item[1].thread_state_mappings[item[1].thread_state]))

    def refresh_thread_dropdown(self):
        menu = self.thread_dropdown.children["menu"]
        menu.delete(0, "end")

        for value in (self.manager.threads.keys()):
            menu.add_command(label=value, command=lambda t=value: self.thread_selected.set(t))

        if self.manager.threads.__len__() > 0:
            self.thread_selected.set(sorted(self.manager.threads.keys())[0])
        else:
            self.thread_selected.set('Select a Thread...')
        self.refresh_tree_view()

    def refresh_output(self): # function passed to ui thread
        if self.manager.functions.MessageQueue.__len__() > 0:
            while self.manager.functions.MessageQueue.__len__() != 0:
                self.output_textbox.insert(END, '{}\n'.format(self.manager.functions.MessageQueue.pop()))
                if self.manager.thread_stats()[1]>0:
                    self.output_textbox.see('end')

    def create_thread(self):
        self.manager.create_thread()
        self.refresh_thread_dropdown()

    def remove_thread(self):
        self.manager.remove_thread(self.thread_selected.get())
        self.refresh_thread_dropdown()

    def remove_all(self):
        self.manager.remove_thread('all')
        self.refresh_thread_dropdown()

    def start_thread(self):
        self.manager.control_thread(self.thread_selected.get(), 'start')
        self.refresh_tree_view()

    def start_all(self):
        self.manager.control_thread('all', 'start')
        self.refresh_tree_view()

    def restart_thread(self):
        self.manager.control_thread(self.thread_selected.get(), 'restart')
        self.refresh_tree_view()

    def restart_all(self):
        self.manager.control_thread('all', 'restart')
        self.refresh_tree_view()

    def sleep_thread(self):
        self.manager.control_thread(self.thread_selected.get(), 'sleep')
        self.refresh_tree_view()

    def sleep_all(self):
        self.manager.control_thread('all', 'sleep')
        self.refresh_tree_view()

    def wake_thread(self):
        self.manager.control_thread(self.thread_selected.get(), 'wake')
        self.refresh_tree_view()

    def wake_all(self):
        self.manager.control_thread('all', 'wake')
        self.refresh_tree_view()

    def stop_thread(self):
        self.manager.control_thread(self.thread_selected.get(), 'stop')
        self.refresh_tree_view()

    def stop_all(self):
        self.manager.control_thread('all', 'stop')
        self.refresh_tree_view()

    def set_thread_function(self):
        self.manager.set_function(self.thread_selected.get(), self.function_selected.get())
        self.refresh_tree_view()

    def set_all_function(self):
        self.manager.set_function('all', self.function_selected.get())
        self.refresh_tree_view()


if __name__ == "__main__":
    ui = SleepableThreadManagerGUI()
