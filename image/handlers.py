def image_name_handler(image):
    """
    it removes `media/` and `extension` from name
    """
    name = image.split("/")[1].split(".")[0]
    return name
