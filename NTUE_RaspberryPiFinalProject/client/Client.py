import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import RPi.GPIO as GPIO
import mariadb
import sys
import os
from time import sleep
from math import floor

# ----------------------------------------------

GPIO.setwarnings(False)

myUser="wpuser"
myPassword="123456"
myHost="192.168.43.221"
myPort=3306
myDatabase="final_data"
myTable = "log"

sevenSegmentStringDict = {
  0: "0111111",
  1: "0000110",
  2: "1011011",
  3: "1001111",
  4: "1100110",
  5: "1101101",
  6: "1111101",
  7: "0000111",
  8: "1111111",
  9: "1101111"
}

pin10_segA = 19
pin10_segB = 13
pin10_segC = 6
pin10_segD = 5
pin10_segE = 22
pin10_segF = 27
pin10_segG = 17
pin_segA = 24
pin_segB = 23
pin_segC = 21
pin_segD = 20
pin_segE = 16
pin_segF = 25
pin_segG = 12
sevenSegmentPin10 = [pin10_segG, pin10_segF, pin10_segE, pin10_segD, pin10_segC, pin10_segB, pin10_segA]
sevenSegmentPin = [pin_segG, pin_segF, pin_segE, pin_segD, pin_segC, pin_segB, pin_segA]

pin_key = 2
loadInitData = False
nowTemp = True
tempNumber = 0
wetNumber = 0

# ---------------------------------------------- 

def getSqlData():
  try:
    print("----- Connect to MariaDB Platform -----")
    conn = mariadb.connect(user=myUser, password=myPassword, host=myHost, port=myPort, database=myDatabase)
    cur = conn.cursor()
    sql = "Show tables;"
    cur.execute(sql)
    allTable = cur.fetchall()
    sql = "use {};".format(myDatabase)
    cur.execute(sql)
    sql = "SELECT * FROM {};".format(myTable)
    cur.execute(sql)
    allColumns = cur.fetchall()
    df = pd.DataFrame(allColumns)
    conn.close()
    print("------------- Connect Done ------------")
    global loadInitData
    loadInitData = True
    updateNumber(df)
    return df
  except mariadb.Error as e:
    print("------------- Connect Dead! -----------")
    print(f"Error connecting to MariaDB Platform: {e}")
    conn.close()
    sys.exit(1)
  except Exception as e:
    print("------------- Connect Dead! -----------")
    print(e)

# ----------------------------------------------

def drawChart(dataframe):
  for i in range(5):
    if i==1:
      continue
    dataframe[i] = dataframe[i].astype('float64')
  timeList = dataframe[1]
  tempList = dataframe[2]
  wetList = dataframe[3]
  FontSize = 20
  PltWidth = 80
  PltHeight = 15
  PltDpi = 80
  try:
    print("-------------- Draw Start -------------")
    print("Now drawing......")
    print("  x = time, y = wet")
    plt.figure(figsize=(PltWidth, PltHeight), dpi=PltDpi)
    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.plot(timeList, wetList, '-.')
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.title('humidity', fontsize=FontSize)
    plt.xlabel('time', fontsize=FontSize)
    plt.ylabel('(%)', fontsize=FontSize)
    plt.savefig("/home/pi/web-jesse/images/outputWet.jpg")
    print("Now drawing......")
    print("  x = time, y = temp")
    plt.figure(figsize=(PltWidth, PltHeight), dpi=PltDpi)
    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.plot(timeList, tempList, 'r:')
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.title('temperature', fontsize=FontSize)
    plt.xlabel('time', fontsize=FontSize)
    plt.ylabel('T(℃)', fontsize=FontSize)
    plt.savefig("/home/pi/web-jesse/images/outputTemp.jpg")
    print("--------------- Draw Done -------------")
    os.system("sudo cp /home/pi/web-jesse/images/* /var/www/html")
    print("-------------- Update Done ------------")
  except Exception as e:
    print("-------------- Draw Dead! -------------")
    print(e)

# ----------------------------------------------

def updateNumber(dataframe):
  global tempNumber
  tempNumber = round(float(dataframe[2].tail(1)))
  global wetNumber
  wetNumber = round(float(dataframe[3].tail(1)))

# ----------------------------------------------

def segInit():
  GPIO.setmode(GPIO.BCM)
  try:
    GPIO.setup(pin_key, GPIO.IN, GPIO.PUD_UP)
    print("------------ key setup done -----------")
    for pin in sevenSegmentPin10:
      GPIO.setup(pin, GPIO.OUT)
    for pin in sevenSegmentPin:
      GPIO.setup(pin, GPIO.OUT)
    for pinIndex in range(7):
      value = int(sevenSegmentStringDict[0][pinIndex])
      GPIO.output(sevenSegmentPin10[pinIndex], value)
      GPIO.output(sevenSegmentPin[pinIndex], value)
    print("--------- 7-Segment setup done --------")
  except Exception as e:
    print("-------------- 7Seg Dead! -------------")
    print(e)

# ----------------------------------------------

def segNumberChange(pin_key):
  global nowTemp
  nowTemp = not nowTemp
  while(not loadInitData):
    print("not loadInitData ... ")
    sleep(1)
  sevenSegmentControl(nowTemp)

# ----------------------------------------------

def sevenSegmentControl(showTemp):
  try:
    if(showTemp):
      getNumber = tempNumber
    else:
      getNumber = wetNumber
    number10 = floor(getNumber/10)
    number = getNumber%10
    for pinIndex in range(7):
      value10 = int(sevenSegmentStringDict[number10][pinIndex])
      GPIO.output(sevenSegmentPin10[pinIndex], value10)
      value = int(sevenSegmentStringDict[number][pinIndex])
      GPIO.output(sevenSegmentPin[pinIndex], value)
  except Exception as e:
    print("-------------- 7Seg Dead! -------------")
    print("now number = ", number)
    print(e)

# ----------------------------------------------

def welcomeOuO():
  print("\n\n\n")
  print("╔═════════════════════════════╗")
  print("║                             ║")
  print("║                             ║")
  print("║         Welcome To          ║")
  print("║   Medicine Control System   ║")
  print("║                             ║")
  print("║                             ║")
  print("╚═════════════════════════════╝")


def modeCtrl():
  try:
    while(True):
      userMode = input(" 0 : exit\n 1 : only web\n 2 : web and 7-segement\n : ")
      if userMode == '0':
        print("-------------- ByeBye OuO! -------------\n\n\n")
        sys.exit(1)
      if userMode == '1' or userMode == '2':
        print("\n\n\n")
        return userMode
      else:
        continue
  except Exception as e:
    print("------------ modeCtrl Error -----------")
    print(e)

# ----------------------------------------------

def main():
  welcomeOuO()
  user = modeCtrl()
  try:
    if(user=='2'):
      segInit()
      GPIO.add_event_detect(pin_key, GPIO.FALLING, callback=segNumberChange, bouncetime=200)
    while(True):
      data = getSqlData()
      if(user=='2'):
        sevenSegmentControl(nowTemp)
      drawChart(data)
      sleep(60)
  except KeyboardInterrupt:
    print("\n----------- User Interrupt ------------")
  except Exception as e:
    print("---------- other Exception -----------")
    print(e)
  finally:
    GPIO.cleanup()
    print("---------- GPIO cleanup done ----------")
    print("------------ end of main() ------------")
    print("\n")
    print("-------------- ByeBye OuO! -------------")
    print("\n\n\n")

# ----------------------------------------------

if __name__ == '__main__':
  main()

