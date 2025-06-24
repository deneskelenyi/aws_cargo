#!/Users/dindi/Documents/Code/scrape/bin/python3

## 
## Super simple gradio to split up description:tracking and throw it in a DB
##

import gradio as gr
#from sqlalchemy import create_engine
#import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import logging 

# GLOBAL VARIABLES
logger = logging.getLogger(__name__)
load_dotenv(override=True,dotenv_path="./.env")

DB_PORT = int(os.getenv('DB_PORT',3306))
DB_HOST = os.getenv('DB_HOST','localhost')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB = os.getenv('DB','aws')
AWS_USER = os.getenv('AWS_USER')
AWS_PASS = os.getenv('AWS_PASS')


# not using sqlalchemy here
#engine = create_engine('mysql+mysqlconnector://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+':'+str(DB_PORT)+'/'+DB)

cparams = {'host':DB_HOST,'port':DB_PORT,'user':DB_USER,'passwd':DB_PASS,'database':DB}

mydb = mysql.connector.connect(**cparams)
c_dict = mydb.cursor(dictionary=True)

def insert_tracking(text)->str:
    mydb = mysql.connector.connect(**cparams)
    c_dict = mydb.cursor(dictionary=True)
    print("text received",text)
    ret = []
    retStr =""
    for line in text.split("\n"):
        print(line)
        try:
            description,trackingNumber = line.split(":")            
            print (description,trackingNumber)
            description=description.strip()
            trackingNumber = trackingNumber.strip()
            ret.append("inserted tracking number: "+trackingNumber)
            retStr+=description+":"+trackingNumber
            sql = '''insert ignore into ship_tracking
        (`tracking`, `description`) values (%s, %s);'''
        
            params=(trackingNumber,description)
            res = c_dict.execute(sql, params)   
            mydb.commit()
            ins_id= c_dict.lastrowid
            ret.append("inserted tracking number: "+str(ins_id)+":"+description+":"+trackingNumber)
            if ins_id is not None:
                retStr+= ": "+ str(ins_id) + "\n"
            else:
                retStr+="\n"
        except Exception as ex:
            print("error",ex)
        
    return "Finished:\n"+retStr
    
demo = gr.Interface(
    fn=insert_tracking,
    title="Insert Tracking",
    inputs=[gr.Textbox(lines=10, placeholder="Product: tracking",label="tracking numbers")],
    outputs=[gr.Textbox(lines=10, placeholder="",label="Inserted into tracking system")],
    flagging_options=["none"],
    allow_flagging="never"
)

demo.launch(share=False,server_name="0.0.0.0")
