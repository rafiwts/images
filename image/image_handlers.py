def image_name_handler(image):
    """
    it removes `media/` and `extension` from name
    """
    name = image.split("/")[1].split(".")[0]
    return name


def image_path_handler(instance, filename):
    # FIXME: instance.id returns None in a path
    """
    it creates path for image
    """
    return f"{instance.user.id}/images/{filename}"
