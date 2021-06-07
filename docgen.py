
#############################################
# README : Run this program to get started. #
#############################################

# Do things with JSON, files and dynamically importing functions.
import json, os, importlib

# Used for getting names from class.
from utils import parse_dict_properties

# Define filepath constants.
ROOT_FOLDER = os.getcwd() + "/"
INPUT_FOLDER = ROOT_FOLDER + "input"
TEMPLATES_FOLDER = ROOT_FOLDER + "templates"
OUTPUT_FOLDER = ROOT_FOLDER + "output"

# Initialise templates dictionary
templates = {}

# Load all files into templates dictionary
# Crawl through Templates folder and dynamically import functions. This allows user to add function files.
### !todo MAKE THIS RECURSIVELY GO THROUGH ALL FOLDERS
# Note that This is done in global scope
for file_name in os.listdir(TEMPLATES_FOLDER): # Assuming cwd == 'doc-gen/'.

    # Error checks
    if file_name == "__init__.py" or file_name == "__pycache__":
        continue

    ### if file_name is a directory:
    ### run recursive function
    # !todo - this broke when I had a folder at `general/__pycache__`.
    # Pycache is gitignored so 'general' stayed, but this loop doesn't know how to handle directories.
    # Instead of fixing the problem, I just deleted the directory :)

    ### DEF ()
    # Strip off the .py on end of file name - not required for import lib.
    file_name_stripped = file_name.split('.')[0]

    template_string = 'templates.' + file_name_stripped

    # Import programmatically with importlib.
    module = importlib.import_module(template_string)
    ### Return module (for scope purposes)

    # Add entry to templates dictionary. Getattr takes a function from an object using a string (an f-string here)
    # We want the form:
    #           "actor_exception": actor_exception,
    #                 str              function
    # Use module that is returned by function

    # Returns a Boolean - checking whether the function is in the file.
    if hasattr(module, file_name_stripped):
        
        templates[file_name_stripped] = getattr(module, file_name_stripped)

    else:

        print(f'<!> File name does not match name of function in "{file_name_stripped}"! Skipping.')
        input("Press any key to continue.")
        continue

def do_the_thing(settings_dict):
    """
    Template + Class data = Customised Document

    This function creates the Document.
    """

    # Get Json information. Store in 'classes' dictionary.

    # 'classes' is an array that contains the data objects to format the templates.
    _classes = {}
    # default_dict is a dictionary which stores the default values of each json file (In case an entry has no template).
    default_dict = {}

    for file_name in os.listdir(INPUT_FOLDER): # Assuming cwd == '/doc-gen'.        

        # Skip
        if file_name == "__init__.py":
            continue

        # Strip off the .json on end of file name.
        file_name_stripped = file_name.split('.')[0]

        # Load the raw JSON data into 'data'.
        with open(f'{INPUT_FOLDER}/{file_name}') as f:
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
        filepath = f'{OUTPUT_FOLDER}/{_class["_filename"]}'

        if "output" not in os.listdir():
          os.mkdir("output")

        if settings_dict["create_files"] == 'y':

            # If the writing lock is on, then we can create a new directory.

            # Write the formatted doc script to a new file at location.
            text_file = open(filepath, "w")
            text_file.write(output_code)
            text_file.close()

            # Log that bad boy.
            print(f'\'{_class["_filename"]}\' ==> {filepath}.')

        elif settings_dict["create_files"] == 'n':

            # We need to check if the directory exists before writing.
            check_file = os.listdir(f'{OUTPUT_FOLDER}/{_class["_filename"]}')

            if f'{_class["_filename"]}.gml' in check_file:

                # Write the formatted doc script to a new gml file at location.
                text_file = open(filepath, "w")
                text_file.write(output_code)
                text_file.close()

                # Log that bad boy.
                print(f'\'{_class["_filename"]}\' ==> {filepath}.')

    print("FINISHED.")

def get_settings():
    """
    This function takes settings from user_settings and puts them in a dictionary.
    """

    SETTINGS_FOLDER = ROOT_FOLDER + "settings/"

    if "settings" not in os.listdir("./"):
      os.mkdir(SETTINGS_FOLDER)

    if "user_settings" not in os.listdir(SETTINGS_FOLDER):

        # Create a settings file at location.
        text_file = open(SETTINGS_FOLDER + "user_settings", "w")
        text_file.write(f"""first_time:y
quick_write:n
create_files:n
templates_dir:./templates
data_dir:./input
output_dir:./output""")
        text_file.close()

    settings_dict = {}

    # Open user settings txt file to read
    with open(f'{SETTINGS_FOLDER}/user_settings') as f:

        text = f.readlines()

        # Go through text settings and put them in a dictionary.
        for line in text:

            key = line.strip().split(":")[0]
            value = line.strip().split(":")[1]

            settings_dict[key] = value

    return settings_dict

def set_settings(setting, value):
    """
    This function writes settings to the user_settings txt file
    """

    # Read from txt file
    settings_dict = get_settings()

    SETTINGS_FILE = ROOT_FOLDER + "settings/user_settings"

    if setting in settings_dict.keys():

        output_txt = ""

        # Update the passed in settings dict, 
        settings_dict[setting] = value

        # Then save those updates to 'user_settings'.txt
        for line in settings_dict:

            output_txt += (str(line) + ":" + str(settings_dict[line]) + "\n")

        # Write new dictionary to file.
        text_file = open(SETTINGS_FILE, "w")
        text_file.write(output_txt)
        text_file.close()

    else:

        print("Setting not found.")

def user_input_setting(setting, message, options=[]):
    """
    This function prompts user input and then changes the settings appropriately.
    """

    user_input = ""

    # Wait for user input to match one of the avail. options.
    while user_input not in options:
        user_input = input("\n" + message + "\n")
        if len(options) == 0:
            # If no options provided, accept anything.
            break

    # Once user_input in options, update the setting.
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

        # INITIALISE SETTINGS
        # If it is the first time user has booted up:
        if settings_dict['first_time'] == 'y':

            print("""~~~~~ Initialise Settings ~~~~~
            """)

            # Create_files setting.
            user_input_setting('create_files', "Would you like to allow DocGen to create files in your directory? (y/n)", ["y", "n"])

            # Quick_write setting
            user_input_setting('quick_write', "Would you like to allow DocGen to quick write at the push of a button? (y/n)", ["y", "n"])

            # It is now no longer the first time the user has booted up
            set_settings('first_time', 'n')

        # MAIN MENU LOOP
        user_input = input("""~~~~~ What would you like to do? ~~~~~

Run:        'r'
Help:       'h'
Settings:   's'
Exit:       'e'

""")

        if user_input == "r":

            # This boolean arms the DocGen
            run_boolean = False

            # Check whether quick write is enabled.
            if settings_dict['quick_write'] == 'n':

                # If it isn't enabled, check whether they want to write or not.
                user_input = input("Would you like to run DocGen? Be warned, it may do unexpected things. (y/n)")

                if user_input == 'y':
                    # They have agreed to the terms and conditions, and we may now arm the directory destroyer.
                    run_boolean = True

                else:
                    # They have not agreed to the terms and conditions, and will be returned to the main menu.
                    run_boolean = False

            elif settings_dict['quick_write'] == 'y':

                # Quick write is on, so arm the DocGen
                run_boolean = True

            # Check if it is armed.
            if run_boolean == True:

                # Run the thing.
                ### PASS IN SETTINGS
                do_the_thing(settings_dict)

        elif user_input == "h":

            # Help message to console
            print(f"""~~~~~ DocGen: The Document Generator ~~~~~
Originally written for Aether in 2020.

This Document Generator was written to generate and modify the API for a game engine. Essentially, it takes json files from the
"input" folder, and then uses python templates from the "templates" folder, and merges them. This allows us to create vast
quantities of code, and edit that code very quickly and easily.

I will now walk you through using DocGen:

1. You will need to create a json file of the following format:

    a) Entries with #'s in front and behind are for you to put in yourself. 
    b) The "_default" entry at the beginning is optional, if you would like a default template.
    c) The "_filename" entry is what the new file created will be called.
    d) The "_templates" entry is where you can specify which python templates to enact on the Json file.
    e) The "..."'s indicate that you can add as many more entries here as you require.
    f) [#template1#, #template2#, ...] etc. refers to the specific python templates you would like. The
        order of these gives the order that they will appear in the file.
    g) #optional_property1" etc. gives optional properties that you can use in the code. For example, if
        you wanted a "type" entry that was unique to each file, you would put this here. The #value# of
        this entry can be in the format of a dictionary, list, or string.

Json:

{{
    "_default":[#template1#, #template2#, ...]
    "#firstfilename#":{{
        "_filename": #filename#
        "_templates": [#template1#, #template2#, ...]
        #optional_property1#: #value#
        #optiona2_property1#: #value#
        ...
    }}
    "#secondfilename#":{{
        "_filename": #filename#
        "_templates": [#template1#, #template2#, ...]
        #optional_property1#: #value#
        #optiona2_property1#: #value#
        ...
    }}
    "#thirdfilename#":{{
            "_filename": #filename#
            "_templates": [#template1#, #template2#, ...]
            #optional_property1#: #value#
            #optiona2_property1#: #value#
            ...
    }}
    ...
}}

2. You will need to create a python file which returns a string.

You can create this string in whichever way pleases you, but it is highly recommended to make use of
Python's "f-string" templates which have the following form:

f\"""Here is some text.

Variables can be used like this: {{class_name}} would write the variable "class_name" to the string.
\"""

Using loops and appropriate information flow will allow you to create a string in such a way as to 
represent even larger quantities of code.

Providing that the Python file is in the "templates" folder, and that that file returns a string, a
file will be generated by Document Generator.

3. Linking the Python Template and the Json file is done by the following steps:

    a) Writing and placing a Python "Template" file (.py) in the "templates" folder
    b) Writing a Json file that has that template included in either the "_default" or "_templates" 
    entry. Extra properties added will be read by DocGen, and can be used in the Python Templates.
    c) Running DocGen.

Once this process is complete, if you need to add to or amend your code, you can simply change the template
or Json file. This will allow you to make, say, a small (or large!) change to every file in your Document Generator
at the press of a button.

""")

        elif user_input == "s":
            # Settings menu
            user_input = ""
            options = {
                "c": ["create_files", "Would you like to allow DocGen to create files in your directory? (y/n)", ["y", "n"]],
                "q": ["quick_write", "Would you like to allow DocGen to quick write at the push of a button? (y/n)", ["y", "n"]],
                "t": ["templates_dir", "Where would you like to load templates from?", []],
                "d": ["data_dir", "Where would you like to load data from?", []],
                "o": ["output_dir", "Where would you like to save the output to?", []]
            }

            while user_input not in options.keys():
                
                user_input = input("""~~~~~ Which setting would you like to change? ~~~~~

Create Files:       'c' 
Choose whether DocGen can create files in your directory.

Quick Write:        'q'    
Choose whether DocGen can quick write at the push of a button.

Template location:   't'
Specify directory for templates.

Data location:   'd'
Specify directory for data.

Output location:   'o'
Specify root directory for output.

""")
            option = options[user_input]
            user_input_setting(option[0], option[1], option[2])

        elif user_input == "e":
            break

    # Exit message
    print("Many thanks for using DocGen")

if __name__ == "__main__":

    run_menu()

        