#!/home/dindi/aws_client/.venv/bin/python3
from bs4 import BeautifulSoup
import mysql.connector
import datetime as dt
import time
import sys, os
import http.client, urllib
from dotenv import load_dotenv
from colorama import Fore, Back
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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

#you need a working Chrome installation and a matching chromedriver 
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH','./chromedriver/chromedriver')
WINDOW_SIZE = "1920,1080"

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN_AWS")
pushover_url = "https://api.pushover.net/1/messages.json"

# GLOBAL VARIABLES /

try:
    #use this for local/remote TCP connection
    cparams = {'host':DB_HOST,'port':DB_PORT,'user':DB_USER,'passwd':DB_PASS,'database':DB}

    # use this for UNIX socket
    # cparams = {'unix_socket':'/var/run/mysqld/mysqld.sock','user':DB_USER,'passwd':DB_PASS,'database':DB}

    mydb = mysql.connector.connect(**cparams)
    c_dict = mydb.cursor(dictionary=True)
    logger.info("Connected to DB")
except Exception as e:
    logger.info("Connected to DB")
    print(e)
    exit(-1)


def get_pending_notifications()->list:
    sql = """ SELECT *,o.tracking as o_tracking, o.id as o_id, t.tracking as t_tracking  from aws_orders o left join ship_tracking t
    on o.tracking like concat('%',trim(t.tracking),'%') where notified='';"""
    params=()
    
    c_dict.execute(sql,params)
    rs = c_dict.fetchall()
    mydb.commit()
    
    #print(rs)
    '''for r in rs:
        print("----------------------")
        print(r)
        #print(r["o_tracking"],r["t_tracking"],r["description"],r["price"])
       ''' 
    return rs

def reset_notified_status(ids):
    paramlist = []
    for id in ids:
        sql = """update aws_orders set notified=1 where id=%s;"""
        params=(id,)
        paramlist.append(params)
    c_dict.executemany(sql,paramlist)
    mydb.commit()

#print(type(notifications))

def send_notifications(notifications)->list:
    ids = []
    message = "You have new items at AWS Cargo"
    print(Fore.YELLOW,notifications)
    for r in notifications:
        print(r["o_id"],r["o_tracking"],r["t_tracking"],r["description"],r["price"])
        message += "\n"
        message += str(r["description"])
        message += " - $" + str(r["price"]) + ""
        message += " - " + r["o_tracking"]
        message += " - (" + str(r["t_tracking"]) + ")"

        ids.append(r["o_id"])
        
    reset_notified_status(ids)
    push(message)
    return ids
    

def push(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": pushover_token,
        "user": pushover_user,
        "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    print(conn.getresponse())


def insert_arrivals_from_html(html_text)->int:
    
    # use this for local testing only
    #f = open('test1.html', 'r')
    #html_text = f.read()
    
    soup = BeautifulSoup(html_text, features='html.parser')
    table = soup.find("table", attrs={ "id" : "ContentPlaceHolder1_PAQUETES" })
    tb = table.find('tbody')
    cnt = 0
    for row in tb.find_all("tr"):
        cells = row.find_all("td")
        cellsA =[]
        for cell in cells:
            cellsA.append(cell.text)
        try:                        
            
            if len(cellsA)<2:
                continue            
            #print(Fore.CYAN,"trying:", cellsA)
            #print(len(cellsA))
            #print(cellsA[0])            
            sql = '''insert ignore into aws_orders
            (`tracking`, `price`,`date_system`) values (%s, %s, %s);'''
            #s = "01/12/2011"
            ts = time.mktime(dt.datetime.strptime(cellsA[0], "%m/%d/%Y").timetuple())
            #print(ts)
            aws_date = dt.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
            #print(aws_date)            
            params=(cellsA[2].strip(),cellsA[5].strip(),aws_date,)
            #print(params)   
            res = c_dict.execute(sql, params)   
            mydb.commit()
            ins_id = c_dict.lastrowid            
            cnt += 1
            #print("ins_id", ins_id)
            #print("--------")
        except Exception as ex:
            #print(Fore.RED,ex)
            #logger.error(ex)
            pass
    f.close()
    return cnt

#pull html / scrape and return the page source
def get_html()->str:
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless")
    opt.add_argument("--window-size=%s" % WINDOW_SIZE)
    opt.add_argument('--no-sandbox')
    driver = webdriver.Chrome(opt)
    driver.get(url="https://system.awscargo.com/Login.aspx")
    user_f = driver.find_element(By.ID,'ContentPlaceHolder1_BoxUsuario')
    user_f.send_keys(AWS_USER)

    pass_f = driver.find_element(By.ID,'ContentPlaceHolder1_BoxContraseña')
    pass_f.send_keys(AWS_PASS)
    driver.find_element(By.ID,'ContentPlaceHolder1_Button1').click()
    time.sleep(2)    
    driver.get(url='https://system.awscargo.com/Clientes/MisPaquetes.aspx')
    page_source = driver.page_source
    
    #You don't need to save it, but you can, for debug
    #f = open('test_'+str(time.time())+'.html', 'x')
    #f.write(driver.page_source)
    #f.close()
    driver.quit()
    #print(Fore.CYAN,page_source,type(page_source))
    return page_source
    

def called():
    print(pushover_url)

def main():
    logging.basicConfig(filename='awscargo_notifications.log', level=logging.INFO)
    logger.info("Running: "+str(dt.date.today())+" at "+dt.datetime.now().strftime("%H:%M:%S"))
    ##page_source = get_html()
    html_text = get_html()
    notifications = []
    try:
        # there are nicer ways to do this, but if the HTML is not good, this will catch it
        # also, if there are no packages, there is no table, so it will just throw an exception
        insert_arrivals_from_html(html_text)    
    except Exception as e:
        print(e)
        logger.error(str(e))
        
        
    notifications = get_pending_notifications()
    
    # Don't send notifications, unless there are items in there
    if len(notifications)>0:
        ids = send_notifications(notifications)
        reset_notified_status(ids)
        print("\n\n",Fore.GREEN,ids,"sent",type(ids))
        logger.info("sent" + str(len(ids)) + " notifications")
    else:
        print(Fore.RED,"No pending notifications")
        logger.info("No pending notifications")
        
    #print(Fore.CYAN,page_source,type(page_source
    called()
    pass



if __name__ == "__main__":
	main()