# UAV Log Viewer

![log seeking](preview.gif "Logo Title Text 1")

 This is a Javascript based log viewer for Mavlink telemetry and dataflash logs.
 [Live demo here](http://plot.ardupilot.org).

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

# Docker

``` bash

# Build Docker Image
docker build -t <your username>/uavlogviewer .

# Run Docker Image
docker run -p 8080:8080 -d <your username>/uavlogviewer

# View Running Containers
docker ps

# View Container Log
docker logs <container id>

# Navigate to localhost:8080 in your web browser

```

BACKEND

Open a new terminal and split it

Terminal 1 - In the main project directory (UAVLogViewer-master), Run the frontendusing the command "npm run dev"

Create a virtual python environment and activate it

Install all the dependent libraries using requirements.txt

Add the Open AI API Key in a .env file in the backend folder

Terminal 2 - In the second terminal, Open the backend directory using "cd .\backend\" and run the backend using the command "uvicorn main:app --reload"

Go to the browser and see the App in "http://localhost:8080/"

Working : 

Find the "log171.bin" attached in the sample data folder.

In the App, you can use this file to insert for processing in the placeholder "Drop *.tlog or *.bin file here or click to browse". 

After that, on the left bottom you can see the chat bot implemented. You ask questions to the chat bot based on the sample data using the following sample questions from Questions.txt.


