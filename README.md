# Proyecto 01 Modelado y Programacion
> Chat utilizando sockets

Proyecto 01 Un chat simple con interfaz grafica que utiliza sockets para manejar la comunicacion servidor-cliente

## Como ejecutar el programa

Antes que nada es necesario clonar el repositorio

```shell
git clone
```

Primero es necesario verificar la dependencia con tkinter
Tkinter viene por omision en la mayoria de las distribuciones de python3 en caso de no tenerlo usar el siguiente comando
o su equivalente para la distribucion de unix adecuada:

```shell
  sudo apt-get install python3-tk
```

Una vez instalado tkinter usar los siguientes comandos
```shell
python3 Server.py <puerto>
```
Esto ejecuta el servidor especificado en <puerto>

```shell
python3 GuiClient.py <host> <port>
```
Esto ejecuta la vista en la interfaz grafica del cliente conectando en automatico
<host> es la direccion ip del servidor y <port> el puerto donde se ejecuta el servidor

## Bugs/Errores conocidos

La siguiente es una lista de errores conocidos con el cliente/servidor
* Ctrl+C no termina de manera limpia el servidor
* La caja de texto en la interfaz grafica no se desplaza de manera automatica, pero es posible desplazarla manualmente
* Los colores en el combo box de seleccion de evento son incorrectos, por lo que el texto no se muestra hasta poner el mouse sobre una linea

## Extensiones al protocolo

Esta es una lista de funcionalidad extra agregada al protocolo, no afecta la funcionalidad del protocolo duplicado
* Los usuarios tienen una cuenta de los mensajes invalidos enviados, puede ser usado para silenciar usuarios
* El servidor manda eventos de tipo MESSAGE, PUBLICMESSAGE y ROOMESSAGE con la finalidad de diferenciarlos en la GUI
* El servidor avisa a todos los usuarios cuando alguien se conecta o desconecta
* Los mensajes del servidor vienen prefijos con el usuario "[Servidor]"

#### Guia de uso

Una vez iniciado el servidor y despues concatado el cliente unicamente es necesario seleccionar el evento del combo box
ubicado en la esquina inferior izquierda para seleccionar el evento y escribir el mensaje a enviar. Despues presionar
la tecla enter para enviarlo.

Los eventos que solo requieren de una palabra como USERS o DISCONNECT se escogen en la combo box y despues se presiona la
tecla enter sin escribir nada en la caja de texto

Para el resto de los eventos es necesario escribir todos los argumentos dentro de la caja de texto


## Licensing

This project is licensed under the MIT License - see the LICENSE.md file for details
