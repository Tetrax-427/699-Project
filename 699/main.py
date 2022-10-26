import mimetypes
from flask import Flask,send_file,render_template,request
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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
        
        plot_type=request.form.get("plot_type")
        
        
        X=data[x_col].to_list()
        Y=data[y_col].to_list()

        x_size=6
        y_size=6
        if plot_type=='1':
            fig,ax= plt.subplots(figsize=(x_size,y_size))
            ax=sns.set_style(style="darkgrid")
            plt.plot(X,Y)       #LINE graph
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            canvas=FigureCanvas(fig)
            img=io.BytesIO()
            fig.savefig(img)
            img.seek(0)
            return send_file(img,mimetype='img/png')
        elif plot_type=="2":
            fig,ax= plt.subplots(figsize=(x_size,y_size))
            ax=sns.set_style(style="darkgrid")
            plt.bar(Y, X, width = 0.4)  #BAR graph
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            canvas=FigureCanvas(fig)
            img=io.BytesIO()
            fig.savefig(img)
            img.seek(0)
            return send_file(img,mimetype='img/png')
        elif plot_type=="3":
            fig,ax= plt.subplots(figsize=(x_size,y_size))
            ax=sns.set_style(style="darkgrid")
            plt.scatter(X,Y)     #Scatter Plot
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
    return send_file(img,mimetype='img/jpg')


if __name__=="__main__":
    app.run()