def custom_field(path, id="", tabs=0, comment="//"):
    """
    Allow the user to customise this field by reading the text from the script itself,
    and adding it to this template. Custom fields have optional IDs to differentiate
    from other fields in the same template.

    path: full path to the script containing the custom content.
    id: optional ID to differentiate this field from others in the same template.
    tabs: number of tabs to offset content by (default=0).
    comment: string that denotes a comment (default="//").

    NOTE: This util is intended only to be used within templates.
    """

    tabs = "\t" * tabs
    if id != "":
        id = f' CUSTOM FIELD: {id} '
    else:
        id = ' CUSTOM FIELD '

    gateCharLenMax = 80
    gateCharLen = int((gateCharLenMax - len(id)) / len(comment))
    fieldGateStart = f'{comment}{id}{comment*gateCharLen} START {comment}'
    fieldGateEnd = f'{comment}{id}{comment*gateCharLen} END {comment*2}'
    outerField = f'{tabs}{fieldGateStart}{"""{0}"""}{fieldGateEnd}'

    gateCharLenMax = 80
    gateCharLen = int((gateCharLenMax - len(id)) / len(comment))
    fieldGateStartNew = f'{comment}{id}{comment*gateCharLen} START {comment}'
    fieldGateEndNew = f'{comment}{id}{comment*gateCharLen} END {comment*2}'
    outerField = f'{tabs}{fieldGateStartNew}{"""{0}"""}{fieldGateEndNew}'

    # E.g.
    # // CUSTOM FIELD: METHODS ////////////////////////////////////////////////////////////////// START //
    # // CUSTOM FIELD: METHODS ////////////////////////////////////////////////////////////////// END ////

    with open(path, 'r') as f:
        rawText = f.read()
        f.close()

    rawTextSplit = rawText.split(fieldGateStart) # Only find gates with the given ID.
    
    if len(rawTextSplit) < 2:
        # There should be at least two areas created. If not, it's not a valid custom field.
        innerField = f"""

{tabs}{comment} Do nothing for now.

{tabs}"""
    else:
        areaAfterStart = rawTextSplit[1] # Access the area after the start gate.
        innerField = areaAfterStart.split(fieldGateEnd)[0] # Access the area before the end gate.
    
    # Add the inner field within the outer field.
    # Example outcome:
    """
    // CUSTOM FIELD: METHODS ////////////////////////////////////////////////////////////////// START //
    // CUSTOM FIELD: METHODS //////////////////////////////////////////////////////// START //
    function CreateActor(_role, _x, _y)
    {
        ...
    }
    // CUSTOM FIELD: METHODS //////////////////////////////////////////////////////////////////// END //
    """
    customField = outerField.format(innerField)
    return customField