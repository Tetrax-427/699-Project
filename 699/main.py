import mimetypes
from flask import Flask, flash, redirect,send_file,render_template,request
import io
import base64
from werkzeug.utils import secure_filename
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import shutil
import random




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
ALLOWED_EXTENSIONS = set(['xlsx'])

df=pd.read_excel("data.xlsx")
uploaded_file="data.xlsx"
X=[1,2,3,4,5,6,7,8,9]
Y=[6,8,4,2,1,2,4,8,6]


x_size=15
y_size=6
x_col="A"
y_col="B"

y_vals=["A","B"]
plot_type=1

colors=["red","forestgreen","royalblue","darkorange",
        "deepskyblue","deeppink","teal",
        "greenyellow","crimson","violet",
        "darkcyan","purple","gold","navy"
        ]
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/iframe')
def iframe():
    
    #global df
    global uploaded_file
    
    
    
    return render_template('plot.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    global file_names
    global uploaded_file
    global df
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
        
        
        uploaded_file = os.path.join(UPLOAD_FOLDER, file_names[-1])
        df=pd.read_excel(uploaded_file)
        flash('File in Use: ' + file_names[-1]  )
        data=pd.read_excel(uploaded_file)
        
        html_page = data.to_html(index=False)
        css="""<head>
<style>
table, td, th {  
  border: 1px solid #ddd;
  text-align: left;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  padding: 15px;
  text-align: center;
}

th{
    background-color: MediumSeaGreen;
}
th.sticky {
  position: fixed;
  top: 0;
  width: 100%;
}
tr:nth-child(even) {
  background-color: rgba(150, 212, 212, 0.4);
}

td:nth-child(even) {
  background-color: rgba(150, 212, 212, 0.4);
}

</style>
</head>
        """
        to_html = open("static/plot.html", "w")
        to_html.write(css+html_page)
        to_html.close()
        return render_template('form.html')
    

@app.route('/form_data', methods =["GET", "POST"])
def form_data():
    if request.method == "POST":
        
        global X
        global Y
         
        global x_col
        global y_col
        
        global y_vals
        
        global plot_type
        global file_names
        
        global df
        global uploaded_file
        
        # getting input with name = x_col in HTML form
        #data=request.form.get("FILE")
        x_co= request.form.get("x_col")
        if x_co!="":
            x_col=x_co
        # getting input with name = x_col in HTML form
        y_va = request.form.get("y_col")
        if y_va!="":
            y_vals=y_va.split(',')
            y_col=y_vals[0]
            
            
        plot_tp=request.form.get("plot_type")
        if plot_tp!="":
            plot_type=plot_tp
        
        
        if len(file_names)!=0:
            df=pd.read_excel(uploaded_file)
        
        
        

        x_size=6
        y_size=6
        flash('File in Use: ' + file_names[-1])
        
         
    return render_template('form.html')

@app.route('/visualize')
def visualize():
    global df
    global uploaded_file
    
    X=df[x_col].to_list()
    
    if plot_type=='Line Graph':
        #Y=df[y_col].to_list()
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
        for y in y_vals:
            Y=df[y].to_list()
            plt.plot(X,Y,color= colors[y_vals.index(y)])       #LINE graph
        #plt.legend()
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/png')
    
    elif plot_type=="Bar Graph":
        #Y=df[y_col].to_list()
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
          #BAR graph
        
        L=len(y_vals)
        w=0.6/L
        a=w/2
        a=-1*a
        for i in range(len(y_vals)):
            y=y_vals[i]
            Y=df[y].to_list()
            X_axis = np.arange(len(X))
            plt.bar(X_axis+a, Y, width = w, color= colors[i])      #bar graph
            a=a+w
        plt.xticks(X_axis, X)
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/png')
    
    elif plot_type=="Scatter Plot":
        #Y=df[y_col].to_list()
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
           #Scatter Plot
        for y in y_vals:
            Y=df[y].to_list()
            plt.scatter(X,Y,color= colors[y_vals.index(y)])        #SCatter graph
        
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        
        return send_file(img,mimetype='img/png')
    
    elif plot_type=="Histogram":
        y_col=y_vals[0]
        Y=df[x_col].to_list()
        X=df[y_col].to_list()
        n_bins = len(set(X))
 
        # Creating distribution
        x = X
        y = Y
 
        # Creating histogram
        fig, axs = plt.subplots(1, 1,
                        figsize =(x_size, y_size),
                        tight_layout = True)
 
        axs.hist(x, bins = n_bins)
        ax=sns.set_style(style="darkgrid")
        
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        
        return send_file(img,mimetype='img/png')

    elif plot_type=="Box Plot":
        data=[]
        for col in y_vals:
            data.append(df[col].to_list())
            print("data len :  " , len(data))
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
        
        plt.boxplot(data)
        x=[ i+1 for i in range(len(y_vals))]
        plt.xticks( x,y_vals)
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/jpg')
    
    elif plot_type=="Pie Chart":
        y_col=y_vals[0]
        Y=df[y_col].to_list()
        fig,ax= plt.subplots(figsize=(x_size,y_size))
        ax=sns.set_style(style="darkgrid")
        
        plt.pie(Y,labels =X)
        canvas=FigureCanvas(fig)
        img=io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img,mimetype='img/jpg')

    else:
        
        return send_file("static/download.jpg")

@app.route('/download', methods =["GET", "POST"])
def download():
    if request.method == "POST":
        return visualize()

@app.route('/legend')
def legend():    
    y=[0,0,0,0]
    x=[1,2,3,4]
    fig,ax= plt.subplots(figsize=(1,len(y_vals)))
      
    
  
    #Adding text inside a rectangular box by using the keyword 'bbox'
    #for i in range(len(y_vals)):
    for i in range(len(y_vals)):
        plt.text(0.5, 0.8-0.2*i, y_vals[i], fontsize = 16,color = colors[i])
    #plt.plot(x, y, c = 'g')
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/jpg')
if __name__=="__main__":
    app.run()