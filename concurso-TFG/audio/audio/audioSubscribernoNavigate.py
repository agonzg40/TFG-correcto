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

#Save the output of the program in the archive results
archive=open("src/concurso-TFG/output/results.txt","w")
counter = [0]

#Identify if is a source or a goal
def identify(data, verb, number):

    #Opening the archive with the places
    archiveAux = open("src/concurso-TFG/lexicon/places.txt","r")
    mensaje = archiveAux.read()

    aux = ""
    places = []
    j=0

    #Saving the places of the archive in array places
    for i in range(len(mensaje)):

        if(mensaje[i]!="\n"):
            aux += mensaje[i]
        else:
            places.append(aux)
            j+=1
            aux = ""

    dataAux = data
    copia = False

    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(dataAux)

    #See if the audio has two verbs
    if(number == 1):
        data = ""
        for word, tag in tagger.tag(tokens): 
            if(word != "and"):
                data += word
            elif (word == "and"):
                break

    #See if the audio has more than two verbs
    if(number == 2):
        data = ""
        for word, tag in tagger.tag(tokens): 
            if(copia == True):
                data += word + " "
            elif(word == "and" and copia == False):
                copia = True
            

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
    
    #See if the verb has places
    for word, tag in tagger.tag(tokens):
        if(word!=verb):
            aux.append(word)
            for i in range(len(places)):
                if(word == places[i]):
                    for j in range(len (aux)):
                        if(j > len(aux)-4):
                            aux2 += " " + aux[j]
                            coma = True

                    goal += "goal:" + aux2 + " "

    #See if the verb has objects
    for word, tag in tagger.tag(tokens):
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


#Add the goal with verbs that aren't of special type to single verbs
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

#Add the goal with verbs that are of special type
def identifyGoalComposed(data, verb):
    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    tokens = nltk.word_tokenize(data)

    goal = ""
    boolean = False

    #Seeing where is the goal
    for word, tag in tagger.tag(tokens):
        if(word == "and"):
            boolean = False
        if(boolean==True):
            goal += word + " "
        if(word==verb):
            boolean = True

    return goal
        

#Identify the beneficiary for verb bring
def identifyBeneficiary(data):

    #Open the archive pronouns
    archiveAux = open("src/concurso-TFG/lexicon/personal_pronouns.txt","r")
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
    
    #See to the beneficiary of the archive pronouns
    for word, tag in tagger.tag(tokens):
        for i in range(len(pronouns)):
            if(word==pronouns[i]):
                goal += "beneficiary: " + word

    return goal


class audioSubscribernoNavigate(Node):

    def __init__(self):
        super().__init__('audio_subscriber')

        #Create the token
        self.subscription = self.create_subscription(
            String,                                              
            'audio',
            self.listener_callbackS,
            10)
        self.subscription   

    def listener_callbackS(self, text):
        self.get_logger().info('I heard: "%s"' % text.data)

        counterAux = 0

        oration = ""

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
        tokens = nltk.word_tokenize(text.data)

        #Opening the archive with the verbs
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

        archiveAux.close()

        #Scooch the audio record to count the verbs
        for word, tag in tagger.tag(tokens):
            for i in range(len(mensajeFinal)):
                if(word == mensajeFinal[i]):
                    verb = word
                    counterAux += 1

        #If only appear one verb
        if(counterAux == 1):
            self.singleCommand(text.data, mensajeFinal)

        #If appear more than one verb
        elif(counterAux >= 2):
            self.composedCommand(text.data, mensajeFinal)

        #If dont appear verbs or bad recognition of the audio
        elif(counterAux == 0):
            counter[0] += 1
            data = "BAD_RECOGNITION"
            oration = "NO_INTERPRETATION"
        
            archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))


    def singleCommand(self, data, mensajeFinal):

        oration = ""

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
        tokens = nltk.word_tokenize(data)

        #Scooch the audio record to see what type of verb is it
        for word, tag in tagger.tag(tokens):
            for i in range(len(mensajeFinal)):
                if(word==mensajeFinal[i] and word != "search" and word != "take" and word != "get" and word != "grab" and word != "pick" and word != "put" and word != "place" and word != "bring"):
                    counter[0] += 1
                    oration = "MOTION(goal:"
                    oration += addGoal(data, mensajeFinal[i])
                    break

                elif (word == "search" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "SEARCHING("
                    oration += identify(data, mensajeFinal[i], 0)
                    break

                elif (word == "take" or word == "get" or word == "grab" or word == "pick" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "TAKING("
                    oration += identify(data, mensajeFinal[i], 0)
                    break

                elif (word == "place" or word == "put" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "PLACING("
                    oration += identify(data, mensajeFinal[i], 0)
                    break

                elif (word == "bring" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "BRINGING("
                    oration += identify(data, mensajeFinal[i], 0)
                    oration += identifyBeneficiary(data)
                    break


        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        oration += ")"


        #Writing the exit in the archive result
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))


    def composedCommand(self, data, mensajeFinal):

        i = 0
        oration = ""
        counterAux = 0

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
        tokens = nltk.word_tokenize(data)

        #Scooch the audio record to see what type of verbs has
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

                    oration += "SEARCHING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "take" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    oration += "TAKING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "place" or word == "put" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    oration += "PLACING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += ")"

                elif (word == "bring" and word==mensajeFinal[j]):
                    i += 1
                    counterAux += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    oration += "BRINGING("
                    oration += identify(data, mensajeFinal[j], i)
                    oration += identifyBeneficiary(data)
                    oration += ")"

        

        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

    


        
        
            
        

def main(args=None):
    
    rclpy.init(args=args)

    audio_subscriber = audioSubscribernoNavigate()

    rclpy.spin(audio_subscriber)

    audio_subscriber.destroy_node()
    rclpy.shutdown()
    archive.close()


if __name__ == '__main__':
    main()
