# Logic Flow

## About the application
Logic flow is a utility to be used for testing user segments on DaVita web applications. A segment is a user group definition that consists of various URLs, CTA interactions, and searches on the site that categorize a user into one group or another. For example: a user could qualify for an 'on dialysis' segment if they have filtered recipes by the 'dialysis' tag, have viewed educational materials regarding dialysis/late stage kidney disease, or clicked any CTA that indicates they are on dialysis.

The interface consists of a segment editor, and a logic runner. The segment editor is designed to allow analysts to add and delete segments, and edit which interaction they want to target on. All interactions are allowed to be assigned a weight, which serves as a multiplier on any strongly indicative interactions for a segment. Once different interactions have been added and saved, they can be run via the logic runner to see how the output has shifted given the updated segment definitions. On the logic runner page, analysts can either run the new logic against all users in their database dump, or run it against one particular user by selecting an ID from the dropdown. The logic runner's output allows analysts to look summary statistics, as well as each user individually to see what their top rated segments are, and which interactions they took to be classified in that segment.

## For Developers
The codebase has been structured so developers can run the application in a docker container, or via command line on your local host. If you do not have python 3+ on your machine, and would rather not hassle with downloading the needed software, I would recommmed leveraging the [docker run method](#Docker-Run-Steps). However, if you are in a situation where you have python and not docker, the [command line method](#Non-Docker-Steps) may be more suitable.


### Docker Run Steps
- Install Docker on your machine. [Download Here](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
- Clone this repository: https://github.com/Markweese/logic-flow.git
- cd into the root directory (logic-flow)
- add a database dump csv file to the app/data directory(contact Brandon D, or Mark B if you don't have one)
- from the root directory run the following command to build the docker image: `docker build . -t logic-flow`
- once the build is successful, run `docker run -p 5000:5000 -v <directory of your code (C:/Code/logic-flow for me)>:/app logic-flow`, or optionally `docker run -p 5000:5000 logic-flow` if you don't plan on editing code.
- visit your http://localhost:5000/, the tool should be live there

### Non-Docker Steps
- Ensure that you have python 3+ installed on your machine. [Download Here](https://www.python.org/downloads/release/python-392/)
- Clone this repository: https://github.com/Markweese/logic-flow.git
- cd into the root directory (logic-flow)
- add a database dump csv file to the app/data directory(contact Brandon D, or Mark B if you don't have one)
- Run `python app/app.py`
