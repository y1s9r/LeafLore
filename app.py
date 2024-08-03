from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'plant' not in request.files:
            return ("File not uploaded")
        
        plant = request.files.get("plant")
        
        if plant.filename == "":
            return ("Invalid file selected")
        
        if plant and plant.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return render_template("uploaded.html")
        
        return ("Invalid file type selected")
    
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
