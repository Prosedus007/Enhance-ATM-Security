from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import face_recognition
import os
import base64
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from imutils.video import VideoStream
from imutils.video import FPS
import time
from tkinter import *
from tkinter import messagebox
import sqlite3
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
from sendgrid.helpers.mail import FileContent, FileName, FileType, Disposition



load_dotenv()

# Access environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

conn = sqlite3.connect('Bank.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                unique_id INTEGER PRIMARY KEY, 
                account_number INTEGER(10) UNIQUE,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                number TEXT UNIQUE,
                bank TEXT NOT NULL,
                password TEXT NOT NULL,
                account_balance REAL DEFAULT 10000)''')
                                                    
# cursor.execute("DROP TABLE users")

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

ARIAL = ("arial",25,"bold")

class BankUi:
    def __init__(self,root):
        self.root = root
        self.header = Label(self.root,text="SBI BANK",bg="#8bdbc4",fg="white",font=("arial",50,"bold"))
        self.header.pack(fill=X,pady=50,anchor="center")
        self.frame = Frame(self.root,bg="#8bdbc4",width=1100,height=700)
        root.geometry("1100x700")
        self.button1 = Button(self.frame,text="Click to begin transactions",bg="#50A8B0",fg="white",font=ARIAL,command = self.begin_page)
        self.q = Button(self.frame, text="Quit", bg="#50A8B0", fg="white", font=ARIAL, command=self.root.destroy)
        self.q.place(x=350, y=200, width=400, height=70)
        self.button1.place(x=270,y=50,width=560,height=70)
        self.countter = 2
        self.frame.pack()
   
    def begin_page(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        root.geometry("1100x700")
        self.enroll = Button(self.frame, text="Enroll",bg="#50A8B0",fg="white",font=ARIAL,command=self.enroll_user)
        self.withdraw = Button(self.frame, text="Withdraw Money",bg="#50A8B0",fg="white",font=ARIAL,command=self.withdraw_money_page)
        self.q = Button(self.frame, text="Quit", bg="#50A8B0", fg="white", font=ARIAL, command=self.root.destroy)
        self.enroll.place(x=0, y=60, width=400, height=70)
        self.withdraw.place(x=500, y=60, width=400, height=70)
        self.q.place(x=390, y=250, width=120, height=50)
        self.frame.pack()


    def withdraw_money_page(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=1000,height=500)
        self.maillable = Label(self.frame, text="Email",bg="#8bdbc4",fg="white",font=ARIAL)
        self.mail = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.paslable = Label(self.frame, text="Password",bg="#8bdbc4",fg="white",font=ARIAL)
        self.pas = Entry(self.frame,bg="honeydew",show="*",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.maillable.place(x=150,y=20,width=120,height=50)
        self.mail.place(x=150,y=90,width=250,height=50)
        self.paslable.place(x=500,y=20,width=200,height=50)
        self.pas.place(x=500,y=90,width=250,height=50)

        self.verify1 = Button(self.frame,text="Verify",bg="#50A8B0",fg="white",font=ARIAL,command = self.verify_user)
        self.verify1.place(x=280,y=230,width=150,height=50)

        self.q = Button(self.frame,text="Quit",bg="#50A8B0",fg="white",font=ARIAL,command = self.root.destroy)
        self.b = Button(self.frame,text="Back",bg="#50A8B0",fg="white",font=ARIAL,command = self.begin_page)
        self.q.place(x=480,y=360,width=120,height=50)
        self.b.place(x=280,y=360,width=120,height=50)
        self.frame.pack()



    def enroll_user(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        #Login Page Form Components
        self.userlabel =Label(self.frame,text="Full Name",bg="#8bdbc4",fg="white",font=ARIAL)
        self.uentry = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.plabel = Label(self.frame, text="Password",bg="#8bdbc4",fg="white",font=ARIAL)
        self.pentry = Entry(self.frame,bg="honeydew",show="*",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.nlable =Label(self.frame,text="Number",bg="#8bdbc4",fg="white",font=ARIAL)
        self.Num = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.mlable = Label(self.frame, text="Email",bg="#8bdbc4",fg="white",font=ARIAL)
        self.mail = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        
        self.nlable.place(x=500,y=0,width=250,height=50)
        self.Num.place(x=500,y=60,width=350,height=50)
        self.mlable.place(x=500,y=120,width=250,height=50)
        self.mail.place(x=500,y=180,width=350,height=50) 
    
        self.button1 = Button(self.frame,text="Next",bg="#50A8B0",fg="white",font=ARIAL,command = self.enroll_and_move_to_next_screen)
        #self.button2 = Button(self.frame,text="Click to go to video capture after enrolling",bg="#50A8B0",fg="white",font=ARIAL, command = self.video_page)
        self.q = Button(self.frame,text="Quit",bg="#50A8B0",fg="white",font=ARIAL,command = self.root.destroy)
        self.b = Button(self.frame,text="Back",bg="#50A8B0",fg="white",font=ARIAL,command = self.begin_page)
        self.userlabel.place(x=50,y=0,width=250,height=50)
        self.uentry.place(x=50,y=60,width=350,height=50)
        self.plabel.place(x=50,y=120,width=250,height=50)
        self.pentry.place(x=50,y=180,width=350,height=50)
        self.button1.place(x=50,y=260,width=250,height=50)
        #self.button2.place(x=355,y=230,width=350,height=30)
        self.q.place(x=480,y=360,width=120,height=70)
        self.b.place(x=280,y=360,width=120,height=70)
        self.frame.pack()
        
    
    def enroll_and_move_to_next_screen(self):
        n = 5;range_start = 10**(n-1);range_end = (10**n)-1
        unique_id = randint(range_start, range_end)
        name = self.uentry.get()
        password = self.pentry.get()
        email = self.mail.get()
        number = self.Num.get()
        if not name and not password:
            messagebox._show("Error", "You need a name to enroll an account and you need to input a password!")
            self.enroll_user()
        elif not password:
            messagebox._show("Error", "You need to input a password!")
            self.enroll_user()
        elif not email:
            messagebox._show("Error", "You need to input a Email!")
            self.enroll_user()
        elif not number:
            messagebox._show("Error", "You need to input a Number!")
            self.enroll_user()
        elif len(number) != 10:
            messagebox._show("Number Error", "Your number needs to be 10 digits!")
            self.enroll_user()
        elif not name:
            messagebox._show("Error", "You need a name to enroll an account!")
            self.enroll_user()
        elif len(password) < 8:
            messagebox._show("Password Error", "Your password needs to be at least 8 digits!")
            self.enroll_user()
        else:
            self.Write_to_sql(unique_id)


    def verify_user(self):
        emailver = self.mail.get()
        passwordver = self.pas.get()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (emailver, passwordver))
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            messagebox.showinfo("Verify face Before Login")
            self.video_check(emailver)
        else:
            # Handle case where email and password don't match
            messagebox.showerror("Error", "Invalid email or password")
                
   
    def final_page(self,emailver):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        self.detail = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_account_transfer(emailver))
        self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_balance(emailver))
        self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_deposit_money(emailver))
        self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_withdrawl_money(emailver))
        self.q = Button(self.frame, text="Log out", bg="#50A8B0", fg="white", font=ARIAL, command=self.begin_page)
        self.detail.place(x=0,y=0,width=350,height=70)
        self.enquiry.place(x=0, y=250, width=350, height=70)
        self.deposit.place(x=500, y=0, width=400, height=70)
        self.withdrawl.place(x=500, y=250, width=400, height=70)
        self.q.place(x=355, y=350, width=200, height=70)
        self.frame.pack()

    
    def user_account_transfer(self,emailver):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        self.detail = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_account_transfer(emailver))
        self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_balance(emailver))
        self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_deposit_money(emailver))
        self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_withdrawl_money(emailver))
        self.q = Button(self.frame, text="Log out", bg="#50A8B0", fg="white", font=ARIAL, command=self.begin_page)
        self.detail.place(x=0,y=0,width=340,height=50)
        self.enquiry.place(x=0, y=315, width=340, height=50)
        self.deposit.place(x=550, y=0, width=340, height=50)
        self.withdrawl.place(x=550, y=315, width=340, height=50)

        self.q.place(x=370, y=370, width=150, height=50)
        self.frame.pack()
        self.label11 = Label(self.frame, text="Reciepient's account number",bg="#8bdbc4",fg="white",font=ARIAL) 
        self.label21 = Label(self.frame, text="Amount to be transferred",bg="#8bdbc4",fg="white",font=ARIAL) 
        self.button1 = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda:self.user_account_transfer_transc(emailver))
        self.Acc_Num = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.Amount1 = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20)) 
        self.label11.place(x=200,y=60,width=550,height=40)
        self.Acc_Num.place(x=200,y=110,width=300,height=40)
        self.label21.place(x=200,y=160,width=480,height=40)
        self.Amount1.place(x=200,y=210,width=300,height=40)
        self.button1.place(x=300,y=260,width=180,height=40)
        

    def user_account_transfer_transc(self,emailver):
        acc_number = self.Acc_Num.get()
        amount = self.Amount1.get()

        cursor.execute("SELECT account_number FROM users WHERE account_number = ?", (acc_number,))
        res = cursor.fetchone()

        cursor.execute("SELECT account_number FROM users WHERE email = ?", (emailver,))
        res1 = cursor.fetchone()

        cursor.execute("SELECT account_balance FROM users WHERE email = ?", (emailver,))
        res3 = cursor.fetchone()
        if not res:
            messagebox.showinfo("Transfer Info!", "Invalid account number")
        elif res1 and int(res1[0]) == int(acc_number):
            messagebox.showinfo("Transfer Info!", "Sorry, you cannot make a transfer to yourself")
        elif res3 and float(res3[0]) < float(amount):
            messagebox.showinfo("Transfer Info!", "Insufficient Funds") 
        else:
            cursor.execute("UPDATE users SET account_balance = account_balance + ? WHERE account_number = ?", (amount, acc_number))
            conn.commit() 
            cursor.execute("UPDATE users SET account_balance = account_balance - ? WHERE email = ?", (amount, emailver))
            conn.commit()
            messagebox.showinfo("Successfully Transfer")
            self.user_account_transfer(emailver)

    def user_balance(self,emailver):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        self.detail = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_account_transfer(emailver))
        self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_balance(emailver))
        self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_deposit_money(emailver))
        self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_withdrawl_money(emailver))
        self.q = Button(self.frame, text="Log out", bg="#50A8B0", fg="white", font=ARIAL, command=self.begin_page)
        self.detail.place(x=0,y=0,width=340,height=50)
        self.enquiry.place(x=0, y=315, width=340, height=50)
        self.deposit.place(x=550, y=0, width=340, height=50)
        self.withdrawl.place(x=550, y=315, width=340, height=50)
        self.q.place(x=370, y=370, width=150, height=50)
        self.frame.pack()
        cursor.execute("SELECT account_balance FROM users WHERE email = ?", (emailver,))
        result = cursor.fetchone()
        text = result[0]

        self.label = Label(self.frame, text= 'Current Account Balance: ' + ' ' + str(text),font=("arial",25),fg="white",bg="#8bdbc4")
        self.label.place(x=200, y=100, width=500, height=100)

    def user_deposit_money(self,emailver):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        self.detail = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_account_transfer(emailver))
        self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_balance(emailver))
        self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_deposit_money(emailver))
        self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_withdrawl_money(emailver))
        self.q = Button(self.frame, text="Log out", bg="#50A8B0", fg="white", font=ARIAL, command=self.begin_page)
        self.detail.place(x=0,y=0,width=340,height=50)
        self.enquiry.place(x=0, y=315, width=340, height=50)
        self.deposit.place(x=550, y=0, width=340, height=50)
        self.withdrawl.place(x=550, y=315, width=340, height=50)
        self.q.place(x=370, y=370, width=150, height=50)
        self.frame.pack()
        self.label = Label(self.frame, text="Enter amount", font=ARIAL,fg="white",bg="#8bdbc4")
        self.label.place(x=200, y=80, width=230, height=100)
        self.money_box = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.submitButton = Button(self.frame,text="Deposit",bg="#50A8B0",fg="white",font=ARIAL)

        self.money_box.place(x=200,y=150,width=200,height=40)
        self.submitButton.place(x=445,y=150,width=200,height=40)
        self.submitButton.bind("<Button-1>", lambda event: self.user_deposit_trans(emailver))

    def user_deposit_trans(self,emailver):
        amount_to_transfer = self.money_box.get()
        cursor.execute("UPDATE users SET account_balance = account_balance + ? WHERE email = ?", (amount_to_transfer, emailver))
        conn.commit() 
        if cursor.rowcount > 0:
            messagebox.showinfo("Deposit Info!", "Successfully Deposited!")
        else:
            messagebox.showerror("Error!", "Failed to deposit amount. Please try again.")
        self.user_deposit_money(emailver)

    def user_withdrawl_money(self,emailver):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        self.detail = Button(self.frame,text="Transfer",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_account_transfer(emailver))
        self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_balance(emailver))
        self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_deposit_money(emailver))
        self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=lambda: self.user_withdrawl_money(emailver))
        self.q = Button(self.frame, text="Log out", bg="#50A8B0", fg="white", font=ARIAL, command=self.begin_page)
        self.detail.place(x=0,y=0,width=340,height=50)
        self.enquiry.place(x=0, y=315, width=340, height=50)
        self.deposit.place(x=550, y=0, width=340, height=50)
        self.withdrawl.place(x=550, y=315, width=340, height=50)
        self.q.place(x=370, y=370, width=150, height=50)
        self.frame.pack()
        self.label = Label(self.frame, text="Enter amount", font=ARIAL,fg="white",bg="#8bdbc4")
        self.label.place(x=200, y=100, width=230, height=40)
        self.money_box = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
           highlightthickness=2,
            highlightbackground="white",font=("Arial", 20))
        self.submitButton = Button(self.frame,text="Withdraw",bg="#50A8B0",fg="white",font=ARIAL)

        self.money_box.place(x=200,y=150,width=200,height=40)
        self.submitButton.place(x=435,y=150,width=200,height=40)
        self.submitButton.bind("<Button-1>",lambda event: self.user_withdrawl_trans(emailver))

    def user_withdrawl_trans(self,emailver):
        amount_to_withdrawl = self.money_box.get()
        cursor.execute("SELECT account_balance FROM users WHERE email = ?", (emailver,))
        res3 = cursor.fetchone()
        account_balance = float(res3[0])
        if float(account_balance) < float(amount_to_withdrawl):
            messagebox.showinfo("Transfer Info!", "Insufficient Funds")
        else:
            cursor.execute("UPDATE users SET account_balance = account_balance - ? WHERE email = ?", (amount_to_withdrawl, emailver))
            messagebox._show("Withdrwawal Info!", "Successfully Withdrwan, please take your cash")  
            self.user_withdrawl_money(emailver)
  
    def Write_to_sql(self,unique_id):
        n = 10;range_start = 10**(n-1);range_end = (10**n)-1
        account_number = randint(range_start, range_end)
        bank = "Unilag Bank"
        account_balance = "10000"
        name = self.uentry.get()
        password = self.pentry.get()
        ###changes
        email1 = self.mail.get()
        number = self.Num.get()
        
        # data = (unique_id,account_number,name, email1,number,bank, password, account_balance)
        # # Insert data into the table
        # cursor.execute("INSERT INTO users (unique_id,account_number,name, email,number,bank, password, account_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        try:
            # Data to be inserted
            data = (unique_id, account_number, name, email1, number, bank, password, account_balance)
            # Execute the SQL INSERT statement
            cursor.execute("INSERT INTO users (unique_id, account_number, name, email, number, bank, password, account_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
            # Commit the transaction
            conn.commit()
            # Display a success message
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            # Display an error message if an exception occurs
            print("Error inserting data:", e)


        messagebox._show("Enrollment Info!", "Successfully Enrolled!")
        self.video_capture_page(unique_id)


    def video_capture_page(self,unique_id):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#8bdbc4",width=900,height=500)
        #Login Page Form Components
        self.label1 =Label(self.frame,text="Note:",bg="#8bdbc4",fg="white",font=ARIAL)
        self.label2 =Label(self.frame,text="1.By clicking on the 'Capture' button below, your image gets captured ",bg="#8bdbc4",fg="white",font=(ARIAL,15))
        self.label3 =Label(self.frame,text="2.You will be required to capture 5 images for full registration",bg="#8bdbc4",fg="white",font=(ARIAL,15))
        self.label4 =Label(self.frame,text="3.To capture each image click the space bar on your keyboard when the camera turn on:",bg="#8bdbc4",fg="white",font=(ARIAL,15))
        self.label5 =Label(self.frame,text="4. Please wait till you are notified that your capture was successful before leaving the page",bg="#8bdbc4",fg="white",font=(ARIAL,15))
        # data = pd.read_csv('bank_details.csv')
        self.label6 =Label(self.frame,text="5.To begin, click the 'Capture' button below and click the space bar to capture a new image",bg="#8bdbc4",fg="white",font=(ARIAL,15))
        self.button = Button(self.frame,text="Capture",bg="#50A8B0",fg="white",font=ARIAL,command=lambda:self.captureuser(unique_id))
        self.label1.place(x=0,y=0,width=1000,height=32)
        self.label2.place(x=0,y=32,width=1000,height=32)
        self.label3.place(x=0,y=64,width=1000,height=32)
        self.label4.place(x=0,y=96,width=1000,height=32)
        self.label5.place(x=0,y=128,width=1000,height=32)
        self.label6.place(x=0,y=160,width=1000,height=32)
        self.button.place(x=0,y=230,width=1000,height=70)
        self.frame.pack()

    #hit space bar to capture
    def captureuser(self,unique_id):
        # data = pd.read_csv('bank_details.csv')
        name = unique_id
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("capture")

        img_counter = 0
       
        dirname = f'data/{name}'
        os.mkdir(dirname)

        while True:
            ret, frame = cam.read()
            cv2.imshow("capture", frame)
           
            if img_counter == 5:
                cv2.destroyWindow("capture")
                break
            if not ret:
                break
            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                path = f'data/{name}'
                img_name = "{}.jpg".format(img_counter)
                cv2.imwrite(os.path.join(path , img_name), frame)
                # cv2.imwrite(img_name, frame)
                print("{} written!".format(img_counter))
                
                if img_counter == 4 :
                    path = f'dataset'
                    img_name = "{}.jpg".format(unique_id)
                    cv2.imwrite(os.path.join(path , img_name), frame)
                    # cv2.imwrite(img_name, frame)
                img_counter += 1
        cam.release()

        cv2.destroyAllWindows()
       
        self.get_embeddings()
        #self.get_embeddings()
        self.train_model()
        messagebox._show('Face Id Successfully Registered!')
        self.begin_page()



    def get_embeddings(self):
        #summary:
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--dataset", required=True,
            help="path to input directory of faces + images")
        ap.add_argument("-e", "--embeddings", required=True,
            help="path to output serialized db of facial embeddings")
        ap.add_argument("-d", "--detector", required=True,
            help="path to OpenCV's deep learning face detector")
        ap.add_argument("-m", "--embedding-model", required=True,
            help="path to OpenCV's deep learning face embedding model")
        ap.add_argument("-c", "--confidence", type=float, default=0.5,
            help="minimum probability to filter weak detections")
        #args = vars(ap.parse_args())
       
        # load our serialized face detector from disk
        print("[INFO] loading face detector...")

        detector = cv2.dnn.readNetFromCaffe('face_detection_model/deploy.prototxt', 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel')
        # load our serialized face embedding model from disk
        embedder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')
        #embedder = cv2.dnn.readNetFromTorch('openface_nn4.small2.v1.t7')

        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images('dataset'))
        # initialize our lists of extracted facial embeddings and
        # corresponding people names
        knownEmbeddings = []
        knownNames = []
        # initialize the total number of faces processed
        total = 0
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the image, resize it to have a width of 600 pixels (while
            # maintaining the aspect ratio), and then grab the image
            # dimensions
            image = cv2.imread(imagePath)
            image = imutils.resize(image, width=600)
            (h, w) = image.shape[:2]
            # construct a blob from the image
            imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)

            # apply OpenCV's deep learning-based face detector to localize
            # faces in the input image
            detector.setInput(imageBlob)
            detections = detector.forward()

            # ensure at least one face was found
            if len(detections) > 0:
                # we're making the assumption that each image has only ONE
                # face, so find the bounding box with the largest probability
                i = np.argmax(detections[0, 0, :, 2])
                confidence = detections[0, 0, i, 2]

                # ensure that the detection with the largest probability also
                # means our minimum probability test (thus helping filter out
                # weak detections)
                if confidence > 0.5:
                    # compute the (x, y)-coordinates of the bounding box for
                    # the face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # extract the face ROI and grab the ROI dimensions
                    face = image[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue

                    # construct a blob for the face ROI, then pass the blob
                    # through our face embedding model to obtain the 128-d
                    # quantification of the face
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                        (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()
       
                    # add the name of the person + corresponding face
                    # embedding to their respective lists
                    knownNames.append(name)
                    knownEmbeddings.append(vec.flatten())
                    total += 1
        # dump the facial embeddings + names to disk
        print("[INFO] serializing {} encodings...".format(total))
        data = {"embeddings": knownEmbeddings, "names": knownNames}
        f = open('output/embeddings.pickle', "wb")
        f.write(pickle.dumps(data))
        f.close()
   
    

    def train_model(self):
        # Summary
        print("[INFO] loading face embeddings...")
        
        # Load the embeddings and labels from the saved pickle file
        data = pickle.loads(open('output/embeddings.pickle', "rb").read())
        
        # Check if the dataset contains at least two classes
        unique_classes = set(data["names"])
        if len(unique_classes) < 2:
            print("[ERROR] Dataset contains only one class. Please ensure your dataset has samples from multiple classes.")
            return

        # Encode the class labels
        le = LabelEncoder()
        labels = le.fit_transform(data["names"])
        
        # Train the model
        print("[INFO] training model...")
        recognizer = SVC(C=1.0, kernel="linear", probability=True)
        recognizer.fit(data["embeddings"], labels)
        
        # Write the trained model to disk
        with open('output/recognizer.pickle', "wb") as f:
            pickle.dump(recognizer, f)
        
        # Write the label encoder to disk
        with open('output/le.pickle', "wb") as f:
            pickle.dump(le, f)
        
        print("[INFO] Model training completed successfully.")
  
    
    
    def video_check(self,emailver):
        # Path to the folder containing images
        folder = "dataset"
        unique_id = cursor.execute('SELECT unique_id FROM users WHERE email = ?', (emailver,)).fetchone()[0] if cursor.execute('SELECT COUNT(unique_id) FROM users WHERE email = ?', (emailver,)).fetchone()[0] > 0 else None


        # Load all images from the folder along with their file names
        images = []
        image_names = []
        for filename in os.listdir(folder):
            img_path = os.path.join(folder, filename)
            if os.path.isfile(img_path):
                image = face_recognition.load_image_file(img_path)
                images.append(image)
                image_names.append(filename)  # Store the image file name

        # Initialize list to store face encodings and corresponding image names
        known_face_encodings = []
        known_image_names = []

        # Iterate over the loaded images to compute face encodings
        for image, name in zip(images, image_names):
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                known_face_encodings.append(face_encodings[0])  # Assuming there's only one face in each image
                known_image_names.append(name)

        # Initialize variables
        face_locations = []
        face_names = []

        # Get a reference to the webcam (0 if you have one webcam, otherwise you can try different indices)
        video_capture = cv2.VideoCapture(0)
        real_user_list = []

        timeout = time.time() + 5

        while True:
            if time.time() > timeout :
                cv2.destroyWindow("Video")
                break

            # Capture frame-by-frame
            ret, frame = video_capture.read()

            # Resize frame to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            
            # Only proceed if faces are found
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    if True in matches:
                        # Get the index of the first match
                        match_index = matches.index(True)
                        # Get the corresponding image name from the known_image_names list
                        name = known_image_names[match_index]
                        if name == (str(unique_id)+".jpg"):
                            real_user_list.append(unique_id)
                        #     # video_capture.release()
                        #     # cv2.destroyAllWindows()
                        #     self.final_page(emailver)
                    
                    face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4        
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        path = f'Fraud'
        img_name = "{}.jpg".format(unique_id)
        cv2.imwrite(os.path.join(path , img_name), frame)

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        lenth = len(real_user_list)
        max = real_user_list.count(unique_id)
       
        if self.countter != 0:
            if max == 0:
                messagebox._show("Verification Info!", "Face Id match failed! You have {} trials left".format(self.countter))
                self.countter = self.countter - 1
                self.video_check(emailver)
            elif max>0.6*lenth:
                messagebox._show("Verification Info!", "Face Id match!")
                self.final_page(emailver)
        else:
            # self.fraud_message(emailver)
            self.fraud_mail(emailver)
            messagebox._show("Verification Info!", "Face Id match failed! You cannot withdraw at this time, try again later")
            self.begin_page()
            self.countter = 2
        # print(real_user_list)


    def face_match(self,emailver):
        
        detector = cv2.dnn.readNetFromCaffe('face_detection_model/deploy.prototxt', 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel')
        #summary
        # load our serialized face embedding model from disk
        print("[INFO] loading face recognizer...")
        embedder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')

        # load the actual face recognition model along with the label encoder
        recognizer = pickle.loads(open('output/recognizer.pickle', "rb").read())
        le = pickle.loads(open('output/le.pickle', "rb").read())

        # initialize the video stream, then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        #run check for only 15seconds and then stop
        timeout = time.time() + 5
       
        # start the FPS throughput estimator
        fps = FPS().start()

            # loop over frames from the video file stream
        real_user_list = []    
        while True:
            
            #run check for only 15seconds and then stop
            if time.time() > timeout :
                cv2.destroyWindow("Frame")
                break;
               
            # grab the frame from the threaded video stream
            frame = vs.read()

            frame = imutils.resize(frame, width=800, height=200)
            (h, w) = frame.shape[:2]

            # construct a blob from the image
            imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)

            # apply OpenCV's deep learning-based face detector to localize
            # faces in the input image
            detector.setInput(imageBlob)
            detections = detector.forward()

            #TODO: if 2 faces are detected alert the user of a warning
            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections
                if confidence > 0.5:
                    # compute the (x, y)-coordinates of the bounding box for
                    # the face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # extract the face ROI
                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue

                    # quantification of the face
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                        (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()

                    # perform classification to recognize the face
                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]

                    #Decision boundary
                    if (name == 'unknown') or (proba *100) < 90:
                        print("Fraud detected")
                        real_user_list.append(name)
                    else:
                        #cv2.destroyWindow("Frame")
                        real_user_list.append(name)
                        break
                       

            # update the FPS counter
            fps.update()

            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
       

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        print(real_user_list)
        
        try:
            Counter(real_user_list).most_common(1)[0][0] == 'unknown'
        except IndexError:       
            if self.countter != 0:
                messagebox._show("Verification Info!", "Face Id match failed! You have {} trials left".format(self.countter))
                self.countter = self.countter - 1
                self.video_check()
            else:
                messagebox._show("Verification Info!", "Face Id match failed! You cannot withdraw at this time, try again later")
                self.begin_page()
                self.countter = 2
            
           
        else:
            if Counter(real_user_list).most_common(1)[0][0] == 'unknown':
                if self.countter != 0:
                    messagebox._show("Verification Info!", "Face Id match failed! You have {} trials left".format(self.countter))
                    self.countter = self.countter - 1
                    self.video_check()
                else:
                    self.fraud_message(emailver)
                    self.fraud_mail(emailver)
                    messagebox._show("Verification Info!", "Face Id match failed! You cannot withdraw at this time, try again later")
                    self.begin_page()
                    self.countter = 2
                
            else:
                self.real_user = int(Counter(real_user_list).most_common(1)[0][0])
                messagebox._show("Verification Info!", "Face Id match!")
                self.final_page()


    def fraud_message(self,emailver):
        client = Client(account_sid, auth_token)
    
        try:
            # Execute the SQL query to get the phone number
            cursor.execute('SELECT number FROM users WHERE email = ?', (emailver,))
            # Fetch the result
            result = cursor.fetchone()  # Use fetchone() instead of fetchall() to get a single result

            if result:
                # Extract the phone number from the result
                num = result[0]
                if num:
                    # Send an SMS message
                    message = client.messages.create(
                        from_='+12513698579',  # Twilio phone number
                        body='Dear Customer, we detected potential unauthorized access to your debit card. Block your card immediately, review recent transactions, and report any fraud to your bank. Contact your bank\'s 24/7 helpline for assistance.',
                        to='+91' + num  # Recipient's phone number
                    )
                    print(message.sid)
                else:
                    print("Phone number is empty.")
            else:
                print("No user found with the provided email.")

        except Exception as e:
            print(f"An error occurred: {e}")


    def fraud_mail(self,emailver):
        cursor.execute('SELECT unique_id FROM users WHERE email = ?', (emailver,))
        # Fetch the result
        unikid = cursor.fetchone()
        cursor.execute('SELECT name FROM users WHERE email = ?', (emailver,))
        # Fetch the result
        names = cursor.fetchone()
        image_path = 'Fraud/'+str(unikid[0])+'.jpg'
        with open(image_path, 'rb') as f:
            data = f.read()
            encoded_image = base64.b64encode(data).decode()
    
        attachment = Attachment(
            FileContent(encoded_image),
            FileName(os.path.basename(image_path)),
            FileType('image/jpg'),
            Disposition('attachment')
        )
        
        message = Mail(
        from_email='msraut07@gmail.com',
        to_emails=emailver,
        subject='Urgent Alert: Potential Unauthorized Access to Your Debit Card',
        html_content='''
        
            <p>Dear Customer,</p>
            <p>We have detected that someone may be trying to access your debit card. To protect your account and prevent any unauthorized transactions, please take the following steps immediately:</p>
            <ol>
                <li><strong>Block Your Card:</strong> Contact your bank’s customer service or use their online banking/mobile app to block your card immediately.</li>
                <li><strong>Check Transactions:</strong> Review your recent transactions for any suspicious activity.</li>
                <li><strong>Report Fraud:</strong> Inform your bank of any unauthorized charges and request a new debit card.</li>
            </ol>
            <p>If you need assistance, contact your bank's 24/7 helpline immediately.</p>
            '''
            )
        message.attachment = attachment
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

root = Tk()
root.title("SBI Bank")
root.geometry("1100x700")
root.configure(bg="#8bdbc4")

obj = BankUi(root)
root.mainloop()
