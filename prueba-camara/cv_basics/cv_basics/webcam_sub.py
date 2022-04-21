# Import the necessary libraries
from typing import Any
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import sys
from torch import hub # Hub contains other models like FasterRCNN

thres = 0.45 # Threshold to detect object

#cap = cv2.VideoCapture(0)

classFile = 'src/prueba-camara/cv_basics/cv_basics/coco.names'
with open(classFile,'rt') as f:
  classNames = f.read().rstrip('\n').split('\n')

configPath = 'src/prueba-camara/cv_basics/cv_basics/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'src/prueba-camara/cv_basics/cv_basics/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#while True:
      #success,img = cap.read()
      #classIds, confs, bbox = net.detect(img,confThreshold=thres)
      #print(classIds,bbox)
 
      #if len(classIds) != 0:
        #for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            #cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            #cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
            #cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            #cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
            #cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
     
    # Convert to grayscale
    #gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect the faces
    #faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw the rectangle around each face
    #for (x, y, w, h) in faces:
        #cv2.rectangle(current_frame, (x, y), (x+w, y+h), ((0, 255, 0)), 2)
        #cv2.addText(img=current_frame, text="Face", org=(x ,y), nameFont="Times", pointSize=15, color=(255, 0, 0))
    
    # Display image
      #cv2.imshow("camera", img)
    
      #cv2.waitKey(1)

#face_cascade = cv2.CascadeClassifier('src/prueba-camara/cv_basics/cv_basics/haarcascade_frontalface_default.xml')

 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      'video_frames', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    #self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)

    

    #while True:
      #success,img = data.read()
    classIds, confs, bbox = net.detect(current_frame,confThreshold=thres)
    print("eh", classIds,bbox)
 
    if len(classIds) != 0:
      for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
          cv2.rectangle(current_frame,box,color=(0,255,0),thickness=2)
          cv2.putText(current_frame,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
          cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
          cv2.putText(current_frame,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
          cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    
    # Display image
      cv2.imshow("camera", current_frame)
    
      cv2.waitKey(1)
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
