from rest_framework.exceptions import ValidationError


def validate_minimum_size(image):
    width, height = (1000, 1000)
    error = False
    if width is not None and image.width < width:
        error = True
    if height is not None and image.height < height:
        error = True
    if error:
        raise ValidationError(
            [f"Size should be at least {width} x {height} pixels."]
        )

