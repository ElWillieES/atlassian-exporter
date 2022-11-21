# Atlassian Exporter

[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)

## Introducción

Atlassian Exporter es un proyecto desarrollado con Python y PyCharm, con el objetivo de poder descargar datos de **Atlassian Cloud**, como por ejemplo los datos de usuarios, grupos, licencias, y proyectos.

Estos datos pueden posteriormente importarse en una base de datos para su análisis, pudiendo utilizarse para diferentes propósitos, como el inventariado o el reparto de costes.

Este repo se ha creado para complementar el Post [Exportando datos de Atlassian Cloud con Python](https://elwillie.es/2022/11/09/xxx/) del Blog [El Willie - The Geeks invaders](https://elwillie.es)

Para la ejecución sobre MiniKube te puede interesar leer los Posts [Introducción a MiniKube e instalación en Windows 11](https://elwillie.es/2022/11/15/kubernetes-introduccion-a-minikube-e-instalacion-en-windows-11/) y [Administración fácil y rápida con K9s](https://elwillie.es/2022/11/15/kubernetes-administracion-facil-y-rapida-con-k9s/).


## Arquitectura de la Solución

Se trata de un simple programa Python que accede a la API de Atlassian Cloud, para poder descargar los datos que necesita, generando ficheros CSV que sean fáciles de importar, para su posterior análisis y tratamiento.

## Otros detalles de interés

Puedes apoyar mi trabajo haciendo "☆ Star" en el repo o nominarme a "GitHub Star". Gracias !!! 

[![GitHub Star](https://img.shields.io/badge/GitHub-Nominar_a_star-yellow?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://stars.github.com/nominate/)

Si te interesa aprender Python, tienes disponibles los siguientes [cursos gratuitos de Python en Edube - OpenEDG](https://edube.org/):

* Python Essentials 1
* Python Essentials 2
* Python Advanced 1 – OOP
* Python Advanced 2 – Best Practices and Standardization
* Python Advanced 3 – GUI Programming
* Python Advanced 4 – RESTful APIs
* Python Advanced 5 – File Processing

Otro recurso muy interesante es [Real Python](https://realpython.com/), donde podrás encontrar tutoriales, baterías de preguntas para ponerte a prueba (quizzes), etc.

Dentro de [Atlassian Cloud developer documentation](https://developer.atlassian.com/cloud/), tenemos varios enlaces de interés, incluyendo a la documentación de varias APIs de Atlassian Cloud como las siguientes:

* [Jira Cloud Platform - REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
* [Confluence Cloud - REST API](https://developer.atlassian.com/cloud/confluence/rest/v1/intro/)
* [Bitbucket Cloud - REST API](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)

En mi Blog personal ([El Willie - The Geeks invaders](https://elwillie.es)) y en mi perfil de GitHub, encontrarás más información sobre mi, y sobre los contenidos de tecnología que comparto con la comunidad.

[![Web](https://img.shields.io/badge/GitHub-ElWillieES-14a1f0?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/ElWillieES)

# Git

## Repositorio

Este repo se puede clonar desde GitHub utilizando este [enlace HTTP](https://github.com/ElWillieES/atlassian-exporter.git). 

A continuación se muestra el comando git clone usando SSH en lugar de HTTP.

```sh
git clone git@github.com:ElWillieES/atlassian-exporter.git
```

## Estructura de Ramas: Trunk Based Development (TBD)

* **Ramas permanentes**. Utilizaremos **master** como rama principal.
* **Ramas temporales o efímeras**. Utilizaremos **feature/xxx** (nueva característica) y/o **hotfix/xxx** (corregir un bug crítico urgente), que nacen de la rama principal y mezclan de nuevo sobre ella mediante Merge Request.
* **Gestión de Releases**. Para cada Release generaremos una etiqueta (tag) del tipo **release/a.b.c**.

En la descripción de las ramas de feature y hotfix, se especificará el ID de la tarea o issue asociada, por ejemplo:

```git
feature/3813
hotfix/2262
```

Si necesitáramos varias ramas para una misma tarea, añadiremos un número secuencial para evitar la colisión:

```git
feature/3813-1
feature/3813-2
```

## Commits Semanticos: icónos y prefijos

Como recomendación y buena práctica, el título para los Commits y de las Merge Request, pueden empezar con un icono y un prefijo, seguido de dos puntos y de un mensaje corto que comience por un verbo imperativo (ej: add, change, fix, remove, etc.). Por ejemplo:

```git
✨ feat(backend): add support for users having multiple suscriptions
```

Prefijos:

```git
feat: Nueva característica
fix: Corrección a un error
docs: Documentació
style: Cambios de formato (guía de estilo)
refactor: Renombrar una variable, simplificar un método, etc…
test: Añadir o modificar tests
chore: Rareas rutinarias, como modificar el .gitignore, etc…
```

Iconos:

```git
💄 Cosmetic
🎨 Improve format / structure
🛠/🐛 Fix
✨ Feature
🚑 Hotfix
📝 Doc
🚀 Release
♻ Refactor
🐳 Devops
☸ Kubernetes
🧪 Arquitectura de tests
✅ Añadir un Test
✔ Hacer que un test pase
💩 Ñapas
🏗 Architectural changes
🤡 Mocks
💚 Fixing Build
📈 Analiltycs
🌐 Localizations
😒 Chore
💫 Animations & Transitions
♿ Accesibility
🚧 Feature work in progress
🚀 Launch a new build
```

# Docker - Ejecución en local

## Con Docker

Se puede ejecutar la aplicación en local con Docker. 

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran cómo crear una imagen en local, listar las imágenes que tenemos disponible sen local, y cómo ejecutar un contenedor con nuestra imagen.

```shell
docker build -t atlassian-exporter .
docker images
docker run --rm atlassian-exporter
```

## Con Docker Compose

El siguiente comando ejecutado en la raíz del Proyecto, muestra cómo ejecutar nuestra aplicación con Docker Compose. 

```shell
docker-compose -f docker-compose.yml up --build -d
```


# Kubernetes - Ejecución en local (MiniKube)

Se puede ejecutar la aplicación en local con Kubernetes, si tienes instalado MiniKube.

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran cómo tagear la Imagen Docker para subirla al Registry local de MiniKube.

```shell
docker tag atlassian-exporter localhost:5000/atlassian-exporter
docker push localhost:5000/atlassian-exporter
```

Realizado esto, en la ventana Terminal de PyCharm, podemos ejecutar los siguientes comandos para aplicar los manifiestos en nuestro Cluster de MiniKube (namespace y Job), y consultar el Log de ejecución del Job que acabamos de crear y ejecutar (la salida del Log, será igual a cuando lo ejecutamos en Docker o directamente en PyCharm).

```shell
cd kube
kubectl apply -f ns-exporter.yml
kubectl apply -f job-atlassian-exporter.yml
kubectl logs job/atlassian-exporter -n exporter
```

Al finalizar podemos eliminar el namespace de Kubernetes, para eliminar todos los recursos y dejar "la casa limpia".

```shell
kubectl delete ns exporter
```


# Contactos

| Nombre        | Posición en el Proyecto         | Email                                                |
|---------------| ------------------------------- |------------------------------------------------------|
| **El Willie** | Product Owner                   | [elwillieES@gmail.com](mailto:elwillieES@gmail.com)  |
