#Cution:This example is not supported by the officail ImageAI!!!
#This is the examplpe for AIT test+Project_RSPImageRobot_20200801_0

#demo pictures: https://www.reddit.com/r/FortNiteBR/comments/7l2ovk/we_need_a_rock_paper_scissors_emotes/

#Nov 6 2020, Branched from "YM20200918_RSPImage" master and modified for the python practice.


from imageai.Detection.Custom import CustomVideoObjectDetection
import os
import cv2
import threading
import time
import random

import serial 
import serial.tools.list_ports

from pygame import mixer




UserSign=0
matchTable=[[1,2,0],[0,1,0],[0,0,1]]
SignDic={"five gesture":2,"v gesture":1,"fist gesture":0}
SignImageDic={0:"fist.png",1:"v.png",2:"five.png"}
scoreDic={0:"Lose",1:"Tight",2:"Win"}

ser=None
outputChar="0"


def GameLoopDisplay(ImgName,waitk):
    UIFrame = cv2.imread(ImgName)
    cv2.imshow("UI",UIFrame)
    cv2.waitKey(waitk)


def GameLoopMotion(MotionGesture):
    outputChar=str(MotionGesture)
    ser.write(outputChar.encode())

def gameLoop():
    var=1

    global UserSign
    
    GameLoopDisplay("0_PressAnyKey.png",0)



    MachineSign=random.randint(0,1)
    GameLoopMotion(MachineSign+1)
    GameLoopDisplay(SignImageDic[MachineSign],2000)
		
    matchResult=matchTable[UserSign][MachineSign]
		

    if 0 == matchResult:
        GameLoopDisplay("6_YouLoss.png",0)            
        
        

def per_frame_function_DataGet(counting, output_objects_array, output_objects_count,detected_frame):

    global UserSign
    
    if len(output_objects_array)!=0:
        UserSign=SignDic[output_objects_array[0]["name"]]
       
        
    cv2.imshow('getCamera',detected_frame)
    cv2.waitKey(1)
    

def videoLoop():
    execution_path = os.getcwd()
    camera = cv2.VideoCapture(0)

    video_detector = CustomVideoObjectDetection()
    video_detector.setModelTypeAsYOLOv3()
    video_detector.setModelPath("detection_model-ex-012--loss-0003.960.h5") #Download the model from "https://github.com/NAERSTEAM/EELAB/releases/download/20202603_0/detection_model-ex-012--loss-0003.960.h5"
    video_detector.setJsonPath("detection_config HandSign.json")
    video_detector.loadModel(detection_speed='fastest')

    video_detector.detectObjectsFromVideo(camera_input=camera,
                                          output_file_path=os.path.join(execution_path, "HandSignRecognition"),
                                          frames_per_second=20,
                                          minimum_percentage_probability=80,
                                          log_progress=False,
                                          save_detected_video=False,
                                          per_frame_function=per_frame_function_DataGet,
                                          return_detected_frame=True)
    


def serialPortSetting():
    global ser

    comlist = serial.tools.list_ports.comports()
    connected = []

    for element in comlist:
        connected.append(element.device)
        
    print("Connected COM ports: " + str(connected))
    COM_PORT = input("Port?:")
    
    BAUD_RATES = 9600
    ser = serial.Serial(COM_PORT, BAUD_RATES)

	
serialPortSetting()

thread_video=threading.Thread(target=videoLoop)
thread_game=threading.Thread(target=gameLoop)

thread_video.start()
thread_game.start()