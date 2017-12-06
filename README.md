# Leaf LIMS

![Leaf LIMS logo](https://leaflims.github.io/img/logo.svg)

_Leaf LIMS is a laboratory information management system (LIMS) designed to make managing projects
in a laboratory much easier. By using Leaf LIMS you can keep track of almost everything in the
laboratory including samples, results data and even consumable levels._

Leaf LIMS uses [Docker](https://docker.com) to easily bundle all the necessary components into a single package. Setting it up is as simple as downloading the latest release, editing a few configuration files and then running a single command!

## Prerequisites

1. [Docker](https://www.docker.com/get-docker)
2. [Docker Compose](https://docs.docker.com/compose/install/)
3. Python 3
4. Some basic knowledge of terminal commands

## Quickstart deploying to Docker

This requires that you have a recent version of [Docker](https://docker.com) that includes
the docker-compose tool. You will also need Python 3 to run the installer and an SSL certificate
(self-signed works, see this
 [stackoverflow](https://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl question)
question for more details).

1. Download the [setup files](https://github.com/LeafLIMS/LeafLIMS/releases/latest) and unzip
   on the server you want to run Leaf LIMS on.
2. Run the installer: `./installer.py` and answer the questions. The administration password can
   be changed once the system has been created.
3. The installer will then start Leaf LIMS. Wait a minute for configuration to happen and then
   head to the web address you configured to login with the username `admin`.

For more information on options that can be set during deployment please see the documentation at
the [Leaf LIMS website](https://leaflims.github.io/docs).

## Manually configuring the system

The installer will automatically generate a .env file that is required for running the system in
Docker. If you would like to manually edit this file you can rename the env.template file to .env
and edit the values there.

If you run the installer after manually configuring values it will overwrite the values in
this file.

All configuration variables related to the running of the system are set using environmental
variables. For a list of these and the defaults please see the
[environmental variables](https://leaflims.github.io/docs/environmental-variables/) section.

You will also need to change the `frontend/config.json` file and replace the `localhost` in the
`"api_endpoint": "https://localhost/api/",` line to match your domain. You will also need to
change `crm_enabled` if you want to enable CRM.

### I don't think it worked!

By default the docker-compose command given tells docker to run it in the background. To check for any issues you can run `docker-compose -p leaflims up --build` which will show the startup process in the terminal window.

Leaf LIMS has been tested on Mac and Linux only, you are likely to encounter problems when running on Windows.

### Changing ports

**For advanced users only. This is usually not required unless you are running multiple instances/
sharing with another application**

By default the docker instance runs on ports 80 for the frontend and 8000 for the backend. You can
change these in the docker-compose.yml file by editing the port definition in the file. You only
need to change the first of the port numbers e.g. "80:80" becomes "85:80" as this is the external
facing port; The others are internal and changing them or any other port defined in a command
elsewhere will break the system.

## Upgrading Leaf LIMS

Upgrading is as simple as downloading the newest release, copying over the `.env` and `frontend/config.js` files then restarting (in the directory run: `docker-compose -p leaflims stop; docker-compose -p leaflims up --build -d`).

**If you have edited the docker-compose.yml file you will need to make those changes in the new one otherwise they will not be used**

## Bugs and contacting the developers

If you find (or suspect you have found) a bug please check that it has not already been submitted to our [issue tracker](https://github.com/LeafLIMS/LeafLIMS/issues) and if not, submit a bug report with as much detail as you can [here](https://github.com/LeafLIMS/LeafLIMS/issues).

For non-bug related enquiries you can contact the lead developer Thomas at [thomas.craig@liverpool.ac.uk](mailto:thomas.craig@liverpool.ac.uk).

## Support

Leaf LIMS is developed by a group of three major groups at universities in the UK: [GeneMill](https://genemill.liv.ac.uk) at the University of Liverpool, the [EGF](http://www.genomefoundry.org/) at Edinburgh University and the [Earlam Institute](http://www.earlham.ac.uk/). 

If you are interested in further supporting the project please get in touch with Thomas via email at [thomas.craig@liverpool.ac.uk](mailto:thomas.craig@liverpool.ac.uk).

## Licence

Leaf LIMS is open source under the MIT licence. You can access the source code in the following repositories: For the UI see [LIMS-Frontend](https://github.com/LeafLIMS/LIMS-Frontend) and for the API see [LIMS-Backend](https://github.com/LeafLIMS/LIMS-Backend).
