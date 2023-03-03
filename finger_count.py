import mediapipe as mp
import cv2
mphands=mp.solutions.hands
draw=mp.solutions.drawing_utils
hands=mphands.Hands(max_num_hands=2,min_detection_confidence=0.7)

cap=cv2.VideoCapture(0)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(img)
    cv2.rectangle(img,(20,390),(200,440),(255,255,0),cv2.FILLED)
    tipid=[4,8,12,16,20]  # tip code for every finger
    lmlist=[]
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id,lm in enumerate(hand_landmarks.landmark):   # giving id for each point
                cx=lm.x  # coordinates of x
                cy=lm.y  # coorrdinates of y
                lmlist.append([id,cx,cy])
                
                if len(lmlist)!=0 and len(lmlist)==21:
                    fingerlist=[]

                    #thumb
                    if lmlist[12][1]>lmlist[20][1]:
                        if lmlist[tipid[0]][1]>lmlist[tipid[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    
                    else:
                        if lmlist[tipid[0]][1]<lmlist[tipid[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                        
                    
                
    

                  #other fingers

                    for i in range(1,5):   #thumb not included
                        if lmlist[tipid[i]][2]<lmlist[tipid[i]-2][2]:       #[2] indicates the index of  y coordinate of the lmlst
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    print(fingerlist)


                    if len(fingerlist)!=0:
                        fingercount=fingerlist.count(1)   #counts the number pf ones in the list. 1 represents finger
                    

                    cv2.putText(img,'fingers' + '=' + str(fingercount),(25,425),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),4)   #puttext function is used to write a value 0r string
                    
                draw.draw_landmarks(img,hand_landmarks,mphands.HAND_CONNECTIONS,draw.DrawingSpec(color=(200,255,200),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2))


    cv2.imshow("Hand gesture",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cv2.destroyAllWindows()
print(lmlist)
