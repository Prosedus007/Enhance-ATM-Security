from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from imutils.video import VideoStream
from imutils.video import FPS
import time
from tkinter import *
from tkinter import messagebox
import pymongo
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from bson import Binary

# Load environment variables from .env file
load_dotenv()

# Access environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# Get MongoDB connection string from environment variable
mongodb_uri = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = pymongo.MongoClient(mongodb_uri)

# Create or select a database
mydb = client["mydatabase"]

# Create or select a collection
mycol = mydb["customers"]

image_col = mydb["user_images"]

for x in mycol.find():
    print(x)


ARIAL = ("arial",25,"bold")

class BankUi:
    def __init__(self,root):
        # Load face embedding model
        self.embedder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')

        # Load face recognition model
        self.recognizer = pickle.loads(open('output/recognizer.pickle', "rb").read())

        # Load label encoder
        self.le = pickle.loads(open('output/le.pickle', "rb").read())

        # Load face detector
        self.detector = cv2.dnn.readNetFromCaffe('face_detection_model/deploy.prototxt', 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel')

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
        result = mycol.find_one({"email": emailver, "password": passwordver})

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
        
        res = mycol.find_one({"account_number": acc_number})
        res1 = mycol.find_one({"email": emailver})
        res3 = mycol.find_one({"email": emailver}, {"account_balance": 1})

        if not res:
            messagebox.showinfo("Transfer Info!", "Invalid account number")
        elif res1 and res1["account_number"] == acc_number:
            messagebox.showinfo("Transfer Info!", "Sorry, you cannot make a transfer to yourself")
        elif res3 and float(res3["account_balance"]) < float(amount):
            messagebox.showinfo("Transfer Info!", "Insufficient Funds")
        else:
            # Update recipient's account balance by adding the transfer amount
            mycol.update_one({"account_number": acc_number}, {"$inc": {"account_balance": float(amount)}})

            # Update sender's account balance by subtracting the transfer amount
            mycol.update_one({"email": emailver}, {"$inc": {"account_balance": float(-amount)}})

            messagebox.showinfo("Transfer Info!", "Successfully Transferred")
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
        result = mycol.find_one({"email": emailver}, {"account_balance": 1})
        text = result["account_balance"]
        self.label = Label(self.frame, text='Current Account Balance: ' + str(text), font=("arial", 25), fg="white", bg="#8bdbc4")
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
        amount_to_transfer = float(amount_to_transfer)
        update_result = mycol.update_one({"email": emailver}, {"$inc": {"account_balance": amount_to_transfer}})
        if update_result.modified_count > 0:
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
        result = mycol.find_one({"email": emailver}, {"account_balance": 1})


        account_balance = result.get("account_balance", 0)
        if float(account_balance) < float(amount_to_withdrawl):
            messagebox.showinfo("Transfer Info!", "Insufficient Funds")
        else:
            # Update the account balance after withdrawal
            updated_balance = float(account_balance) - float(amount_to_withdrawl)
            mycol.update_one({"email": emailver}, {"$set": {"account_balance": updated_balance}})
            messagebox.showinfo("Withdrawal Info!", "Successfully Withdrawn. Please take your cash.")
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
        
        data = (unique_id, account_number, name, email1, number, bank, password, account_balance)
       
        try:
            # Construct a dictionary representing the document to be inserted
            document = {
                "unique_id": unique_id,
                "account_number": account_number,
                "name": name,
                "email": email1,
                "number": number,
                "bank": bank,
                "password": password,
                "account_balance": float(account_balance)
            }
            
            # Insert the document into the collection
            mycol.insert_one(document)
            
            # Display a success message
            print("Data inserted successfully.")
        except pymongo.errors.PyMongoError as e:
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
    def captureuser(self, unique_id):
        num_images = 5
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("capture")
        img_counter = 0
        dirname = f'dataset/{unique_id}'
        os.makedirs(dirname, exist_ok=True)

        while True:
            ret, frame = cam.read()
            cv2.imshow("capture", frame)

            if img_counter == num_images:
                cv2.destroyWindow("capture")
                break
            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = f"{unique_id}_{img_counter}.jpg"
                img_path = os.path.join(dirname, img_name)
                cv2.imwrite(img_path, frame)
                print("{} written!".format(img_name))

                # Insert image into MongoDB
                with open(img_path, "rb") as f:
                    img_binary = Binary(f.read())
                    image_doc = {
                        "user_id": unique_id,
                        "image_data": img_binary
                    }
                    image_col.insert_one(image_doc)

                img_counter += 1

        cam.release()
        cv2.destroyAllWindows()
        # After capturing images, call the functions to generate embeddings and train the model
        self.get_embeddings(unique_id)
        self.train_model()

    def get_embeddings(self, unique_id):
        # Load face detector and embedding model
        detector = cv2.dnn.readNetFromCaffe('face_detection_model/deploy.prototxt', 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel')
        embedder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')
        
        # Query images associated with the unique_ids
        image_docs = image_col.find({"user_id": unique_id})

        # Initialize lists for embeddings and corresponding names
        knownEmbeddings = []
        knownNames = []

        # Loop through the images
        for image_doc in image_docs:
            # Extract image data from MongoDB
            image_binary = image_doc["image_data"]
            nparr = np.frombuffer(image_binary, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    def train_model(self):
        # Load the embeddings and labels from the saved pickle file
        data = pickle.loads(open('output/embeddings.pickle', "rb").read())

        # Check if the dataset contains at least two classes (same as in your code)
        unique_classes = set(data["names"])
        if len(unique_classes) < 2:
            print("[ERROR] Dataset contains only one class. Please ensure your dataset has samples from multiple classes.")
            

        # Train the model (same as in your code)
        self.begin_page()


    def video_check(self,emailver):
        
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

            # resize the frame to have a width of 600 pixels (while
            # maintaining the aspect ratio), and then grab the image
            # dimensions
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

                    # construct a blob for the face ROI, then pass the blob
                    # through our face embedding model to obtain the 128-d
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
                    #TODO: Handle if 2 faces are given.
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
                self.video_check(emailver)
            else:
                self.fraud_message(emailver)
                messagebox._show("Verification Info!", "Face Id match failed! You cannot withdraw at this time, try again later")
                self.begin_page()
                self.countter = 2
            
           
        else:
            if Counter(real_user_list).most_common(1)[0][0] == 'unknown':
                if self.countter != 0:
                    messagebox._show("Verification Info!", "Face Id match failed! You have {} trials left".format(self.countter))
                    self.countter = self.countter - 1
                    self.video_check(emailver)
                else:
                    messagebox._show("Verification Info!", "Face Id match failed! You cannot withdraw at this time, try again later")
                    self.begin_page()
                    self.countter = 2
                
            else:
                self.real_user = int(Counter(real_user_list).most_common(1)[0][0])
                messagebox._show("Verification Info!", "Face Id match!")
                self.final_page(emailver)

    def fraud_message(self,emailver):
        client = Client(account_sid, auth_token)
        result = mycol.find_one({"email": emailver}, {"number": 1})
      
        # Extract the phone number from the result
        num = result[0]
        # Send an SMS message
        message = client.messages.create(
            from_='+12513698579',  # Twilio phone number
            body='Someone is trying to access your bank account. Block your Card Immediately.',          # Message body
            to='+91' + num    # Recipient's phone number
        )
        print(message.sid)

    # client.close()   
root = Tk()
root.title("SBI Bank")
root.geometry("1100x700")
root.configure(bg="#8bdbc4")

obj = BankUi(root)
root.mainloop()
