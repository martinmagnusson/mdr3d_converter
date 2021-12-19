from lxml import etree


def find_XSD(filetype:str): ## Currently all use the same schema, update as I get hold of the others.
    xsd_path = "None"
    if filetype == "ROS Gridmap":
        xsd_path = "Validation_Templates\\2D_Standard_Schema.xsd"
    elif filetype == "2D Standard":       
        xsd_path =  "Validation_Templates\\2D_Standard_Schema.xsd"
    elif filetype == "Pointcloud": ##Not sure if pointcloud uses xml?
        xsd_path = "Validation_Templates\\2D_Standard_Schema.xsd"
    elif filetype == "Test XSD": ##Not sure if pointcloud uses xml?
        xsd_path = "Validation_Templates\\2D_Standard_Schema.xsd"
    print("\nSetting XSD path for:" + filetype + "\tLocation: " + xsd_path)
    return xsd_path

def validate(xml_path: str, filetype: str) -> bool:
    print("\nEntering validate function")
    xsd_path = find_XSD(filetype)

    xmlschema_doc = etree.parse(xsd_path) ##Creates the proper format for checking.
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result