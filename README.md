# Leaf LIMS Docker deployment script

## Prerequisites

1. Docker
2. Docker Compose

## Deploying to Docker

1. Download the file to the server where you intend to deploy Leaf LIMS
2. Edit the `frontend/config.js` with the URL and port of server you are running the backend of the
   system on. By default this is port 8000.
3. Set the admin email and password in the `.env` file. Do not use spaces in the password otherwise
   it will not be correctly recognised. This password can be changed later.
4. Run `docker-compose up --build`
5. Enjoy your now running version of Leaf LIMS!

For more information on options that can be set during deployment please see the documentation at
the [Leaf LIMS website](https://leaflims.github.io).

## Changing ports

By default the docker instance runs on ports 80 for the frontend and 8000 for the backend. You can
change these in the docker-compose.yml file by editing the port definition in the file. You only
need to change the first of the port numbers e.g. "80:80" becomes "85:80" as this is the external
facing port; The others are internal and changing them or any other port defined in a command
elsewhere will break the system.
