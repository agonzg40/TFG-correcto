Codigo hecho para la presentacion de un TFG, y un concurso europero de robotica.
Consta de dos partes, un reconocimiento de audio con navegacion y un reconocimiento de objetos.

#Manual de instalación

Prerrequisitos
Ubuntu 20.04:
https://ubuntu.com/download/desktop

Python 3.8.10 (mínimo):

	$sudo apt update
	$sudo apt install -y python3-pip

Ros-foxy:
Lo primero antes de nada es tener instalado ros2-foxy, para ello tenemos que ir esta página y seguir la instalación:
https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html

E instalar algunas dependencias:

	$sudo apt install python3-colcon-common-extensions
	$sudo apt install python3-pip

Instalación audio-navegación
Hay que descargar los archivos de los siguientes enlaces de github:
https://github.com/agonzg40/TFG-audio-navegacion
https://github.com/mgonzs13/ros2_rb1

Crear una carpeta llamada src dentro de una carpeta con el nombre que se prefiera,en mi caso le di el nombre de ros-foxy, y meter en la carpeta src creada previamente los archivos descargados.

Hay que instalar las dependencias con los comandos:

$sudo apt-get install python3-sphinx 	
$pip install stanfordnlp
$sudo pip install -U nltk
$pip install SpeechRecognition
$sudo apt install python3-sphinx
$sudo apt install pocketsphinx
$sudo apt-get install -y python3-pyaudio


Ejecución
Lo primero tenemos que buildear nuestro archivo, para ello tendremos que abrir una nueva terminal en la carpeta de ros-foxy.
Primero tendremos que sourcear para poder usar comandos de ros, para ello usamos el siguiente comando:

	$source /opt/ros/foxy/setup.bash

Ahora ya podremos buildear mediante el comando:
	
	$colcon build

Nos dará un error, pero nos quedará el siguiente sistema de carpetas:




Una vez hecho esto ya podremos ejecutar el código, para ello tendremos que abrir tres nuevos terminales en la carpeta de ros-foxy, es decir en el mismo sitio que buildeamops.

A continuación tendremos que instalar las dependencias, para ello instalaremos rosdep con los comandos:

	$sudo apt install python3-rosdep2
	$rosdep update

E instalaremos las dependencias del programa:

	$rosdep install --from-paths src --ignore-src -r -y

Y realizaremos de nuevo:

	$colcon build

Ahora realizamos primero el paso que hicimos para buildear, es decir el source en las tres terminales:

	$source /opt/ros/foxy/setup.bash

Y después de esto tendremos que realizar otro source de install, para ello lanzaremos el siguiente comando:

	$source install/setup.bash

Y ya podremos ejecutar el código, para ello en una de las dos terminales ejecutaremos primero el simulador:

	$ros2 launch rb1_gazebo granny.launch.py

Se nos abrirán dos ventanas, si la primera vez que lanzamos la ejecución rviz da algún error, cerrar los programas con Ctrl+c en la consola poner este comando, y volver a lanzar:

	$killall gzserver

Ahora en otra terminal lanzaremos 

	$ros2 run audio listener

Este será el nodo suscriptor que escuchará lo que publiquemos mediante nuestra voz en el topic.

Ahora tendremos que lanzar el nodo suscriptor, para ello tendremos que lanzar el siguiente comando en la otra terminal:

	$ros2 run audio talker

Este será el nodo que está escribiendo datos en el topic para que lo reciba el suscriptor, tendremos que esperar a que se calibre el audio, y cuando nos diga “Listening”, ya podremos hablarle.

Y ya podremos ver la oración analizada en el archivo de texto que se nos crea llamado output.txt

Y si le damos una orden que implique un “go”, es decir que vaya a algún lugar por ejemplo “go to the kitchen”, podremos ver en la ventana del simulador como el robot va hasta la localización que le hemos dicho

Instalación audio-sin-navegación
Hay que descargar el archivo del siguiente enlace de github:
https://github.com/agonzg40/TFG-audio-sin-navegar

Crear una carpeta llamada src dentro de una carpeta con el nombre que se prefiera,en mi caso le di el nombre de ros-foxy, y meter en la carpeta src creada previamente los archivos descargados.

Una vez hecho esto hay que instalar una serie de dependencias con los siguientes comandos:
$sudo apt-get install python3-sphinx 	
$pip install stanfordnlp
$sudo pip install -U nltk
$pip install SpeechRecognition
$sudo apt install python3-sphinx
$sudo apt install pocketsphinx
$sudo apt-get install -y python3-pyaudio

Ejecución
Lo primero tenemos que buildear nuestro archivo, para ello tendremos que abrir una nueva terminal en la carpeta de ros-foxy.

Primero tendremos que sourcear para poder usar comandos de ros, para ello usamos el siguiente comando:

	$source /opt/ros/foxy/setup.bash

Ahora ya podremos buildear mediante el comando:
	
	$colcon build

Y nos quedará el siguiente sistema de carpetas:



Una vez hecho esto ya podremos ejecutar el código, para ello tendremos que abrir dos nuevos terminales en la carpeta de ros, es decir en el mismo sitio que buildeamos:

Ahora realizamos primero el paso que hicimos para buildear, es decir el source:

	$source /opt/ros/foxy/setup.bash

Y después de esto tendremos que realizar otro source de install, para ello lanzaremos el siguiente comando:

	$source install/setup.bash

Y ya podremos ejecutar el código, para ello en una de las dos terminales ejecutaremos en nuestra terminal:

	$ros2 run audio listener

Este será el nodo suscriptor que escuchará lo que publiquemos mediante nuestra voz en el topic.

Ahora tendremos que lanzar el nodo suscriptor, para ello tendremos que lanzar el siguiente comando en la otra terminal:

	$ros2 run audio talker

Este será el nodo que está escribiendo datos en el topic para que lo reciba el suscriptor, tendremos que esperar a que se calibre el audio, y cuando nos diga “Listening”, ya podremos hablarle.

Y ya podremos ver la oración analizada en el archivo de texto que se nos crea llamado output.txt

Instalación reconocimiento de objetos
Hay que descargar el archivo del siguiente enlace de github:
https://github.com/agonzg40/TFG-object-recognition

Crear una carpeta llamada src dentro de una carpeta con el nombre que se prefiera,en mi caso le di el nombre de ros-foxy, y meter en la carpeta src creada previamente los archivos descargados.

Una vez hecho esto hay que instalar una serie de dependencias con los siguientes comandos:

	$sudo apt install python3-opencv
	$pip install --upgrade opencv-python

Ejecución
Lo primero tenemos que buildear nuestro archivo, para ello tendremos que abrir una nueva terminal en la carpeta de ros-foxy, es decir aquí:

Primero tendremos que sourcear para poder usar comandos de ros, para ello usamos el siguiente comando:

	$source /opt/ros/foxy/setup.bash

Ahora ya podremos buildear mediante el comando:
	
	$colcon build

Y nos quedará el siguiente sistema de carpetas:



Una vez hecho esto ya podremos ejecutar el código, para ello tendremos que abrir dos nuevos terminales en la carpeta de ros, es decir en el mismo sitio que buildeamos:

Ahora realizamos primero el paso que hicimos para buildear, es decir el source:

	$source /opt/ros/foxy/setup.bash

Y después de esto tendremos que realizar otro source de install, para ello lanzaremos el siguiente comando:

	$source install/setup.bash

Y ya podremos ejecutar el código, para ello en una de las dos terminales ejecutaremos en nuestra terminal:

	$ros2 run cv_basics img_publisher

Si nos da un mensaje de error de que no reconoce es porque no está reconociendo la cámara, ya sea porque no la tengamos conectada o apagada o porque tenemos más de una cámara.

Que este será el archivo que nos publicara lo que ve la cámara en tiempo real, en el caso de que tengamos más de una cámara, para que nos coja la imagen de la que queramos tendremos que editar el siguiente código en el archivo de webcam_pub.py:



En el que editaremos el 0, aumentando de 1 en 1 los valores hasta que encontremos la cámara deseada.

Ahora tendremos que lanzar el nodo suscriptor, para ello tendremos que lanzar el siguiente comando en la otra terminal:

	$ros2 run cv_basics img_subscriber

Este será el nodo que está recibiendo las imágenes de la cámara y realizará las operaciones para reconocer los objetos, se nos abrirá una nueva pestaña con lo que está viendo la cámara, y automáticamente empezará a reconocer los objetos.

Instalación audio con navegación y reconocimiento de objetos
Hay que descargar los archivos de los siguientes enlaces de github:
https://github.com/agonzg40/TFG-correcto
https://github.com/mgonzs13/ros2_rb1

Crear una carpeta llamada src dentro de una carpeta con el nombre que se prefiera,en mi caso le di el nombre de ros-foxy, y meter en la carpeta src creada previamente los archivos descargados.


Una vez hecho esto hay que instalar una serie de dependencias con los siguientes comandos:

Ejecución
Seguir los pasos de ejecución de los puntos anteriores dependiendo que se quiere ejecutar
