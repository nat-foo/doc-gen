
#############################################
#      RUN THIS PROGRAM TO GET STARTED      #
#############################################

# Do things with JSON, files and dynamically importing template_names.
import os

# Used for getting names from documents.
from utils import parse_dict_properties

# Used for getting filepath input.
from tkinter import Tk
from tkinter.filedialog import askdirectory
Tk().withdraw() # Prevent TkInter from displaying root GUI.

# Used for loading external Python modules.
from utils import load_modules, load_data

# Path globals.
ROOT_DIR = os.getcwd()
SETTINGS_PATH = f'{ROOT_DIR}/user_settings'

# F-string special char globals.
TAB = "\t"
NL = "\n"

def do_the_thing(settings):
    """
    Template + JSON data = Customised document

    This function creates the document.
    """

    # Get directories from settings.
    TEMPLATES_DIR = settings["templates_dir"]
    DATA_DIR = settings["data_dir"]
    OUTPUT_DIR = settings["output_dir"]

    # Load templates from directory.
    templates = load_modules(TEMPLATES_DIR)

    # Load data from directory.
    data, defaults = load_data(DATA_DIR)

    # Add item name permutations to data.
    # This way we only have to parse the item names once each.
    for item_name in data:
        item = data[item_name]

        # The default template now comes at the start of the json file.
        # We cant parse names if it is the default template.
        if item_name == "_default":
            continue

        # Parse key-value case-structure permutations.
        # E.g. Sentence-case, lowercase, UPPER_CASE.
        item = parse_dict_properties(item)

        # Add "_name" key to dict, to auto-fill the item name.
        item["_name"] = item_name

    # Now we have a list of data and a dict of templates (And a dict of default values!).
    # By their powers combined, we can create anything... >:)
    for item_name in data:

        item = data[item_name]
        document_text = ""

        # Use either specific or default templates.
        if "_templates" in item:
            template_names = item["_templates"]

        else:
            item_type = item["_type"]
            if item_type in defaults:
                # If parent is in the default list, use the default list.
                template_names = defaults[item_type]

            else:
                # Print quiet error.
                print(f'<!> No template was specified for {item["_name"]}! Skipping.')
                continue

        # Debug space:
        """
        if (item_name == "render"):
            pause="here"
        """

        # Now, construct the code by going through the template_names and performing the template
        # within it. It will do them in the order they are written in the "_default" or "_templates"
        # entry in the Json file.
        for template_name in template_names:

            if template_name not in templates:
                print(f'<!> Unknown template: \'{template_name}\' - skipping {item["_name"]}!')
                continue

            # Pass the item, the data, and the settings into the template.
            template = templates[template_name]
            document_text += template(item=item, data=data, settings=settings)

        # Create filepath.
        filepath = f'{OUTPUT_DIR}/{item["_filename"]}'

        # Write the generated document to a new file in the output dir.
        text_file = open(filepath, "w")
        text_file.write(document_text)
        text_file.close()

        # Log the update.
        print(f'\'{item["_filename"]}\' ==> {filepath}.')

    print("FINISHED.")

def get_input(message):
    """
    Get input from the user in lowercase.
    """
    return input(message).lower()

def get_settings():
    """
    This function reads user_settings and adds them to a dictionary.
    """

    if "user_settings" not in os.listdir(ROOT_DIR):

        # Create a settings file at location.
        text_file = open(SETTINGS_PATH, "w")
        text_file.write(f"""templates_dir: {ROOT_DIR}/input/templates
data_dir: {ROOT_DIR}/input/data
output_dir: {ROOT_DIR}/output""")
        text_file.close()

    settings_dict = {}

    # Open user settings txt file to read
    with open(SETTINGS_PATH) as f:

        text = f.readlines()

        # Go through text settings and add them to a dictionary.
        for line in text:
            line = line.strip().split(": ") # Mimics shallow JSON structure
            settings_dict[line[0]] = line[1]

    return settings_dict

def set_settings(setting, value):
    """
    This function writes settings to the user_settings txt file
    """

    # Read from txt file
    settings_dict = get_settings()

    if setting in settings_dict.keys():

        output_txt = ""

        # Update the passed in settings dict, 
        settings_dict[setting] = value

        # Then save those updates to 'user_settings'.txt
        for line in settings_dict:
            output_txt += f'{line}: {settings_dict[line]}{NL}'

        # Write new dictionary to file.
        text_file = open(SETTINGS_PATH, "w")
        text_file.write(output_txt)
        text_file.close()

    else:

        print("Setting not found.")

def user_input_setting(setting, message, options=[]):
    """
    This function prompts user input and changes the settings appropriately.
    """

    user_input = ""

    # Wait for user input to match one of the avail. options.
    while user_input not in options:
        user_input = get_input("\n" + message + "\n")
        if len(options) == 0:
            # If no options provided, accept anything.
            break

    # Once user_input in options, update the setting.
    set_settings(setting, user_input)

def user_dirpath_setting(setting):
    """
    This function prompts the user to select a directory and changes the settings appropriately.
    Doesn't do anything if no dir is selected.
    """

    user_input = ""

    # Wait for the user to select the directory
    user_input = askdirectory()
    if user_input == "":
        return

    # Update the setting.
    set_settings(setting, user_input)

def run_menu():

    print("""Welcome to DocGen.

This program was written for Aether to quickly edit an API on the fly.

But it can be used for any kind of documents - legal, marketing, cover letters, whatever. Your creativity's the limit.

This generator takes a JSON File and a Python template, and combines them together to create your desired documents.
""")

    # Menu System
    while True:

        # Get the settings from 'user_settings.txt'. Refresh each loop cycle.
        settings = get_settings()

        # MAIN MENU LOOP
        user_input = get_input("""~~~~~ What would you like to do? ~~~~~

Run:        'r'
Help:       'h'
Settings:   's'
Exit:       'e'

""")

        if user_input == "r": # Run
            do_the_thing(settings)

        elif user_input == "h":

            # Help message to console
            readme = open("./README.md")
            readme_str = readme.read()
            print(readme_str)
            readme.close

        elif user_input == "s":
            # Settings menu
            user_input = ""
            options = {
                "t": {
                    "message": "Where would you like to load templates from?",
                    "name": "templates_dir",
                    "func": user_dirpath_setting
                },
                "d": {
                    "message": "Where would you like to load data from?",
                    "name": "data_dir",
                    "func": user_dirpath_setting
                },
                "o": {
                    "message": "Where would you like to save the output to?",
                    "name": "output_dir",
                    "func": user_dirpath_setting
                },
                "e": {
                    "message": "Return to menu."
                }
            }

            while user_input not in options.keys():
                title = f"~~~~~ Which setting would you like to change? ~~~~~{NL*2}"
                msg = title
                for key in options:
                    option = options[key]
                    sp = len(title) - len(option["message"]) # Just enough spaces to right-align the key.
                    msg += f"{option['message']}{' '*sp}'{key}'{NL}"
                    # E.g. Where would you like to load templates from?    't'
                user_input = get_input(msg)
            
            # User pressed one of the options:
            option = options[user_input]
            if "func" in option:
                option["func"](option["name"])

        elif user_input == "e":
            break

    # Exit message
    print("Many thanks for using DocGen.")

if __name__ == "__main__":

    run_menu()

        