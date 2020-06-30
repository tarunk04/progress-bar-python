"""
Progress Bar For Jupyter Notebook
----------------------------------
Simple and easy to use progress bar.

Author : Tarun Kumar
"""

import time


class Progress:
    """
    Element Examples:
        "Epochs: 1"
        "Epochs: 1/10"
        "1 Epochs"

    Parameters:
        max_val (int): maximum value for progress.
        mode (str):  Default "no-bar". Take value 'bar' and 'no-bar'. Select the the mode for progress.
    """


    class Elememt:
        """
        Element Examples:
            "Epochs: 1"
            "Epochs: 1/10"
            "1 Epochs"

        Parameters:
            name (str): name for displaying in progress for the element
            initial_value (float): initial value for the element
            max_value (int): maximum value that element can take. Note only required in display_mode =1.
            display_name (str): value can take form ["normal","reverse","hide"]. In "reverse" mode name will displayed
                        after value. "hide" will hide the name from progress
            value_display_mode (int): [0,1].default 0. Format "Epoch: 1". For 1 format "Epoch 1/10".
            separator (char): default ":". can be changed according to preference
        """

        def __init__(self, name, initial_value, max_value=None, display_name="normal", value_display_mode=0,
                     separator=":", f=None):

            # progress properties
            self.name = name
            self.value = initial_value
            self.initial_value = initial_value
            self.value_display_mode = value_display_mode
            self.max_value = max_value
            self.display_name = display_name
            self.separator = separator

            if f != None:
                self.floating_point = ":." + str(f) + "f"
            else:
                self.floating_point = ""

        def get_value(self):
            """ Return the current value of the element """

            return selt.values

        def __call__(self, value=None):
            """ Update the vlaue of element"""

            if value != None:
                self.value = value
            return self.value

        def get_element(self):
            """ Return element structure"""

            element = ""

            if self.value_display_mode == 0:
                element += " {" + self.floating_point + "} "
            if self.value_display_mode == 1:
                if self.max_value == None:
                    print("Error: display_mode '1', max_value for element is required.")
                    return "test"
                element += " {" + self.floating_point + "}/" + str(self.max_value) + " "
            if self.display_name == "normal":
                element = self.name + self.separator + element
            if self.display_name == "reverse":
                element += self.name + " "
            if self.display_name == "hide":
                pass

            return element

        def reset(self):
            """ Initialize element value """
            self.value = self.initial_value

    # Class Bar
    class Bar:
        """
        Element Examples:
            [======>     ]
            [------->          ]

        Parameters:
            max_value (int): not required. it will be automatically taken from Progress object.
            bar_len (int):  default 20. length for the bar. [==========>    ].
            bar_marker (char): default "=" can be changed according to preference.
            bar_marker (char): default ">" can be changed according to preference.
        """

        def __init__(self, max_value=None, bar_len=25, fill="=", pointer=">"):
            # Bar properties
            self.val = 0
            self.max_value = max_value
            self.bar_len = bar_len

            # style properties
            self.fill = fill
            self.empty_fill = ' '
            self.prefix = '['
            self.postfix = ']'
            if len(pointer) == 1:
                self.pointer = pointer
            else:
                self.pointer = ""

        def __call__(self, value=None):
            """ Return updated bar """
            if value != None:
                self.val = value
            return self.update_bar(self.val)

        def update_bar(self, val):
            """ Update Bar """
            persent = int((val * 100) / self.max_value)
            bar_unit = 100 / self.bar_len

            num_fill = int(persent / bar_unit)

            bar = self.fill * num_fill + \
                  self.pointer + \
                  self.empty_fill * (self.bar_len - num_fill - len(self.pointer))
            return self.prefix + bar[:self.bar_len] + self.postfix

        def reset(self):
            pass

    # Fill Bar class
    class FillBar(Bar):
        """
        Bar style Fill
        Example:
            ●●●●●●●○○○○○○○
            ■■■■■■□□□□□□□□
            █████○○○○○○○○○

        Parameters:
            mode (char, str, int): Default: "normal", Mode can be 'circle' 'c' or 0, 'square' 's' or 1 and 'normal'
                                    'n' or 2.
            max_value (int): not required. it will be automatically taken from Progress object.
            bar_len (int):  default 20. length for the bar. [==========>    ].
        """

        def __init__(self, mode=None, max_value=None, bar_len=25):
            super().__init__(max_value=max_value, bar_len=bar_len, pointer="")
            # Style properties
            self.prefix = ''
            self.postfix = ''

            if mode == "c" or mode == "circle" or mode == 0:
                self.empty_fill = '○'
                self.fill = '●'
            if mode == "s" or mode == "square" or mode == 1:
                self.empty_fill = '□'
                self.fill = '■'
            if mode == None or mode == 'n' or mode == "normal" or mode == 2:
                self.empty_fill = '○'
                self.fill = '█'
                self.prefix = '|'
                self.postfix = '|'

    class ProgressTime:
        """
        Element Examples:
            "100ms"
            "112s/epochs"

        Parameters:
            postfix (str): string after time
        """
        def __init__(self, postfix=""):
            self.postfix = postfix
            self.start_time = 0

        def __call__(self):
            """ Return update ProgressTime Element"""
            return self.calculate_elapsed_time()

        def calculate_elapsed_time(self):
            """ Calculate and  return elapsed time with unit in 's' 'ms' and 'us' """

            elapsed_time = time.time() - self.start_time
            if elapsed_time < 1:
                elapsed_time = elapsed_time * 1000

                if elapsed_time < 1:
                    elapsed_time = (elapsed_time * 1000) // 1
                    return str(int(elapsed_time)) + "us" + self.postfix
                else:
                    return str(int(elapsed_time)) + "ms" + self.postfix
            else:
                return str(int(elapsed_time)) + "s" + self.postfix

        def get_element(self):
            """ Return element structure"""

            element = " {} "
            return element

        def reset(self):
            """ Initialize element value """
            self.start_time = time.time()

    def __init__(self, max_val, mode="no-bar"):
        self.bar_mode = (mode == "bar")
        self.bar = None
        self.progress_time = None
        self.max_val = max_val
        self.val = 0
        self.add_postfix = False
        self.prefix = ""
        self.postfix = ""
        self.elements = []
        self.history = []
        self.max_string_len = 0

    def initialize(self):
        self.val = 0
        self.history = []
        self.max_string_len = 0
        if self.progress_time != None:
            self.progress_time.reset()

    def add(self, element):
        """ Add new elements to the Progress. Element can be Object of Element, Bar, FillBar, ProgressTime """

        if element == None:
            print("Error: Nothing to add. Pass any [element,bar] to add.")
            return

        if type(element) == str:
            if self.add_postfix == True:
                self.postfix += element
            else:
                self.prefix += element
            return

        if type(element) == Progress.ProgressTime:
            self.progress_time = element
            if self.add_postfix == True:
                self.postfix += element.get_element()
            else:
                self.prefix += element.get_element()
            self.elements.append(element)
            return

        if type(element) == Progress.Bar or type(element) == Progress.FillBar:
            self.add_postfix = True
            element.max_value = self.max_val
            self.bar = element
            self.elements.append(element)
            return

        if type(element) != Progress.Elememt:
            print("Error: Invalid input type. Required type Progress.Elememt found {}".format(type(element)))
            return

        if self.add_postfix == True:
            self.postfix += element.get_element()
        else:
            self.prefix += element.get_element()
        self.elements.append(element)

        return

    def __call__(self, element):
        """ Callable function to add new elements. Easy way to compile or add elements. """

        self.add(element)
        return self

    def update(self, step=1):
        """ Update progress """

        self.val += step
        if self.val > self.max_val:
            self.val = 1
        self.output()

    def output(self):
        """ Render the updated progress """

        bar = ""
        if self.bar_mode:
            bar = "{}"
            self.bar(self.val)

        out = self.prefix + bar + self.postfix
        update = "\r" + out.format(*[e() for e in self.elements])
        string_len = len(update)
        if string_len > self.max_string_len:
            self.max_string_len = len(update)

        print(update, end=" " * (self.max_string_len - string_len))

    def get_format(self):
        """ Return the final structure of the progress after all element has compiled """
        bar = ""
        if self.bar_mode:
            bar = "{bar}"
        return self.prefix + bar + self.postfix

    def set_cursor_position(self):
        """ Change the cursor to the new line """

        bar = ""
        if self.bar_mode:
            bar = "{}"
            self.bar(self.val)

        # saving history of progress
        out = self.prefix + bar + self.postfix
        history = out.format(*[e() for e in self.elements])
        self.history.append(history)

        # reset progress bar
        for e in self.elements:
            e.reset()

        # line Change
        print()
        self.max_string_len = 0
