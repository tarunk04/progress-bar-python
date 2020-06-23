"""
Progress Bar For Jupyter Notebook
----------------------------------
Simple and easy to use progress bar.

Auther : Tarun Kumar
"""

import time

class Progress:
    
    #Class Element
    class Elememt:
        def __init__(self, name,initial_value,max_value = None,display_name="normal",value_display_mode=0,separator=":",f=None):
            self.name = name
            self.value = initial_value
            self.value_display_mode = value_display_mode
            self.max_value = max_value
            self.display_name = display_name
            self.separator = separator
            
            if f != None:
                self.floating_point = ":."+str(f)+"f"
            else:
                self.floating_point = ""

        def get_value(self): 
            return selt.values

        def __call__(self,value = None):
            if value != None:
                self.value = value
            return self.value

        def get_element(self):
            element = ""

            if self.value_display_mode == 0:
                element += " {" + self.floating_point + "} "
            if self.value_display_mode == 1:
                if self.max_value == None:
                    print("Error: display_mode '1', max_value for element is required.")
                    return "test"
                element += " {" + self.floating_point + "}/" + str(self.max_value) + " "
            if self.display_name=="normal":
                element = self.name + self.separator + element
            if self.display_name=="reverse":
                element += self.name +" "
            if self.display_name == "hide":
                pass

            return element 
    
    #Class Bar  
    class Bar:
        def __init__(self,max_value=None,bar_len=20, bar_marker="=", bar_pointer=">"):
            self.max_value = max_value
            self.val = 0
            self.bar_len = bar_len
            self.bar_marker = bar_marker
            if len(bar_pointer) == 1:
                self.bar_pointer = bar_pointer
            else:
                self.bar_pointer = " "
        
        def __call__(self,value = None):
            if value != None:
                self.val = value
            return self.update_bar(self.val)
        
        def update_bar(self,val):
            persent = int((val * 100) / self.max_value) 
            bar_unit = 100/self.bar_len
            
            num_marker = int(persent/bar_unit)
            
            bar = self.bar_marker*num_marker+\
                self.bar_pointer+\
                " "*(self.bar_len -num_marker-1)
            return "["+bar[:self.bar_len]+"]"
    
    class ProgressTime:
        def __init__(self, postfix=""):
            self.postfix = postfix
            self.start_time = 0
            
        def __call__(self):
            return self.calculate_elapsed_time()
            
        def initialize(self):
            self.start_time = time.time()
            
        def calculate_elapsed_time(self):
            elapsed_time = time.time() - self.start_time
            if elapsed_time < 1:
                elapsed_time = elapsed_time*1000
                
                if elapsed_time < 1:
                    elapsed_time = (elapsed_time*1000)//1
                    return str(int(elapsed_time))+"um"+self.postfix
                else:
                    return str(int(elapsed_time))+"ms"+self.postfix
            else:
                return str(int(elapsed_time))+"s"+self.postfix  
            
        def get_element(self):
            element = " {} "
            return element

            
    def __init__(self, max_val, desc= "Step", mode = "no-bar"):
        self.bar_mode = (mode == "bar")
        self.bar = None
        self.progress_time = None
        self.desc = desc
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
            self.progress_time.initialize()
    
    def add(self,element):
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
        
        if type(element) == Progress.Bar:
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
            
    def __call__(self,element):
        self.add(element)
        return self
    
    def update(self,step = 1):
        self.val += step
        if self.val > self.max_val:
            self.val = 1
            if self.progress_time != None:
                self.progress_time.initialize()
        self.output()
        
    def output(self):
        bar = ""
        if self.bar_mode:
            bar = "{}"
            self.bar(self.val)
            
        out = self.prefix + bar + self.postfix
        update = "\r"+out.format(*[e() for e in self.elements])
        string_len = len(update)
        if string_len > self.max_string_len:
            self.max_string_len = len(update)
            
        print(update, end=" "*(self.max_string_len-string_len))
    
    def get_format(self): 
        bar = ""
        if self.bar_mode:
            bar = "{bar}"
        return self.prefix + bar + self.postfix
    
    def set_cursor_position(self):
        bar = ""
        if self.bar_mode:
            bar = "{}"
        out = self.prefix + bar + self.postfix

        self.bar(self.val)
        history = out.format(*[ e() for e in self.elements])
        self.history.append(history) 

        print("\r"+history)
        self.max_string_len = 0