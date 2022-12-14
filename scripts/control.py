#!/usr/bin/env python3

from __future__ import print_function

import rospy
import math
import mediapipe as mp

from geometry_msgs.msg import Twist

"""
  This node should arrange the motion of the robot once a person is detected. Of course
  there are several ways in which the robot can approach the person.
  However the final position in which the robot should do all the investigations is near the 
  head (mantaing a certain distance), framing both the face and the body, in order to see if
  the person is moving its own body and to see if it is blinking. (Also to have the microphone
  as close as possible to the person's mouth). Instead the position of the person can be computed 
  a priori. 

  - LAY DOWN : - if the person is seen by side the robot should compute the middle point between
                 the distance from the nose to the foot. Set a safe distance between the person and 
                 the robot (using depth cameras), and then move near the head facing also the body

               - if the person is seen from the foot the robot should compute the distance between itself
                 and the foot (depth camera), translate to the left or to the right, rotates of 90° 
                 (orario o antiorario dipende come ha traslato il robot) and traslate again. In that case
                 we come back to the case aforementioned

               - if the person is seen from the head the robot should just adjust its angle in a way
                 that it can see both nose and feet landmarks.

  - SIT DOWN : this case is similar to the previous (you can differentiate from the previos taking
               into account the y position of the nose)

  - STAND UP : - if the person is seen from the front --> ok
               - if the person is seen by side the robot should rotate until it visualize (greater than
                 a treshold) the face landmarks.
               - if the person is seen from the back same as before.  
"""

detection = None
full_detection = None
status = None
pub = None


def depth_callback(data):
    """
      Callback function of the depth camera
    """
    try:
        depth_image = self.bridge.imgmsg_to_cv2(data, 'passthrough')
    except CvBridgeError as e:
        print(e)


def detection():
    # make a detection
    global detection
    if len(results.pose_landmarks) > threshold :
       detection == True
       print("A person has been found")
    else:
        detection == False
        print("Serching for people to rescue")
    return detection


def compute_position():
    # evaluate the postion
    global detection, status
    while detection == True:
        # stand up
        if results.pose_world_landmarks.landmark[0].y > (1.50 m):
            status == 'stand up'
        # sit down
        if results.pose_world_landmarks.landmark[0].y < (1.50 m) and results.pose_world_landmarks.landmark[0].y > (0.30 m):
            status == 'sit down'
        # lay down
        if results.pose_world_landmarks.landmark[0].y < (0.30 m):
            status == 'lay down'
    return status


def f_detection():
    """
         The detection can be performed in two different ways: 
        - len(results) > threshold
        - the visibility of both nose and foot is greater than a threshold 
     """
    global detection, full_detection
    nose_vis = results.pose_landmarks.landmark[0].visibility
    left_foot_vis = results.pose_landmarks.landmark[31].visibility
    right_foot_vis = results.pose_landmarks.landmark[32].visibility

    if detection == True and nose_vis > 0.9 and (left_foot_vis > 0.9 or right_foot_vis > 0.9):
        full_detection = True
        print('The person has been framed')
    else:
        full_detection = False
        print('Adjusting the robot')
    return full_detection



def compute_distance():
        """
          This function computes the distance between the nose and the foot in order to
          then compute the distance between the person and the robot.
        """
        global full_detection
        nose = results.pose_landmarks.landmark[0]
        left_foot = results.pose_landmarks.landmark[31]
        right_foot = results.pose_landmarks.landmark[32]

        while full_detection == True:
            left_distance = math.dist(nose, left_foot)
            right_distance = math.dist(nose, right_foot)
            print(left_distance)
            print(right_distance)


def keep_distance():



def movement():
    if status == 'lay down' :

    if status == 'sit down' :

    if status == 'stand up' :
    

def main():
    global pub
    rospy.init_node('control', anonymous = True)
    pub = rospy.publisher('/cmd_vel', Twist, queue_size = 1)
    depth_sub = rospy.Subscriber("/spot/depth/frontleft/image", Image, self.depth_callback)
    rospy.spin()


if __name__ == '__main__':
    main()
