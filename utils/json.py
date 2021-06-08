import os, json

def load_data(path):
    """
    Loads all JSON files in the given directory (shallow only) and returns
    a dict of each JSON file, as well as a dict for each "_default" value.
    """
    data = {} # Contains the data_part objects to format the templates.
    defaults = {} # Stores the default values of each json file (In case an entry has no template).

    for file_name in os.listdir(path): # Assuming cwd == '/doc-gen'.        

        # Skip special case.
        if file_name == "__init__.py":
            continue

        # Load JSON data.
        with open(f'{path}/{file_name}') as f:
            try:
                data_part = json.load(f)
            except:
                print(f"<!> Bad JSON data_part in '{file_name}'! Skipping.")
                continue

            # Update data_part if JSON is a dict.
            if isinstance(data_part, dict):

                # If not enabled, don't add it (but enabled by default).
                # Note: Deactivates entire JSON file.
                if "_enabled" in data_part and not data_part["_enabled"]:
                    continue

                # Strip extensions.
                json_name = file_name.split('.')[0]

                # If there is a default property, add it to the defaults dict.
                if "_default" in data_part:
                    defaults[json_name] = data_part.pop('_default')

                # Add type value to each document.
                for item_name in data_part:
                    data_part[item_name]["_type"] = json_name

                data.update(data_part)

    return data, defaults