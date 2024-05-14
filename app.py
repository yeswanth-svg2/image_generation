from flask import Flask , render_template , request
from gradio_client import Client
import os
import shutil

app = Flask(__name__)

client = Client("KingNish/Instant-Image")

def generate_images(prompt):
      
    image=  client.predict(
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
      

@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
      prompt= request.form['prompt']
     
      image= generate_images(prompt)
    #   file_path = os.path.join('./static' , 'static.jpeg')
      path=image[0][0]['image']
      print(image)
    #   path.save(file_path)
      
    #   print(path)
      
      source_destination = path
      destination_path = './static/static.png'


      shutil.copy2(source_destination, destination_path)
      print("image is uploaded to static directory")

    


      return render_template('index.html' , image=image)
    
    return render_template('index.html')







if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True)
