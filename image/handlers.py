def image_name_handler(image):
    """
    it removes `media/` and `extension` from name
    """
    name = image.split("/")[3].split(".")[0]

    return name


def image_path_handler(instance, filename):
    """
    it creates path for image
    """
    return f"media/{instance.user.id}/images/{filename}"


def thumbnail_path_handler(instance, filename):
    """
    it creates path for image
    """
    return f"{instance.user.id}/images/{filename}"


def generate_link_handler(request, link_id):
    return request.build_absolute_uri(f"/api/link/{link_id}/")


def thumbnails_response_handler(thumbnail_heights, thumbnail_response):
    new_dict = {}

    for index in range(len(thumbnail_response)):
        new_dict[thumbnail_heights[index].height] = thumbnail_response[index][
            "thumbnail"
        ]

    return new_dict
