import mimetypes
from flask import Flask, flash, redirect,send_file,render_template,request
import io
import base64
from werkzeug.utils import secure_filename
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil


app=Flask(__name__,template_folder='template')
file_names=[]
app.secret_key = "secret key"
path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')
shutil.rmtree(UPLOAD_FOLDER, ignore_errors=False, onerror=None)

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['xlsx','csv'])

data=pd.read_excel("data.xlsx")
X=[1,2,3,4,5,6,7,8,9]
Y=[6,8,4,2,1,2,4,8,6]


x_size=6
y_size=6
x_col="X-Label"
y_col="Y-Label"
plot_type=1
print("Fuck")
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    global file_names
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                
                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return render_template('form.html')
    

@app.route('/form_data', methods =["GET", "POST"])
def form_data():
    if request.method == "POST":
        
        global X
        global Y
         
        global x_col
        global y_col
        
        global plot_type
        global file_names
        print("Fucku")
        # getting input with name = x_col in HTML form
        #data=request.form.get("FILE")
        x_col= request.form.get("x_col")
        # getting input with name = x_col in HTML form
        y_col = request.form.get("y_col")
        
        plot_type=request.form.get("plot_type")
        
        
        uploaded_file = os.path.join(UPLOAD_FOLDER, file_names[0])
        df=pd.read_csv(uploaded_file)
        print(df.head())
        X=df[x_col].to_list()
        Y=df[y_col].to_list()

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