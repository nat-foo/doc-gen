def component_imports(_class, _classes):

  nl = "\n"

  def iterate_imports(_class):
    _known_types = [
      "string",
      "number",
      "boolean",
      "any",
      "undefined",
      "null",
    ]
    str = ""
    for _prop in _class["properties"]:
      # Remove [] from arrays of types.
      if "[]" in _prop["type"]:
        _prop["Type"] = _prop["Type"][:-2]
        _prop["_type"] = _prop["_type"][:-2] # "_" denotes underscore case version.

      # Avoid duplicates.
      if _prop["_type"] in str:
        continue

      # Import if type not known or not an arrow function.
      if _prop["_type"] not in _known_types \
      and "=>" not in _prop["type"]:
        str += f'import {{ {_prop["Type"]} }} from "@example/{_prop["_type"]}"{nl}'
    str = str[:-1] # Remove last new line.
    return str

  return f"""import {{ ReactNode, useState }} from 'react'
{iterate_imports(_class)}

"""