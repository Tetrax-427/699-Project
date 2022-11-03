import mimetypes
from flask import Flask,send_file,render_template,request
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

print("Editing by somil")
data=pd.read_excel("data.xlsx")
X=[1,2,3,4,5,6,7,8,9]
Y=[12,8,4,2,1,2,4,8,12]

app=Flask(__name__,template_folder='template')
x_size=6
y_size=6
x_col="X-Label"
y_col="Y-Label"
plot_type=1

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/', methods =["GET", "POST"])
def form_data():
    if request.method == "POST":
        
        global X
        global Y
         
        global x_col
        global y_col
        
        global plot_type

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
        
    return render_template('form.html')

@app.route('/visualize')
def visualize():
    
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

    else:
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
    
        plt.plot(X,Y)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/jpg')


if __name__=="__main__":
    app.run()