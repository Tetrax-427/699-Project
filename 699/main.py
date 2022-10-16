import mimetypes
from flask import Flask,send_file,render_template,request
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


fig,ax= plt.subplots(figsize=(6,6))
ax=sns.set_style(style="darkgrid")

data=pd.read_excel("data.xlsx")
X=data["A"].to_list()
Y=data["B"].to_list()

app=Flask(__name__,template_folder='template')


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/', methods =["GET", "POST"])
def form_data():
    if request.method == "POST":
        # getting input with name = x_col in HTML form
        #data=request.form.get("FILE")
        x_col= request.form.get("x_col")
        # getting input with name = x_col in HTML form
        y_col = request.form.get("y_col")
        
        X=data[x_col].to_list()
        Y=data[y_col].to_list()

        
        
        plt.plot(X,Y)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/png')
    return render_template('form.html')


@app.route('/visualize')
def visualize():
    plt.plot(X,Y)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')
      
      
if __name__=="__main__":
    app.run()
    