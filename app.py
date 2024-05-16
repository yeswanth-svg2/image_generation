from flask import Flask, render_template, request, send_from_directory
from gradio_client import Client
import os
import shutil
import re

app = Flask(__name__)

client = Client("KingNish/Instant-Image")

def generate_images(prompt):
    image = client.predict(
        prompt=prompt,
        negative_prompt=prompt,
        style="(No style)",
        use_negative_prompt=False,
        seed=0,
        width=1024,
        height=1024,
        inference_steps=4,
        randomize_seed=True,
        api_name="/run"
    )
    return image

def sanitize_filename(prompt):
    # Remove any non-alphanumeric characters (except for spaces)
    filename = re.sub(r'[^a-zA-Z0-9 ]', '', prompt)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Truncate to 15 characters
    return filename[:15]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = generate_images(prompt)
        path = image[0][0]['image']

        filename = sanitize_filename(prompt) + '.png'
        destination_path = os.path.join('static', filename)

        shutil.copy2(path, destination_path)

        return render_template('index.html', image_filename=filename)

    return render_template('index.html', image_filename=None)

@app.route('/static/<filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
