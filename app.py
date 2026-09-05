import os
from flask import Flask, request, render_template
from services.parser import extract_text
from analyzer import analyze_resume, is_resume
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB limit

ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return render_template(
            "index.html",
            error="No file part in the request."
        )

    file = request.files["resume"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="No file selected."
        )

    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Only PDF or DOCX files are allowed."
        )

    safe_filename = secure_filename(file.filename)

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        safe_filename
    )

    file.save(save_path)

    try:
        extension = safe_filename.rsplit(".", 1)[1].lower()

        resume_text = extract_text(
            save_path,
            extension
        )

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="Could not extract any text from the resume."
            )

        # Check whether the uploaded document is actually a resume
        if not is_resume(resume_text):
            return render_template(
                "index.html",
                error=(
                    "This document does not appear to be a resume or CV. "
                    "Please upload a valid resume containing information "
                    "such as education, experience, skills, projects, "
                    "or certifications."
                )
            )

        # Analyze only after the document passes resume validation
        analysis = analyze_resume(resume_text)

        return render_template(
            "index.html",
            success=(
                f"Resume uploaded successfully! "
                f"Extracted {len(resume_text)} characters."
            ),
            analysis=analysis
        )

    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)

        return render_template(
            "index.html",
            error=f"An error occurred while processing the resume: {str(e)}"
        )

if __name__ == "__main__":
    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    app.run(debug=True)