# Steps to run locally
- Install Docker on your machine
- clone this repository
- cd into the root directory (logic-flow)
- add a database dump csv file to the app/data directory(contact Brandon D, or Mark B if you don't have one)
- from the root directory run the following command to build the docker image: `docker build . -t logic-flow`
- once the build is successful, run `docker run -p 5000:5000 -v <directory of your code (C:/Code/logic-flow for me)>:/app logic-flow`, or optionally `docker run -p 5000:5000 logic-flow` if you don't plan on editing code.
- visit your http://localhost:5000/, the tool should be live there
