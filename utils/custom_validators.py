from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import ValidationError
from PIL import Image
from io import BytesIO

# Define allowed file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

def file_size_limit(form, field):
    """Custom validator to check file size."""
    file = field.data
    if file and file.content_length and file.content_length > MAX_FILE_SIZE:
        raise ValidationError("File size must be less than 5MB.")

def image_dimension_limit(form, field):
    """Custom validator to check image dimensions."""
    file = field.data
    if file:
        image = Image.open(BytesIO(file.read()))
        file.seek(0)
        width, height = image.size
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            raise ValidationError(f"Image dimensions should not exceed {MAX_WIDTH}x{MAX_HEIGHT} pixels.")
