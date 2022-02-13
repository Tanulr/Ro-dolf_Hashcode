#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from time import time
import math
import mediapipe as mp
import matplotlib.pyplot as plt
a = 1 #no. of frames
b = 1 #accurate frames; global variables


# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils


# In[3]:


def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''
    
    # Create a copy of the input image.
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape
    
    # Initialize a list to store the detected landmarks.
    landmarks = []
    
    # Check if any landmarks are detected.
    if results.pose_landmarks:
    
        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        
        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    
    # Check if the original input image and the resultant image are specified to be displayed.
    if display:
    
        # Display the original input image and the resultant image.
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
        # Also Plot the Pose landmarks in 3D.
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        
    # Otherwise
    else:
        
        # Return the output image and the found landmarks.
        return output_image, landmarks


# In[4]:


def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.
    '''

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle


# In[19]:


def classifyPose(a, b, landmarks1, output_image1, landmarks2, output_image2, display=False):
    '''
    This function classifies yoga poses depending upon the angles of various body joints.
    Args:
        landmarks: A list of detected landmarks of the person whose pose needs to be classified.
        output_image: A image of the person with the detected pose landmarks drawn.
        display: A boolean value that is if set to true the function displays the resultant image with the pose label 
        written on it and returns nothing.
    Returns:
        output_image: The image with the detected pose landmarks drawn and pose label written.
        label: The classified pose label of the person in the output_image.
    '''
    
    # Initialize the label of the pose. It is not known at this stage.
    #label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    # color = (0, 0, 255)
    a = a+1 #add frame count
    
    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------
    
    # Get the angle between the left shoulder, elbow and wrist points of REF IMAGE
    left_elbow_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks1[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks1[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # Get the angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks1[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks1[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # Get the angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks1[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks1[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks1[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks1[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks1[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks1[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points 
    right_knee_angle1 = calculateAngle(landmarks1[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks1[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks1[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    
    #---------------------------
    # Get the angle between the left shoulder, elbow and wrist points of COMPARE IMAGE
    left_elbow_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks2[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks2[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    # Get the angle between the right shoulder, elbow and wrist points. 
    right_elbow_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks2[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks2[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
    # Get the angle between the left elbow, shoulder and hip points. 
    left_shoulder_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks2[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks2[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points. 
    right_shoulder_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks2[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks2[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks2[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks2[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points 
    right_knee_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks2[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks2[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    
    #----------------------------------------------------------------------------------------------------------------
    
    # Check if all the angles lie within +/- 5 threshold of ref image angles
    #----------------------------------------------------------------------------------------------------------------
    c = 1 # acts as flag
#     if left_elbow_angle1-5 > left_elbow_angle2 or left_elbow_angle2 > left_elbow_angle1+5:
#         c = 0
#     if right_elbow_angle1-5 > right_elbow_angle2 or right_elbow_angle2 > right_elbow_angle1+5:
#         c = 0
#     if left_shoulder_angle1-5 > left_shoulder_angle2 or left_shoulder_angle2 > left_shoulder_angle1+5:
#         c = 0 
#     if right_shoulder_angle1-5 > right_shoulder_angle2 or right_shoulder_angle2 > right_shoulder_angle1+5:
#         c = 0
#     if left_knee_angle1-5 > left_knee_angle2 or left_knee_angle2 > left_knee_angle1+5:
#         c = 0
#     if right_knee_angle1-5 > right_knee_angle2 or right_knee_angle2 > right_knee_angle1+5:
#         c = 0
    if left_elbow_angle1-10 > left_elbow_angle2 or left_elbow_angle2 > left_elbow_angle1+10:
        c = 0
    if right_elbow_angle1-10> right_elbow_angle2 or right_elbow_angle2 > right_elbow_angle1+10:
        c = 0
    if left_shoulder_angle1-10 > left_shoulder_angle2 or left_shoulder_angle2 > left_shoulder_angle1+10:
        c = 0 
    if right_shoulder_angle1-10 > right_shoulder_angle2 or right_shoulder_angle2 > right_shoulder_angle1+10:
        c = 0
    if left_knee_angle1-10 > left_knee_angle2 or left_knee_angle2 > left_knee_angle1+10:
        c = 0
    if right_knee_angle1-10 > right_knee_angle2 or right_knee_angle2 > right_knee_angle1+10:
        c = 0
        
    # If it reached till here then the angles must've been under the threshold. so we can add to accurate frames count
    if c:
        b = b+1
                 
    #----------------------------------------------------------------------------------------------------------------
    
#     # Check if the pose is classified successfully
#     if label != 'Unknown Pose':
        
#         # Update the color (to green) with which the label will be written on the image.
#         color = (0, 255, 0)  
    
#     # Write the label on the output image. 
#     cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    # Check if the resultant image is specified to be displayed.
    if display:
    
        # Display the resultant image.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image1[:,:,::-1]);plt.title("Ref Image");plt.axis('off');
        plt.imshow(output_image2[:,:,::-1]);plt.title("Compare Image");plt.axis('off');
        
    else:
        
        # Return the output image and the classified label.
        return output_image1, output_image2, a, b


# In[22]:


# Setup Pose function for video.
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3, model_complexity=1)

# Initialize the VideoCapture object to read from the webcam.
#camera_video
ref_frame = cv2.VideoCapture('/Users/anagharao/Downloads/Eel GUI-Final 2/short_compare_video.mp4')
compare_frame = cv2.VideoCapture('/Users/anagharao/Downloads/Eel GUI-Final 2/short_compare_video.mp4')
#ref_frame = cv2.VideoCapture('C:/Users/chiragr/Music/HACKS/Hashcode/compare_video.mp4')
#compare_frame = cv2.VideoCapture('C:/Users/chiragr/Music/HACKS/Hashcode/compare_video.mp4')

# Initialize a resizable window.
cv2.namedWindow('Reference Video', cv2.WINDOW_NORMAL)
cv2.namedWindow('Compare Video', cv2.WINDOW_NORMAL)

a = 1
b = 1
k=0
# Iterate until the webcam is accessed successfully.
while k==0:
   while k==0: 

   
       # Read a frame.
       ok1, frame1 = ref_frame.read()
       ok2, frame2 = compare_frame.read()

       
       if ok1==True or ok2==True:
           frame1 = cv2.flip(frame1, 1)
           frame2 = cv2.flip(frame2, 1)


           # Get the width and height of the frame
           frame1_height, frame1_width, _ =  frame1.shape
           frame2_height, frame2_width, _ =  frame2.shape


           # Resize the frame while keeping the aspect ratio.
           frame1 = cv2.resize(frame1, (int(frame1_width * (640 / frame1_height)), 640))
           frame2 = cv2.resize(frame2, (int(frame2_width * (640 / frame2_height)), 640))


           # Perform Pose landmark detection.
           frame1, landmarks1 = detectPose(frame1, pose_video, display=False)
           frame2, landmarks2 = detectPose(frame2, pose_video, display=False)


           # Check if the landmarks are detected.
           if landmarks1:
               if landmarks2:
                   # Perform the Pose Classification.
                   frame1, frame2, a, b = classifyPose(a, b, landmarks1, frame1, landmarks2, frame2, display=False)
                   #frame2 = classifyPose(landmarks2, frame2, display=False)


           # Display the frame.
           cv2.imshow('Reference Video', frame1)
           cv2.imshow('Compare Video', frame2)


           # Wait until a key is pressed.
           # Retreive the ASCII code of the key pressed
           ak = cv2.waitKey(1) & 0xFF

           # Check if 'ESC' is pressed.
           if(ak == 27):
               k=2
       else:
           cv2.destroyAllWindows()
           print(b/a*100)
           k=2

# Release the VideoCapture object and close the windows.
ref_frame.release()
compare_frame.release()
cv2.destroyAllWindows()
print(b/a*100)
