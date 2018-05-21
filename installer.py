#!/usr/bin/env python3

import os
import argparse
import getpass
from collections import OrderedDict
import json
import subprocess

class colours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GREY = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Installer:

    def __init__(self, args):
        print(args)
        self.is_upgrade = args.upgrade
        self.settings_from_file = args.with_settings

        self.settings = OrderedDict()

    def input(self, prompt):
        return input(colours.BLUE + prompt + colours.ENDC)

    def input_default(self, prompt, default=""):
        prompt_string = "{prompt_c}{prompt}{end}{colour}({default}{end}) ".format(
                                                                            prompt_c=colours.BLUE,
                                                                            prompt=prompt,
                                                                            colour=colours.GREEN,
                                                                            default=default,
                                                                            end=colours.ENDC)
        result = input(prompt_string)
        if result == "":
            return default
        return result

    def initial_message(self):
        print(colours.GREEN + """
                                     ``...---::::----..``
                          ``-:/+ossyhhhhhhhhhhhhdddddddddhhyso+/:-``
                   ``-:+osyhhhhhhhhhhhhhhhhhhhhhhhhddddddddddddddddhyo+:.`
               `-/osyhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhddddddddddddddddddddhs+-`
           `-+oyyyyyyhhhhhhhhh+shhhhhhhhhhhhhhhyyhyyyyyyyhhdddddddddddddddhy+-
        `-+syyyyyyyyyyyhhhhhhh/.hhhhyyysoo+++oosssyyhhhhhdddddddddddddhy+-`     
      `:syyyyyyyyyyyyyyyyyhhhy``o+/::/+osyyhhhhhhhhhhhhhhhhhddddddhyo:`         
     -syyyyyy/yyyyyyyyyyyso+:-..--:/++osyyhhhhhhhhhhhhhhhhhhhhdhy+-`            
    /yyyyyyyy::yyyyyys+:--:+oyyhhhhhhyysoooyhhhhhhhhhhhhhhhhhy+-`               
   /yyyyyyyyy.-yys+:..:+syyyyyyyhhhhhhhhhhhyyhhhhhhhhhhhhhhs:`                  
  `syyyyyyyy/ //..-/oyyyyyyyyyyyyyyhhhhhhhhhhhhhhhhhhhhhy+.                     
  :yyyyyyys:  `-+syyyyyyyyyyyyyyyyyyyhhhhhhhhhhhhhhhhhs:`                       
  :ssyyys+.  `.::::::::///++osyyyyyyyyyhhhhhhhhhhhhy+.                          
  .ssss+. ./oosssssyyysssssoo++/+oyyyyyyyyhhhhhhyo:`  `  `       `   ````       
   os+. `/syyyyyyyyyyyyyyyyyyyyyyssyyyyyyyyyhyy+.    -s +s:    `+s:.+/::/+-     
   .:  :ssssyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyys/.y-     -y s/s:   o+s/s/    ..     
     `+sssssssyyyyyyyyyyyyyyyyyyyyyyyyyyo/.`  y-     -y s:.s- ++ s/-++//-.      
     `+sssssssssyyyyyyyyyyyyyyyyyyyso/-`      y-     -y s: .so+  s/  ``.-o+     
       ./osssssssssyyyyyyyyyyys+/:.`          y:`````:y s:  `.   s+o-`  `+o     
          `-:/+oooooooo++/:-.`                ///////-/ :.       :-`:////-      
                                                                                
                                                                                
""" + colours.ENDC)
        print("""This installer will help you set up Leaf LIMS. Before you continue
you will need the following:

    - An SSL certificate
    - A location to be used as a file store

Any selections made will not be written to a file until the end of the process,
quitting at any point will stop the process and no changes will be made.
""")

    def check_directory(self):
        # Check the required files exists: docker-compose.yml, frontend/config.json
        if os.path.exists('./docker-compose.yml') and \
           os.path.exists('./frontend/config.json'):
            pass
        else:
            print(colours.FAIL + """
You must be running this from the directory containing the installer.
Please cd to the directory and run the installer again.
""" + colours.ENDC)
            exit()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                data = f.read()
                self.settings = json.loads(data, object_pairs_hook=OrderedDict)
        except:
            print(colours.FAIL + "Could not load settings.json file!" + colours.ENDC)
            exit()

    def frontend_domain(self):
        print(colours.BOLD + '------------ Frontend Configuration ------------' + colours.ENDC)
        print("""
Please provide the domain on which the system is going to be accessable
e.g. example.org. Do not provide the protocol (http/https) or end with a
trailing slash (/).
""")
        self.settings['DOMAIN'] = self.input("Your domain (e.g. example.org): ")

    def required_environmental_variables(self):
        print(colours.BOLD + '\n------------ Backend Configuration ------------' + colours.ENDC)
        print(colours.BOLD + '------------ Required Settings ------------' + colours.ENDC)
        print("""
The following settings are required to run Leaf LIMS correctly. No default
options are set so you must ensure each setting is filled in.
""")

        self.settings['SETUP_ADMIN_EMAIL'] = self.input("Email address for admin account: ")
        prompt = colours.BLUE + "Password for the admin account: " + colours.ENDC
        self.settings['SETUP_ADMIN_PASSWORD'] = getpass.getpass(prompt=prompt)

        print("""
Leaf LIMS needs a location on the server to store uploaded files. Please provide
an absolute path to a directory you would like them stored (e.g. /var/files)
""")
        self.settings['FILE_STORE'] = self.input("Path to directory: ")

        print("""
Leaf LIMS only runs on a https enabled server. This requires the use of an
SSL certificate. There are two parts you will need: the .crt and .key files.
Please provide the path to the files below (e.g. /certificate/ssl.crt).
""")
        self.settings['CERT_LOCATION'] = self.input("Path to .crt file: ")
        self.settings['KEY_LOCATION'] = self.input("Path to .key file: ")

    def optional_environmental_variables(self):
        print(colours.BOLD + '\n------------ Optional Settings ------------' + colours.ENDC)
        print("""
The following settings are optional and all have defaults provided. Simply
press enter to accept the defaults.
""")

        self.settings['ORGANISATION_NAME'] = self.input_default("Organisation name: ", "Leaf LIMS")

        print("""
An identifier is automatically generated for any created project in Leaf LIMS.
You can set the prefix and the starting number below. Please be aware that
once set it is difficult to change these values.
""")

        self.settings['PROJECT_IDENTIFIER_PREFIX'] = \
                self.input_default("Project identifier prefix: ", "P")
        self.settings['PROJECT_IDENTIFIER_START'] = \
                self.input_default("Project identifier start: ", "100")

    def plugin_variables(self):
        print(colours.BOLD + '\n------------ Plugin Settings ------------' + colours.ENDC)
        print("""
The following settings are only required if you plan to use plugins with
Leaf LIMS. Press enter to accept the default if you don't need them.
""")
        self.settings['EXTERNAL_PLUGINS'] = \
                self.input_default("Directory containing plugins: ", "./plugins")

    def email_variables(self):
        print(colours.BOLD + '\n------------ Email Settings ------------' + colours.ENDC)
        print("""
Leaf LIMS can send emails alerting you to changes amoung other things.
The system requires a valid SMTP server that does not have to be installed
on the same server it is running. Common defaults are provided, please
alter these to suit your email service.
""")
        self.settings['EMAIL_HOST'] = self.input_default("Email host: ", "localhost")
        self.settings['EMAIL_PORT'] = self.input_default("Email host: ", "465")
        self.settings['EMAIL_HOST_PASSWORD'] = self.input_default("Email password: ", "")
        self.settings['EMAIL_HOST_USER'] = \
                self.input_default("Email user: ", "Leaf LIMS <leaflims@localhost>")
        self.settings['EMAIL_USE_SSL'] = self.input_default("Use SSL: ", "True")
        self.settings['EMAIL_FROM'] = self.input_default("Email from: ", "Leaf LIMS")

    def crm_variables(self):
        print(colours.BOLD + '\n------------ CRM Settings ------------' + colours.ENDC)
        print("""
Leaf LIMS can interface with a Salesforce CRM system to pull details out and
update projects. It is disabled by default as not everyone needs it. If you
do enable it you must make sure you have read the guide to using Salesforce
with Leaf LIMS.
""")

        self.settings['ENABLE_CRM'] = self.input_default("Enable CRM: ", "False")

        if self.settings['ENABLE_CRM'] == "True":
            self.settings['SALESFORCE_URL'] = self.input_default("Salesforce URL: ",
                                                                 "https://login.salesforce.com")
            self.settings['SALESFORCE_USERNAME'] = self.input("Salesforce username: ")
            self.settings['SALESFORCE_PASSWORD'] = self.input("Salesforce password: ")
            self.settings['SALESFORCE_TOKEN'] = self.input("Salesforce token: ")

    def confirm_settings(self):
        print(colours.BOLD + '\n------------ Confirm Settings ------------' + colours.ENDC)
        print("""
Please check over the following values that you have provided. If any are
incorrect you can change them by typing the number next to the setting
that needs changing. If they are correct press enter to continue.
""")
        for i, (key, value) in enumerate(self.settings.items()):
            if key == 'SETUP_ADMIN_PASSWORD':
                value = '******'
            print("{}. {} = {}".format(i, key, value))

        choice = self.input("Choose a number to correct or press enter to continue: ")
        if choice == "":
            pass
        else:
            self.edit_choice(choice)

    def edit_choice(self, choice):
        try:
            choice_as_number = int(choice)
            settings = list(self.settings.items())
            chosen_item = settings[choice_as_number]
            self.settings[chosen_item[0]] = self.input_default("Choose new value: ", chosen_item[1])
        except (IndexError, ValueError) as e:
            print(colours.FAIL + "Please pick a valid number." + colours.ENDC)
        self.confirm_settings()

    def write_settings(self):
        # Write settings to JSON file for later reading
        print(colours.GREEN + "Writing settings file..." + colours.ENDC)
        with open('settings.json', 'w+') as f:
            json_string = json.dumps(self.settings)
            f.write(json_string)

    def write_frontend_config(self):
        # Write out frontend config file
        print(colours.GREEN + "Writing config.json file..." + colours.ENDC)
        api_endpoint = 'https://{}/api/'.format(self.settings['DOMAIN'])
        with open('frontend/config.json', 'r') as f:
            data = f.read()
            as_json = json.loads(data)
        with open('frontend/config.json', 'w') as f:
            as_json['api_endpoint'] = api_endpoint
            if self.settings['ENABLE_CRM'] == 'True':
                as_json['crm_enabled'] = True
            else:
                as_json['crm_enabled'] = False
            json_string = json.dumps(as_json, indent=4)
            f.write(json_string)
        os.chmod('frontend/config.json', 0o775)

    def write_env_file(self):
        # write out the .env file
        print(colours.GREEN + "Writing .env file..." + colours.ENDC)
        required_settings = """
DB_NAME=postgres
DB_PASSWORD=
DB_USER=postgres
DB_HOST=db
DB_PORT=5432
"""
        env_string = ''
        for key, value in self.settings.items():
            env_string += key + '=' + value + '\n'
        env_string += required_settings
        with open('.env', 'w+') as f:
            f.write(env_string)

    def attempt_docker_start(self):
        # Using the completed files, try to start Leaf LIMS using docker
        print(colours.GREEN + "Attempting to start a Docker instance..." + colours.ENDC)
        results = subprocess.run(["docker-compose", "-p", "leaflims", "up", "--build", "-d"])
        if results.returncode != 0:
            print(colours.FAIL + "Docker instance failed to start!" + colours.ENDC)
        else:
            print(colours.GREEN + "Docker instance started successfully." + colours.ENDC)
        print(results)

    def run(self):
        self.initial_message()
        self.check_directory()
        if not self.settings_from_file:
            self.frontend_domain()
            self.required_environmental_variables()
            self.optional_environmental_variables()
            self.plugin_variables()
            self.email_variables()
            self.crm_variables()
        else:
            self.load_settings()
        self.confirm_settings()
        self.write_settings()
        self.write_frontend_config()
        self.write_env_file()
        self.attempt_docker_start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--upgrade', help="Upgrade an existing installation",
                        action='store_true')
    parser.add_argument('--with-settings', help="Use an existing settings.json file",
                        action='store_true')
    args = parser.parse_args()

    installer = Installer(args)
    installer.run()
