
import hashlib
import io
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, url_for
from PIL import Image, ImageChops, ImageEnhance, ExifTags, UnidentifiedImageError
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ELA_FOLDER = BASE_DIR / "static" / "ela_results"

UPLOAD_FOLDER.mkdir(exist_ok=True)
ELA_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def calculate_sha256(filepath):
    digest = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def extract_metadata(image):
    metadata = {
        "Format": image.format or "Unknown",
        "Width": f"{image.width} pixels",
        "Height": f"{image.height} pixels",
        "Color Mode": image.mode,
    }

    try:
        exif_data = image.getexif()

        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))

            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="replace")

            metadata[f"EXIF: {tag_name}"] = str(value)[:300]

        if not exif_data:
            metadata["EXIF Information"] = "No EXIF metadata found"

    except (OSError, ValueError, TypeError):
        metadata["EXIF Information"] = "Could not read EXIF metadata"

    return metadata


def perform_ela(filepath, output_path, quality=90):
    """Generate an Error Level Analysis visualization for a JPEG."""
    with Image.open(filepath) as source:
        if source.format != "JPEG":
            return False

        original = source.convert("RGB")

    # Recompress the image in memory without changing the evidence file.
    buffer = io.BytesIO()
    original.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    with Image.open(buffer) as recompressed_image:
        recompressed = recompressed_image.convert("RGB")

    # Calculate pixel-level differences.
    difference = ImageChops.difference(original, recompressed)

    # Amplify differences so they are easier to inspect.
    ela_image = ImageEnhance.Brightness(difference).enhance(10)

    ela_image.save(output_path, format="PNG")
    return True


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please select an image to analyze."

        elif not allowed_file(uploaded_file.filename):
            error = "Only JPG, JPEG, and PNG files are accepted."

        else:
            filename = secure_filename(uploaded_file.filename)

            if not filename:
                error = "Invalid filename. Please choose another image."
            else:
                unique_id = uuid.uuid4().hex
                saved_name = f"{unique_id}_{filename}"
                filepath = UPLOAD_FOLDER / saved_name
                ela_filename = f"{unique_id}_ela.png"
                ela_path = ELA_FOLDER / ela_filename

                try:
                    uploaded_file.save(filepath)

                    # Validate the uploaded file as an actual image.
                    with Image.open(filepath) as image:
                        image.verify()

                    with Image.open(filepath) as image:
                        metadata = extract_metadata(image)
                        image_format = image.format

                    ela_available = False

                    if image_format == "JPEG":
                        ela_available = perform_ela(filepath, ela_path)

                    result = {
                        "filename": filename,
                        "size": f"{filepath.stat().st_size:,} bytes",
                        "sha256": calculate_sha256(filepath),
                        "metadata": metadata,
                        "analyzed_at": datetime.now().strftime(
                            "%d %b %Y, %I:%M:%S %p"
                        ),
                        "ela_available": ela_available,
                        "ela_url": (
                            url_for(
                                "static",
                                filename=f"ela_results/{ela_filename}"
                            )
                            if ela_available else None
                        ),
                    }

                except (
                    UnidentifiedImageError,
                    OSError,
                    ValueError,
                    Image.DecompressionBombError,
                ):
                    if filepath.exists():
                        filepath.unlink()
                    if ela_path.exists():
                        ela_path.unlink()

                    error = "The file is not a valid or readable image."

    return render_template("index.html", result=result, error=error)


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        result=None,
        error="File exceeds the 10 MB upload limit."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
