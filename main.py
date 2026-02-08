from tkinter import *
from tkinter import messagebox
import threading
import time
import subprocess 

root = Tk()
root.title('turn_off_pc (Beta Version)')
root.geometry('750x530')
root.resizable(width=False, height=False) 

timer_active = False
timer_thread = None
correct_login = "a"
correct_login_2 = "b" 
sleep_time_hours = 1
message_shown = False

popup_opend = False 
warning_shown = False

def on_closing():
    global popup_opend 
    if popup_opend:
        return 
    popup_opend = True

    asking_window = Toplevel()
    asking_window.title('Confirmation')
    asking_window.geometry("500x230")
    asking_window.resizable(width=False, height=False)

    loginConfirm = Label(asking_window, text='Enter your login', font=('Arial', 16)) 
    loginConfirm.place(relx=0.5, rely=0.2, anchor=CENTER)

    login_confirmInput = Entry(asking_window, width= 25)
    login_confirmInput.place(relx=0.5, rely=0.42, anchor=CENTER) 
 
    asking_window.transient(root)
    asking_window.grab_set() 

    def submited_confirmation(): 
        global warning_shown
        login_confirm = login_confirmInput.get().strip().lower()

        if not login_confirm:
            messagebox.showwarning(title='Error', message='Enter your login')
            return
        if login_confirm == correct_login_2:
            root.destroy()
        else:
            messagebox.showwarning(title='Error', message='The login is wrong')
            login_confirmInput.delete(0, END) 
                
    button_confirm = Button(asking_window, text='Submit', width=10, command=submited_confirmation)  
    button_confirm.place(relx=0.5, rely=0.6, anchor=CENTER) 

    login_confirmInput.bind("<Return>", lambda event: submited_confirmation()) 

    def close_popup():
        global popup_opend
        popup_opend = False
        asking_window.destroy() 
    
    asking_window.protocol("WM_DELETE_WINDOW", close_popup) 

root.protocol("WM_DELETE_WINDOW", on_closing) 

frame1 = Frame(root, bg='#8c8c8c')
frame1.place(relheight=0.4, relwidth=1)

frame2 = Frame(root, bg='#bfbfbf')
frame2.place(relheight=0.6, relwidth=1, rely=0.4)

title = Label(frame1, text='Hello! Who are you?', bg='#8c8c8c', font=('Arial', 24, 'bold'))
title.place(relx=0.5, rely=0.31, anchor=CENTER)

entrer_log = Label(frame2, text='Login', bg='#bfbfbf', font=('Arial', 16)) 
entrer_log.place(relx=0.5, rely=0.2, anchor=CENTER) 

loginInput = Entry(frame2, bg='white', width=50)
loginInput.place(relx=0.5, rely=0.3, anchor=CENTER)

def submit_login():
    global message_shown
    if message_shown:
        return
    login = loginInput.get().strip().lower() 

    if not login:
        messagebox.showwarning(title='Error', message='Enter your login') 
        return
    elif login == correct_login: 
        message_shown = True 
        start_timer()   
    else:
        messagebox.showwarning(title='Error', message='The login is wrong')
        loginInput.delete(0, END) 

button = Button(frame2, text='Submit', bg='purple', width=35, command=submit_login) 
button.place(relx=0.5, rely=0.4, anchor=CENTER) 

loginInput.bind("<Return>", lambda event: submit_login())  

def start_timer():
    global timer_active, timer_thread

    #if timer_active:
    #    messagebox.showinfo(title='Information', text='Timer is already running')
    #    return

    button.place_forget()
    loginInput.place_forget()
    entrer_log.config(text=f'Start time: {sleep_time_hours} hours')
    #entrer_log.place_forget() 
    title.config(text="The timer is running", fg='purple')   

    global countdown_label
    countdown_label = Label(frame2, text='', bg="#bfbfbf", font=('Arial', 14)) 
    countdown_label.place(relx=0.5, rely=0.41, anchor=CENTER)  

    timer_active = True 
    timer_thread = threading.Thread(target=timer_function)
    timer_thread.daemon = True
    timer_thread.start()
    update_countdown(sleep_time_hours * 3600)  

def update_countdown(seconds_left):
    if not timer_active:
        return
    
    hours = int(seconds_left // 3600)
    minutes = int((seconds_left % 3600) // 60)
    seconds = int(seconds_left % 60) 

    if seconds_left > 0:
        countdown_label.config(text=f'{hours:02}:{minutes:02}:{seconds:02}') 
        root.after(1000, update_countdown, seconds_left - 1) 
    else:
        #timer_active = False     
        put_to_sleep() 

def timer_function():
    time.sleep(sleep_time_hours * 3600)

    if timer_active:
        root.after(0, put_to_sleep())

def put_to_sleep():
#    messagebox.showinfo(title='Info', text='The PC is going to sleep') 
    try:
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], shell=True, check=True) 
    except Exception as e:
        messagebox.showerror(title='Error', text=f'Could not put it to sleep: {e}') 
    finally:
        root.quit()  


root.mainloop()  