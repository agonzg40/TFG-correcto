import rclpy
import speech_recognition as sr
import sphinx
import pocketsphinx
from rclpy.node import Node

from std_msgs.msg import String

import stanfordnlp


class audioPublisher(Node):

    def __init__(self):
        super().__init__('audio_publisher')

        #Create of the token
        self.publisher_ = self.create_publisher(String, 'audio', 10) 
        self.SpeechToString()

    def prueba(self):

        #Opening the archive with the verbs
        archiveAux = open("lexicon/verbs.txt","r")
        mensaje = archiveAux.read()

        aux = ""
        mensajeFinal = []
        j=0

        #Reading the archive
        for i in range(len(mensaje)):

            if(mensaje[i]!="\n"):
                aux += mensaje[i]
            else:
                mensajeFinal.append(aux)
                j+=1
                aux = ""
                
        for i in range(0,j):
            print(mensajeFinal[i])
        archiveAux.close()


    def SpeechToString(self):
        rec = sr.Recognizer()
        seconds = 3

        #Open the microphone to hear the user
        with sr.Microphone() as source:

            print("Calibrating")
            rec.adjust_for_ambient_noise(source, duration=seconds)
            print("Set minimum energy threshold to " + str(rec.energy_threshold))

            print("Listening")
            audio = rec.listen(source, timeout=None, phrase_time_limit=None)

            text = rec.recognize_google(audio)
            
            print(text)

            msg = String()
            msg.data = text
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    audio_publisher = audioPublisher()
    audio_publisher.destroy_node()

    rclpy.shutdown()

    

    


if __name__ == '__main__':
    main()
