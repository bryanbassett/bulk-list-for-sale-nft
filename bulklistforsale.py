import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from turtle import width
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
import os
import io
import sys
import pickle
import time
from decimal import *
import webbrowser
# from click import command
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import timedelta  
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
import locale
import json 
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#check local date format
locale.setlocale(locale.LC_ALL, '')
lastdate = date(date.today().year, 12, 31)
def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = ttk.Style(root)
    style.configure("TRadiobutton", indicatorcolor='#9999',indicatorbackground='#324443')
    root.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')

    
    return style

root = Tk()

root.geometry('750x550')
root.resizable(False, False)
root.title("Bulk List For Sale On OpenSea v1.0.0")
  
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])

def supportURL():
    webbrowser.open_new("https://www.infotrex.net/opensea/support.asp?r=app")

def coffeeURL():
    webbrowser.open_new("https://opensea.io/collection/no-hand-andy")

class WebImage:
    def __init__(self, url):
        image = Image.open(url)
        image = image.resize((748,172))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

img = WebImage(main_directory + r"\bulklistheader.png").get()
imagelab = tk.Label(root, image=img)
imagelab.grid(row=0, column=0,columnspan=4)
#grid(row=10, column=0, padx=12, pady=2)
imagelab.bind("<Button-1>", lambda e:supportURL())


is_listing = BooleanVar()
is_listing.set(True) 

is_numformat = BooleanVar()
is_numformat.set(False) 


def save_duration():
    duration_value.set(value=duration_value.get())
    #print(duration_value.get())

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=9515",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )


def save_file_path():
    return os.path.join(sys.path[0], "Save_gui.cloud") 



def is_numeric(val):
	if str(val).isdigit():
		return True
	elif str(val).replace('.','',1).isdigit():
		return True
	else:
		return False


class InputField:
    def __init__(self, label, row_io, column_io, pos,  master=root):
        self.master = master
        self.input_field = Entry(self.master, width=60)
        self.input_field.grid(ipady=3)
        self.input_field.label = Label(master, text=label, anchor="w", width=20, height=1 )
        self.input_field.label.grid(row=row_io, column=column_io, padx=12, pady=2)
        self.input_field.grid(row=row_io, column=column_io + 1, padx=12, pady=2)
        
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass
        
    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        #messagebox.showwarning("showwarning", "Warning")
        input_save_list.insert(pos, self.input_field.get())
        #print(self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)
            
    def validate_inputs(self, maxlen, type, message):

        if type == 0 and (len(self.input_field.get()) == 0 or (self.input_field.get()).isdigit() != True or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)
                
        elif type == 1 and (len(self.input_field.get()) == 0 or is_numeric(self.input_field.get()) == False or len(self.input_field.get()) >= maxlen):
            messagebox.showwarning("showwarning", message)       
                
        elif type == 2 and ( len(self.input_field.get()) == 0 or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)
               
        else:
            return True     
        

###input objects###
collection_link_input = InputField("OpenSea Collection Root:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Price:", 5, 0, 4)


def save():

    if len(start_num_input.input_field.get()) == 0 or len(end_num_input.input_field.get()) == 0 or (int(end_num_input.input_field.get()) < int(start_num_input.input_field.get())):
        #messagebox.showwarning("showwarning", "End number should greater than start number!")
        print ("true")
    elif len( start_num_input.input_field.get()) == 0 or len(end_num_input.input_field.get()) > 5 :
        #messagebox.showwarning("showwarning", "Start / end number range 0 - 99999")
        print ("true")
    else:
        collection_link_input.validate_inputs(200, 2, 'Collection root URL required')
        price.validate_inputs(100, 1, 'Price required')
     

    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    

    

def main_program_loop():

    if len(end_num_input.input_field.get()) > 5 :
        messagebox.showwarning("showwarning", "Start / end number range 0 - 99999")
        sys.exit()

    project_path = main_directory
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_price = float(price.input_field.get())

    ##chromeoptions
    opt = Options()
    opt.add_argument('--headless')
    opt.add_experimental_option("debuggerAddress", "localhost:9515")
    driver = webdriver.Chrome(
         executable_path=project_path + "/chromedriver.exe",
         chrome_options=opt,
    )
    # driver = webdriver.Chrome( service=Service(project_path + "/chromedriver.exe"), options=opt, )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
    def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )    

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))


    while end_num >= start_num:
        if is_numformat.get():
            start_numformat = f"{ start_num:04}"
        else:
             start_numformat = f"{ start_num:01}"

        print("Listing NFT For Sale: " +  str(start_numformat))
        driver.get(collection_link + "/" + str(start_num))
        main_page = driver.current_window_handle

        if is_listing.get():
            try:
                time.sleep(1)
           
                sell = driver.find_element(By.XPATH, '//a[text()="Sell"]')
                driver.execute_script("arguments[0].click();", sell)
                
                wait_css_selector("input[placeholder='Amount']")
                amount = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Amount']")
                amount.send_keys(str(loop_price))
                time.sleep(1)

                #duration
                duration_date = duration_value.get()
                #print(duration_date)
                # time.sleep(60)
                if duration_date == 1 : 
                    endday = (date.today() + timedelta(days=1)).day
                    endmonth = (date.today() + timedelta(days=1)).month
                    #print(endday, endmonth)
                if duration_date == 3 : 
                    endday = (date.today() + timedelta(days=3)).day
                    endmonth = (date.today() + timedelta(days=3)).month
                    #print(endday, endmonth)
                if duration_date == 7 : 
                    endday = (date.today() + timedelta(days=7)).day
                    endmonth = (date.today() + timedelta(days=7)).month   
                    #print(endday, endmonth)       
                if duration_date == 30:
                    endday = (date.today() + relativedelta(months=+1)).day
                    endmonth = (date.today() + relativedelta(months=+1)).month
                    #print(endday, endmonth)
                if duration_date == 60:
                    endday = (date.today() + relativedelta(months=+2)).day
                    endmonth = (date.today() + relativedelta(months=+2)).month
                    #print(endday, endmonth)
                if duration_date == 90:
                    endday = (date.today() + relativedelta(months=+3)).day
                    endmonth = (date.today() + relativedelta(months=+3)).month
                    #print(endday, endmonth)
                if duration_date == 120:
                    endday = (date.today() + relativedelta(months=+4)).day
                    endmonth = (date.today() + relativedelta(months=+4)).month  
                    #print(endday, endmonth) 
                if duration_date == 150:
                    endday = (date.today() + relativedelta(months=+5)).day
                    endmonth = (date.today() + relativedelta(months=+5)).month  
                    #print(endday, endmonth)  
                if duration_date == 180:
                    endday = (date.today() + relativedelta(months=+6)).day
                    endmonth = (date.today() + relativedelta(months=+6)).month   
                    #print(endday, endmonth)

                amount.send_keys(Keys.TAB)
                time.sleep(0.8)
                
                wait_xpath('//*[@role="dialog"]/div[2]/div[2]/div/div[2]/input')
                select_durationday = driver.find_element(By.XPATH, '//*[@role="dialog"]/div[2]/div[2]/div/div[2]/input')
                driver.execute_script("arguments[0].click();", select_durationday)
                time.sleep(0.8)
                
                if lastdate.strftime('%x')[:2] == "12":
                    select_durationday.send_keys(str(endmonth))
                    select_durationday.send_keys(str(endday))
                    select_durationday.send_keys(Keys.ENTER)
                    time.sleep(1)
                elif lastdate.strftime('%x')[:2] == "31":
                    select_durationday.send_keys(str(endday))
                    select_durationday.send_keys(str(endmonth))
                    select_durationday.send_keys(Keys.ENTER)
                    time.sleep(1)
                else:
                    print("invalid date format: change date format to MM/DD/YYYY or DD/MM/YYYY")

                wait_css_selector("button[type='submit']")
                listing = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                driver.execute_script("arguments[0].click();", listing)
                time.sleep(5)
                print('looking for sign button')
                wait_xpath('//button[text()="Sign"]')
                print('found sign button')
                metasign = driver.find_element(By.XPATH, '//button[text()="Sign"]')
                driver.execute_script("arguments[0].click();", metasign)
                time.sleep(0.7)

                for handle in driver.window_handles:
                    if handle != main_page:
                        login_page = handle
                        #break
                
                driver.switch_to.window(login_page) 
      
                wait_css_selector("button[data-testid='request-signature__sign']")
                sign = driver.find_element(By.CSS_SELECTOR, "button[data-testid='request-signature__sign']")
                driver.execute_script("arguments[0].click();", sign)
                time.sleep(1)
            
    
                #change control to main page
                driver.switch_to.window(main_page)
                time.sleep(0.7)
                print('NFT ' + str(start_num) +  ' listed for sale!')
                start_num = start_num + 1
               
            except Exception as e:
                # work on python 3.x
                start_num = start_num + 1
                print('NFT  ' + str(start_num) +  ' skipped! (either you didnt own it, it was already listed, or something else went wrong.')
    


duration_value = IntVar()
duration_value.set(value=180)

myColor = '#40E0D0'                 # Its a light blue color
                                     # Setting color of main window to myColor
style = darkstyle(root)
                                    # Creating style element
style.configure('Wild.TRadiobutton',    # First argument is the name of style. Needs to end with: .TRadiobutton
        background='white',
        indicatorcolor='green',
        indicatorbackground='red',         # Setting background to our specified color above
        foreground='black',
        )      

duration_date = Frame(root, padx=0, pady=1)
duration_date.grid(row=5, column=1, sticky=(N, W, E, S))
ttk.Radiobutton(duration_date, text='1 day', variable=duration_value, value=1,  command=save_duration, width=8,).grid(row=0, column=1)
ttk.Radiobutton(duration_date, text="3 days", variable=duration_value, value=3, command=save_duration, width=8, ).grid(row=0, column=2)
ttk.Radiobutton(duration_date, text="7 days", variable=duration_value, value=7,  command=save_duration, width=8,).grid(row=0, column=3)
ttk.Radiobutton(duration_date, text="30 days", variable=duration_value, value=30,  command=save_duration, width=8,).grid(row=0, column=4)
ttk.Radiobutton(duration_date, text="60 days", variable=duration_value, value=60, command=save_duration, width=8,).grid(row=0,  column=5)
ttk.Radiobutton(duration_date, text="90 days", variable=duration_value, value=90, command=save_duration,  width=8,).grid(row=1, columnspan=1, column=1)
ttk.Radiobutton(duration_date, text="120 days", variable=duration_value, value=120, command=save_duration, width=8,).grid(row=1, columnspan=1, column=2)
ttk.Radiobutton(duration_date, text="150 days", variable=duration_value, value=150, command=save_duration, width=8,).grid(row=1, columnspan=1, column=3)
ttk.Radiobutton(duration_date, text="180 days", variable=duration_value, value=180,  command=save_duration, width=8,).grid(row=1, columnspan=1, column=4)
duration_date.label = Label(root, text="Duration:", anchor="w", width=20, height=1 )
duration_date.label.grid(row=5, column=0, padx=12, pady=2)



button_save = ttk.Button(root, width=50,   text="Save This Form", command=save) 
button_save.grid(row=6, column=1, pady=2)
open_browser = ttk.Button(root, width=50,   text="Open Chrome Browser (close any other chrome browser first)", command=open_chrome_profile)
open_browser.grid(row=7, column=1, pady=2)
button_start = ttk.Button(root, width=50, text="Start", command=main_program_loop, style="Accentbutton")

button_start.grid(row=8, column=1, pady=2)
footer = ttk.Button(root,  width=60, text='Do you you want to show support? \n Buy one of my NFTs. Thanks.',  command=coffeeURL, style="Togglebutton" )
footer.grid(row=9, columnspan=2, padx=31, pady=31)

#####BUTTON ZONE END#######
root.mainloop()
