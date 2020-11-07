#!/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import getpass
import mysql.connector
classStatus=False
currentPeriod='Free'
classCodes={'classname':'classid','classname','classid',...} #Enter your class name as mentioned in db and class code here

dbhost='' #Enter db details here
dbuser=''
dbpassword=''
dbname=''
meetHome="https://meet.google.com"
emailId=str(input('Enter your email id:'))
password=getpass.getpass()

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 2 
  })

def printBanner():
    print('              _ _                   _                 _           _   ')
    print('             | (_)                 | |               | |         | |  ')
    print('   ___  _ __ | |_ _ __   ___    ___| | __ _ ___ ___  | |__   ___ | |_ ')
    print('  / _ \\| \'_ \\| | | \'_ \\ / _ \\  / __| |/ _` / __/ __| | \'_ \\ / _ \\| __|')
    print(' | (_) | | | | | | | | |  __/ | (__| | (_| \__ \__ \ | |_) | (_) | |_ ')
    print('  \___/|_| |_|_|_|_| |_|\___|  \___|_|\__,_|___/___/ |_.__/ \___/ \__|')
    print('\n\n            Made by karthik\n')

def checkPeriod(): #Configure time here
    timeNow=time.localtime()
    periodNow=""
    if timeNow[3]==9 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period1"
    elif timeNow[3]==10 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period2"
    elif timeNow[3]==11 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period3"
    elif timeNow[3]==12 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period4"
    elif timeNow[3]==14 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period5"
    elif timeNow[3]==15 and timeNow[4]>=0 and timeNow[4]<=50:
        periodNow="period6"
    elif (timeNow[3]==15 and timeNow[4]>=50) or (timeNow[3]==18 and timeNow[4]<=1):
        periodNow="period7"
    else:
        periodNow="free"
    return periodNow

def getDayOrder():
    global dayOrder
    dayOrder=int(input('Enter today\'s day order:'))

def connectSql():
    global connectDb,mycursor,dbhost,dbuser,dbpass,dbname
    connectDb=mysql.connector.connect(host=dbhost,user=dbuser,password=dbpassword,database=dbname)
    mycursor=connectDb.cursor()
    
def fetchPeriod():
    global periodName
    if checkPeriod()!="free":
        query='SELECT '+checkPeriod()+' FROM timetable WHERE day='+str(dayOrder)+';'
        mycursor.execute(query)
        result=mycursor.fetchall()
        periodName=result[0][0]
    else:
        periodName="free"
    return periodName

def gmailLogin():
    global classStatus
    classStatus=False
    global driver
    driver=webdriver.Chrome(options=opt)
    print("[+] Opening Google chrome")
    driver.get(meetHome)
    time.sleep(5)
    signin=driver.find_element_by_xpath('/html/body/header/div[1]/div/div[3]/div[1]/div/span[1]/a')
    signin.click()
    emailField=driver.find_element_by_xpath('//*[@id="identifierId"]')
    emailField.clear()
    emailField.send_keys(emailId)
    emailButton=driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button')
    emailButton.click()
    time.sleep(5)
    passField=driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    passField.clear()
    passField.send_keys(password)
    loginButton=driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button')
    loginButton.click()
    print("[+] Gmail login successful")

def joinMeet():
    global classStatus
    global currentPeriod
    meetCode=""
    currentPeriod=periodName
    meetCode=classCodes[periodName]
    driver.get(meetHome)
    time.sleep(8)
    driver.find_element_by_xpath('/html/body/header/div[1]/div/div[3]/div[1]/div/span[1]/a').click()
    print("[+] Joining "+periodName+" class, code:"+meetCode)
    time.sleep(5)
    meetIdInput=driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[2]/div[2]/div/c-wiz/div[1]/div/div/div[1]')
    meetIdInput.send_keys(meetCode)
    submit=driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/span/div/div[4]/div[2]/div')
    submit.click()
    time.sleep(5)
    dismiss=driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div')
    dismiss.click()
    print("[+] Microphone turned off")
    print("[+] Camera turned off")
    time.sleep(8)
    join=driver.find_element_by_xpath('/html/body/div/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]')
    join.click()
    print("[+] Class joined")
    time.sleep(5)
    try:
        closeInfo=driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[2]/div[3]/div')
        closeInfo.click()
    except:
        pass
    classStatus=True

def leaveMeet():
    global classStatus
    dismissButton=driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div')
    dismissButton.click()
    classStatus=False
    print("[+] Left from class")

printBanner()
connectSql()
print('[+] Successfully connected with database')
getDayOrder()
gmailLogin()
#timing starts
while True:
    if time.localtime()[3]>=9 and time.localtime()[3]<=17: #It is currently configured to run between 9 am and 5 pm
        fetchPeriod()
        if classStatus==False and fetchPeriod()!="free":
            joinMeet()
        if currentPeriod!=fetchPeriod() and classStatus==True:
            leaveMeet()
    else:
        print('[*] Class time over')
        break
    time.sleep(30)
driver.close()
connectDb.close()
