from flask import Flask, Response, render_template, request
from flask import jsonify
import json
from math import sqrt
import numpy as np

app = Flask(__name__)
color = ''
data_distance = []

with open('data/data.csv', 'r') as file:
    data = file.read().splitlines()

for palette in data:
    data_distance.append([palette,0])

def get_palette(data_distance, hexa):
    temp_colors_filtred = []
    rgb = (tuple(int(hexa[i:i+2], 16) for i in (0, 2, 4)))
    for palette in data_distance:
        colors = palette[0].split(',')
        #print(colors)
        if '#'+hexa in colors:
            temp_colors_filtred.append(palette)
    if len(temp_colors_filtred) == 0:
        temp_colors_filtred = data_distance

    for palette in temp_colors_filtred:
        colors = palette[0].split(',')
        
        #converting to RGB
        distances_each_rgb = []
        for i in range(len(colors)):
            colors[i] = (tuple(int(colors[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)))
            #calculating distance for each color in palette and input color
            distances_each_rgb.append(sqrt((colors[i][0] - rgb[0])**2 + (colors[i][1] - rgb[1])**2 + (colors[i][2] - rgb[2])**2))
        palette[1] = sum(distances_each_rgb)
    distances = [i[1] for i in temp_colors_filtred]
    mean_distance = np.median(distances)
    all_distances_to_mean = []
    for data in temp_colors_filtred:
        all_distances_to_mean.append([data[0],sqrt((data[1] - mean_distance)**2)])
    colors_palette = min(all_distances_to_mean, key=lambda x: x[1])
    colors_palette.pop()
    colors_palette = colors_palette[0].split(',')
    colors_palette = [color.lstrip('#').upper() for color in colors_palette]
    print(colors_palette)
    return colors_palette

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    global color
    content = str(request.get_data())
    color = content.replace("b'color=%23",'').replace("'",'')
    colors = get_palette(data_distance, color)
    return jsonify(colors)



if __name__ == '__main__':
    app.run()
    