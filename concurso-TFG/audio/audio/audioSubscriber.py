from re import T
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import sphinx

from std_msgs.msg import String

import stanfordnlp
import nltk


from nltk.corpus import brown
from nltk.tag import UnigramTagger

from geometry_msgs.msg import PoseStamped

#from robot_navigator import BasicNavigator

archive=open("src/concurso-TFG/output/results.txt","w")
counter = [0]

#Identify if is a source or a goal
def identify(data, verb, number):

    archiveAux = open("src/concurso-TFG/lexicon/places.txt","r")
    mensaje = archiveAux.read()

    aux = ""
    places = []
    j=0

    for i in range(len(mensaje)):

        if(mensaje[i]!="\n"):
            aux += mensaje[i]
        else:
            places.append(aux)
            j+=1
            aux = ""

    dataAux = data
    data = ""
    copia = False

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(dataAux)

    if(number == 1):
        for word, tag in tagger.tag(tokens): 
            if(word != "and"):
                data += word
            elif (word == "and"):
                break

    if(number == 2):
        print("hola")
        for word, tag in tagger.tag(tokens): 
            if(copia == True):
                data += word + " "
            elif(word == "and" and copia == False):
                copia = True
            
    print("eeee ", data)

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    goal = ""
    aux = []
    aux2 = ""
    aux3 = ""
    boolean = False
    coma = False
    last = False
    next = False
    
    for word, tag in tagger.tag(tokens): #Busco si se encuentra en el archivo de places
        if(word!=verb):
            aux.append(word)
            for i in range(len(places)):
                if(word == places[i]):
                    for j in range(len (aux)):
                        if(j > len(aux)-4):
                            aux2 += " " + aux[j]
                            coma = True

                    goal += "goal:" + aux2 + " "

    #goal += aux3

    for word, tag in tagger.tag(tokens): #Busco si se encuentra en el archivo de places para saber si es objeto
        if(word!=verb):
            if(next == True):
                    goal += word + " "
                    next = False
                    last = False
            if(last == True and word == "of"):
                    goal += word + " "
                    next = True
            if(boolean == True and last == False):
                for i in range(len(places)):
                    if(word == places[i]):
                        boolean = False
                
                if(boolean == True):
                    if(coma == True):
                        goal += ", "
                    goal += "theme: the " + word +" "
                    boolean = False
                    last = True

            

            if(word == "the"):
                boolean = True

            

    return goal

def addGoal(data, verb):

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    goal = ""
    
    for word, tag in tagger.tag(tokens):
        if(word!=verb):
            goal += word
            goal += " "

    goal = goal[:-1]
    return goal

def identifyGoalComposed(data, verb):
    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    goal = ""
    boolean = False

    print(verb)
    for word, tag in tagger.tag(tokens):
        if(word == "and"):
            boolean = False
        if(boolean==True):
            goal += word + " "
        if(word==verb):
            boolean = True

    return goal
        


def identifyBeneficiary(data):

    archiveAux = open("lexicon/personal_prononouns.txt","r")
    mensaje = archiveAux.read()

    aux = ""
    pronouns = []
    j=0

    for i in range(len(mensaje)):

        if(mensaje[i]!="\n"):
            aux += mensaje[i]
        else:
            pronouns.append(aux)
            j+=1
            aux = ""

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    goal = ""
    
    for word, tag in tagger.tag(tokens):
        for i in range(len(pronouns)):
            if(word==pronouns[i]):
                goal += "beneficiary: " + word

    return goal

def navigate(verb):
    
    print(verb)

    future = action_client.send_goal(10)

    rclpy.spin_until_future_complete(action_client, future)

    navigator = BasicNavigator()

    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'

    navigator.waitUntilNav2Active()



'''def addPlace(places):

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    place = ""
    
    for word, tag in tagger.tag(tokens):
        if(word!=verb):
            place += word
            place += " "

    place = place[:-1]
    return place'''



class audioSubscriber(Node):

    def __init__(self):
        super().__init__('audio_subscriber')

        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

        self.subscription = self.create_subscription(
            String,                                              # CHANGE
            'audio',
            self.listener_callbackS,
            10)
        self.subscription    

    def listener_callbackS(self, text):
        self.get_logger().info('I heardsad: "%s"' % text.data)

        counterAux = 0

        oration = ""

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(text.data)

        archiveAux = open("src/concurso-TFG/lexicon/verbs.txt","r")
        mensaje = archiveAux.read()

        aux = ""
        mensajeFinal = []
        j=0

        verb = ""

        for i in range(len(mensaje)):

            if(mensaje[i]!="\n"):
                aux += mensaje[i]
            else:
                mensajeFinal.append(aux)
                j+=1
                aux = ""
                
        '''for i in range(0,j):
            print(mensajeFinal[i])'''
        archiveAux.close()

        for word, tag in tagger.tag(tokens):
            for i in range(len(mensajeFinal)):
                if(word == mensajeFinal[i]):
                    verb = word
                    print(word)
                    counterAux += 1

        if(counterAux == 1):
            self.singleCommand(text.data, mensajeFinal)

        elif(counterAux >= 2):
            self.composedCommand(text.data, mensajeFinal)
            #LLamo al comando compuesto

        elif(counterAux == 0):
            counter[0] += 1
            data = "BAD_RECOGNITION"
            oration = "NO_INTERPRETATION"
        
            archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))
        
        
        navigate(verb)
	
        #print(tokens)
        #tagged = nltk.pos_tag(tokens)
        #print(tagged[0])

        #sent = ['Mitchell', 'decried', 'the', 'high', 'rate', 'of', 'unemployment']
        

        #for word, tag in tagger.tag(sent):
            #print(word, '->', tag)'''

    
    def singleCommand(self, data, mensajeFinal):

        oration = ""

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)

        for word, tag in tagger.tag(tokens):

            for i in range(len(mensajeFinal)):
            
                if(word==mensajeFinal[i] and word != "search" and word != "take" and word != "get" and word != "grab" and word != "pick" and word != "put" and word != "place" and word != "bring"):
                    counter[0] += 1
                    oration = "MOTION(goal:"
                    oration += addGoal(data, mensajeFinal[i])
                    
                elif (word == "search" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "SEARCHING("
                    oration += identify(data, mensajeFinal[i], 0)

                elif (word == "take" or word == "get" or word == "grab" or word == "pick" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "TAKING("
                    oration += identify(data, mensajeFinal[i], 0)

                elif (word == "place" or word == "put" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "PLACING("
                    oration += identify(data, mensajeFinal[i], 0)

                elif (word == "bring" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "BRINGING("
                    oration += identify(data, mensajeFinal[i])
                    oration += identifyBeneficiary(data)


        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        oration += ")"
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

    def composedCommand(self, data, mensajeFinal):

        i = 0
        oration = ""
        counterAux = 0

        print(data)

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)
        print(tokens)

        for word, tag in tagger.tag(tokens):
            
            for j in range(len(mensajeFinal)):
            
                if(word==mensajeFinal[j] and word != "search" and word != "take" and word != "put" and word != "place" and word != "bring"):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    if(counterAux == 1):
                        oration += "MOTION(goal: "
                        oration += identifyGoalComposed(data, mensajeFinal[j])
                        oration += ")"

                    elif(counterAux==2):
                        oration += "MOTION(, goal: "
                        oration += addGoal(data, mensajeFinal[j])
                        oration += ")"
                
                    

                elif (word == "search" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "SEARCHING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "take" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "TAKING("
                    print(i)
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "place" or word == "put" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "PLACING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "bring" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "BRINGING("
                    oration += identify(data, mensajeFinal[j])
                    oration += identifyBeneficiary(data)
                    oration += ")"

        

        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

    


        
        
            
        

def main(args=None):
    
    rclpy.init(args=args)

    audio_subscriber = audioSubscriber()
    action_client = audioSubscriber()
    

    rclpy.spin(audio_subscriber)

    audio_subscriber.destroy_node()
    rclpy.shutdown()
    archive.close()


if __name__ == '__main__':
    main()
