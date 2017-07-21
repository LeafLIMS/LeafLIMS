# Leaf LIMS

![Leaf LIMS logo](https://leaflims.github.io/img/logo.svg)

_Leaf LIMS is a laboratory information management system (LIMS) designed to make managing projects
in a laboratory much easier. By using Leaf LIMS you can keep track of almost everything in the
laboratory including samples, results data and even consumable levels._

Leaf LIMS uses [Docker](https://docker.com) to easily bundle all the necessary components into a single package. Setting it up is as simple as downloading the latest release, editing a few configuration files and then running a single command!

## Prerequisites

1. [Docker](https://www.docker.com/get-docker)
2. [Docker Compose](https://docs.docker.com/compose/install/)
3. Some basic knowledge of terminal commands

## Deploying to Docker

1. [Download](https://github.com/LeafLIMS/LeafLIMS/releases/latest) the latest release of Leaf LIMS to the location you would like to run it and unzip.
2. Edit the `frontend/config.js` file, replacing "localhost" in `.constant('API_URL', 'https://localhost/api/')` with the URL of your system.
3. Edit the `.env` file to set the required configuration values as explained in the file. On Linux/Mac it will be hidden, open using a text editor such as nano or Vim.
4. Ensure your terminal is in the directory where the files are (`cd /directory`) and run `docker-compose -p leaflims up --build -d`
5. Be patient while the system starts up (this takes a few minutes as it ensures all components go up in the correct order)
6. Visit the URL that you specified instead of localhost and log in with the username `admin` and the password you set.

For more information on options that can be set during deployment please see the documentation at
the [Leaf LIMS website](https://leaflims.github.io).

### I don't think it worked!

By default the docker-compose command given tells docker to run it in the background. To check for any issues you can run `docker-compose -p leaflims up --build` which will show the startup process in the terminal window.

Leaf LIMS has been tested on Mac and Linux only, you are likely to encounter problems when running on Windows.

### Changing ports

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
