import rclpy
import speech_recognition as sr
import sphinx
import pocketsphinx
from rclpy.node import Node

from std_msgs.msg import String

import stanfordnlp

keywords = [
    ("command", 1), 
    ("go", 0)
]


class audioPublisher(Node):

    def __init__(self):
        super().__init__('audio_publisher')
        self.publisher_ = self.create_publisher(String, 'audio', 10)     # CHANGE
        self.SpeechToString()
        #self.prueba()


    def prueba(self):

        archiveAux = open("lexicon/verbs.txt","r")
        mensaje = archiveAux.read()

        aux = ""
        mensajeFinal = []
        j=0

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

        '''tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(sentence)
        #print(tokens)
        #tagged = nltk.pos_tag(tokens)
        #print(tagged[0])

        #sent = ['Mitchell', 'decried', 'the', 'high', 'rate', 'of', 'unemployment']
        for word, tag in tagger.tag(tokens):
            if(tag == "VB"):
                print(word, '->', tag)
        

        #for word, tag in tagger.tag(sent):
            #print(word, '->', tag)
        

        #nlp = stanfordnlp.Pipeline()

        #cadena = "I am here to watch the tv"

        #doc= nlp(cadena)

        #print(doc[0])'''



    def SpeechToString(self):
        rec = sr.Recognizer()
        seconds = 3

        with sr.Microphone() as source:

            print("Calibrating")
            rec.adjust_for_ambient_noise(source, duration=seconds)
            print("Set minimum energy threshold to " + str(rec.energy_threshold))

            print("Listening")
            audio = rec.listen(source, timeout=None, phrase_time_limit=None)

            text = rec.recognize_google(audio)
            #text = rec.recognize_sphinx(audio, keyword_entries = keywords)
            print(text)

            msg = String()
            msg.data = text
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    audio_publisher = audioPublisher()
    audio_publisher.destroy_node()
    
    #rclpy.spin(audio_publisher)

    rclpy.shutdown()

    

    


if __name__ == '__main__':
    main()
