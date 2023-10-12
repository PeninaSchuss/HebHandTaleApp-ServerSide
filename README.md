# HebHandTaleApp-ServerSide
Translate (to any language) images of handwritten Hebrew words.

## Description
This project is a server side of a web application that translates images of handwritten Hebrew words to any language.
The server side is written in Python and uses Flask framework.

## The main components of the project
### This project contains 2 parts:
1) Image recognition process, Which is done in 3 steps:
    1) Cutting the word in the picture into letters.
    2) Identifying the letters by the VGG19 model.
    3) Finding similar words to the word that identified in the previous step.
2) Bringing a translation and audio of the translation. It is done by using 2 external apis:
    1) Rapid api - google translate: to receive a translation.
    2) EdenAi api - text to speech: to receive audio of the translation text.

## Explanation of the folders in the project
1) api_utils - contains the apis files.
2) components - contains the files that are used in the three steps of the image recognition process.
3) data - contains the data files.
4) dbs - contains the databases files.
5) evaluation - contains the files for the evaluation of the three steps of the image recognition process.
6) notebooks - contains the notebooks files, that were used to test the model and the other parts of the recognition process.
7) runners - contains the files that run each of the three steps of the image recognition process.
8) server_api - contains the file that run the server. this file constitutes the api of this project.
9) training - contains the files that were used to train the model.

## How to install the required libraries in the project
There is a pipfile that contains all the libraries that need to be installed in order to run the project.
Here are instructions on how to run this file to install the libraries in it:
https://www.jetbrains.com/help/pycharm/using-pipfile.html

## How to run the project
### If the second part of the project - translation and audio of a word - is used, the following steps must be taken:
1) Create an account in Rapid api and get a key for the Google Translate api. https://rapidapi.com/googlecloud/api/google-translate1/tutorials/how-to-use-the-google-translate-api-with-javascript
2) Paste the key in the appropriate place, in the file: google_translate_api.py under the folder: api_utils.
3) Create an account in EdenAi and get a key for the text to speech api. https://docs.edenai.co/reference/start-your-ai-journey-with-edenai
4) Paste the key in the appropriate place, in the file: edenAi_api.py under the folder: api_utils.
#### So far the instructions for using the translation.

### Instructions for running the project:
#### In order to use the functions found in the server_api.py file, you must run the Flask framework. This can be done in the following way:
##### On a Windows computer this can be done using the Windows PowerShell:
1) Open the Windows PowerShell.
2) Go to the folder where the project is located.
3) Run the following command: ```$env:FLASK_APP = "server_api.recognize_word"```
4) Run the following command: ```flask run```
5) Now the ip and port that flask is listening to, will be printed. (localhost). Usually the default printing is:
```* Running on http://127.0.0.1:5000```
##### For an operating system other than Windows, follow the instructions in the following link:
https://flask.palletsprojects.com/en/1.1.x/cli/

#### For Examples of using the functions found in the server_api.py file, see the file: server_api_examples.md under the folder: server_api.

#### In order to use this project with the interface - the web application itself, you must access the client-side project and apply the instructions found there in the README.
For the client-side project, see the following link:
https://github.com/MichalMeshi/HebHandTaleApp-ClientSide

