from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_KEY = "2b10Ksx2Ra5U4SpfpssAjBl2O"
site_url = 'https://my-api.plantnet.org/v2/identify/all?include-related-images=true&no-reject=false&nb-results=1&lang=en&type=kt'
headers = {
    'Authorization': f'Bearer {API_KEY}'
}

data = {
    'organs': []
}

parameters = ["leaf", "flower", "fruit", "bark", "other"]

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        data['organs'] = []
        selected_organs = request.form.getlist("organs")
        data['organs'].extend(selected_organs)
        if not data['organs']:
            return redirect("/")
        return redirect("/upload")
    return render_template("index.html", parameters=parameters)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    global files  # Declare files as global to modify it
    if request.method == "POST":
        files = []
        for organ in data['organs']:
            image = request.files.get(organ)
            if not image or image.filename == "":
                return f"Invalid file selected for {organ}", 400
            if image and image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(file_path)
                
                # Add file to files list
                files.append(('images', (file_path, open(file_path, 'rb'))))
            else:
                return f"Invalid filetype selected for {organ}", 400
        
        # Store files temporarily in a session or pass them directly to the result route
        return redirect("/result")  # Direct to result handling
        
    parts = data['organs']
    return render_template("upload.html", parts=parts)

@app.route("/result", methods=["GET"])
def result():
    # Read files again from storage or pass them directly
    print(data)
    print(files)
    response = requests.post(site_url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        return render_template("result.html", result=result)
    else:
        return f"API request failed with status code {response.status_code}", 500

if __name__ == "__main__":
    app.run(debug=True)