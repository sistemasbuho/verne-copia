# Verne 2.0
Verne es una plataforma de Ideas para la mejora de procesos internos en las empresas, además esta creada con sofware libre y con licencia (MIT) para su distribución comercial.


### Librerías
Estas son las librerías usadas para la construcción de Verne 2.0

| Librería | Versión |
| ------ | ------ |
| boto3 | 1.10.43 |
| Django | 2.2.10 |
| django-allauth | 0.39.1 |
| django-betterforms | 1.2 |
| django-bootstrap4 | 1.0.1 |
| django-debug-toolbar | 2.2 |
| django-extensions | 2.2.9 |
| django-filter | 2.2.0 |
| django-import-export | 1.2.0 |
| django-simple-history | 2.7.3 |
| django-widget-tweaks | 1.4.6 |
| Pillow | 7.1.1 |

### Herramientas adicionales
* [Admin LTE 3 ] - A beautiful template 
* [Javascript] - Used in plugins dinamically
* [Bootstrap] - Great UI boilerplate for modern web apps
* [Django] - For the backend
* [Google Oauth] - For login to app
* [jQuery] - duh

### Instalación 🚀

Verne 2.0 requiere de  [Django](https://docs.djangoproject.com/en/2.2/releases/2.2.8/) v2.2.10 + para su correcta ejecución.
Ingresa al entorno virtual llamado "env_verne" o instala las librerías del archivo "requeriments.txt"

```sh
$ cd verne2.0
$ cd env_verne
$ source bin/activate
```

O con el archivo "requeriments.txt"

```sh
$ pip3 install -r requeriments.txt
```
Una vez configuradas los requerimientos, se ejecuta el proyecto


### En ejecución

Una vez arrancado en proyecto es necesario entrar al administrador de Django e ingresar los datos predefinidos de la plataforma, que son los siguientes: 

**Credenciales de Google** 
  - Se debe ingresar a "Sites" e ingresar el nombre de dominio y el nombre a mostrar, luego ingresar a "Social Applications" e insertar el nombre del proyecto, el key token y el secret key token, y el sitio agreagado anteriormente. (Para ver las credenciales ver el archivo keys.txt)

**Datos predefinidos módulo Ideas**
    - Luego de ingresar las credenciales de google, ingresar al a "Question_phases" que son las preguntas pàra cambiar de la fase 1 a la fase 2.
    - Ingresar a "Phases" e insertar cada una de las 6 fases de las ideas en Verne 2.0 
    - Ingresar a "Objectives" y agregar los objetivos relacionados al registro de las Ideas

**Datos predefinidos módulo Reunión**
    - Como observación, para agendar reuniones es necesario tener registros en la tabla "Committe" puesto que sin usuarios en el comité no habría reunión

**Datos predefinidos módulo Premios**
    - Ingresar a la tabla "Prizes" e ingresar los premios actuales con sus respectivas leguas

  ##### Revisar el archivo data.txt para conocer cada dato a insertar
