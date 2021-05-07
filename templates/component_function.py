def component_function(_class, _classes):

  nl = "\n"
  tab = "  "

  def iterate_defaults(_class):
    str = ""
    for _prop in _class["properties"]:
      str += f'{tab}{_prop["name"]}'
      if "def" in _prop:
        str += f' = {_prop["def"]},{nl}'
      else:
        str += f',{nl}'
    str = str[:-1] # Remove last new line.
    return str

  def iterate_states(_class):
    str = ""
    for _prop in _class["properties"]:
      str += f'{tab}const [_{_prop["name"]}, set{_prop["Name"]}] = useState<{_prop["type"]}>({_prop["name"]}){nl}'
    str = str[:-1] # Remove last new line.
    return str

  return f"""
export const {_class["Name"]} = ({{
  children,
{iterate_defaults(_class)}
}}: {_class["name"]}Props) => {{
{iterate_states(_class)}

  return (
    {{children}}
  )
}}

export default {_class["Name"]}

"""