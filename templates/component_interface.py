def component_interface(_class, _classes):

  nl = "\n"
  tab = "  "
    
  def iterate_interface(_class):
    str = ""
    for _prop in _class["properties"]:
      str += f'{tab}{_prop["name"]}{"?" if "def" in _prop else ""}: {_prop["type"]}{nl}'
    str = str[:-1] # Remove last new line.
    return str

  return f"""import {{ ReactNode, useState }} from 'react'

export interface {_class["name"]}Props {{
  children: ReactNode
{iterate_interface(_class)}
}}
"""
