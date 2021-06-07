
#############################################
#      RUN THIS PROGRAM TO GET STARTED      #
#############################################

# Do things with JSON, files and dynamically importing functions.
import json, os

# Used for getting names from class.
from utils import parse_dict_properties

# Used for getting filepath input.
from tkinter import Tk
from tkinter.filedialog import askdirectory
Tk().withdraw() # Prevent TkInter from displaying root GUI.

# Used for loading external Python modules.
from utils import load_module

# Path globals.
ROOT_DIR = os.getcwd()
SETTINGS_PATH = f'{ROOT_DIR}/user_settings'

# F-string special char globals.
TAB = "\t"
NL = "\n"

def do_the_thing(settings_dict):
    """
    Template + Class data = Customised Document

    This function creates the Document.
    """

    # Initialise templates dictionary
    templates = {}

    # Get directories.
    settings = get_settings()
    TEMPLATES_DIR = settings["templates_dir"]
    DATA_DIR = settings["data_dir"]
    OUTPUT_DIR = settings["output_dir"]

    # Load all files into templates dictionary
    # Crawl through Templates dir and dynamically import functions. This allows user to add function files.
    for name in os.listdir(TEMPLATES_DIR):

        # Error checks
        if name == "__init__.py" or name == "__pycache__":
            continue

        path = f'{TEMPLATES_DIR}/{name}'

        module = load_module(name, path)

        # Check whether a function by the same name is in the Python script.
        func_name = name.split('.')[0] # Remove trailing `.py`
        if hasattr(module, func_name):
            
            templates[func_name] = getattr(module, func_name)

        else:

            print(f'<!> File name does not match name of function in "{name}"! Skipping.')
            input("Press any key to continue.")
            continue

    # Get Json information. Store in 'classes' dictionary.

    # 'classes' is an array that contains the data objects to format the templates.
    _classes = {}
    # default_dict is a dictionary which stores the default values of each json file (In case an entry has no template).
    default_dict = {}

    for file_name in os.listdir(DATA_DIR): # Assuming cwd == '/doc-gen'.        

        # Skip
        if file_name == "__init__.py":
            continue

        # Strip off the .json on end of file name.
        file_name_stripped = file_name.split('.')[0]

        # Load the raw JSON data into 'data'.
        with open(f'{DATA_DIR}/{file_name}') as f:
            try:
                data = json.load(f)
            except:
                print(f"<!> Bad JSON data in '{file_name}'! Skipping.")
                continue

            # Check if ENITRE json file is a dictionary (should be)
            # If it's a dictionary, extend onto our dictionary of classes i.e. dicts, init, lists, objects
            if isinstance(data, dict):

                # If not enabled, don't add it (but enabled by default).
                # Note: Deactivates entire Json File
                if "_enabled" in data and not data["_enabled"]:
                    continue

                # If there is a default value, put it in the default dictionary.
                if "_default" in data:
                    default_dict[file_name_stripped] = data.pop('_default')

                # Add parent value to each class in the data dictionary
                # This is done so that we know where the data has come from.
                # - Guaranteed you will come back to this and be confused - sorry, I tried my best to be readable
                for _cname in data:
                    # Add _parent to value list (data[_cname] is the value)
                    data[_cname]["_parent"] = file_name_stripped

                _classes.update(data)

    # Add class name permutations to _classes.
    # This way we only have to parse the class names once each.
    for _cname in _classes:
        _class = _classes[_cname]

        # The default template now comes at the start of the json file.
        # We cant parse names if it is the default template.
        if _cname == "_default":
            continue

        # Parse key-value case-structure permutations.
        # E.g. Sentence-case, lowercase, UPPER_CASE.
        _class = parse_dict_properties(_class)

        # Add "_name" key to dict, to auto-fill the class name.
        _class["_name"] = _cname

    # Now we have a list of classes and a dict of templates (And a dict of default values!).
    # By their powers combined, we can create anything... >:)
    for _cname in _classes:

        # Reset output_code
        output_code = ""

        # Refer to the correct class
        _class = _classes[_cname]

        # Get the value for the class
        _classvalue = _classes[_cname]

        if "_templates" in _classvalue:
            # Then use the template
            function_list = _classvalue["_templates"]

        else:

            # Find the parent of the class
            _parent_class = _classvalue["_parent"]

            if _parent_class in default_dict:
                # If parent is in the default list, use the default function list.
                function_list = default_dict[_parent_class]

            else:

                print(f'<!> No template was specified for {_class["_name"]}! Skipping.')
                continue

        # Debug space:
        """
        if (_cname == "render"):
            pause="here"
        """

        # Now, construct the code by going through the function_list and performing the functions
        # within it. It will do them in order that they are written in the "_default" or "_templates"
        # entry in the Json file.
        for function_name in function_list:

            if function_name not in templates:
                print(f'<!> Unknown template: \'{_class["_template"]}\' - skipping {_class["_name"]}!')
                continue

            # templates is the list of functions. Call the correct template function and
            # add it to output code.
            output_code += templates[function_name](_class, _classes)

        # Create filepath.
        filepath = f'{OUTPUT_DIR}/{_class["_filename"]}'

        # Write the formatted doc script to a new file at location.
        text_file = open(filepath, "w")
        text_file.write(output_code)
        text_file.close()

        # Log the update.
        print(f'\'{_class["_filename"]}\' ==> {filepath}.')

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
        settings_dict = get_settings()

        # MAIN MENU LOOP
        user_input = get_input("""~~~~~ What would you like to do? ~~~~~

Run:        'r'
Help:       'h'
Settings:   's'
Exit:       'e'

""")

        if user_input == "r": # Run
            do_the_thing(settings_dict)

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

        