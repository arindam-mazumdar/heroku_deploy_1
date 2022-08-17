from matplotlib import pyplot as plt 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from flask import Flask, request, render_template,jsonify

app = Flask(__name__,template_folder='template')

def do_something(age,sex,smoke):
   age = int(age)
   sex = sex.upper()
   age = str(2*age)
   combine =  sex+' with '+age + smoke   
   return combine
   
@app.route('/')
def home():
    return render_template('format_2inputs.html')    
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    age = request.form['age']
    sex = request.form['sex']
    smoke = request.form['smoke']
    combine = do_something(age,sex,smoke)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
    

@app.route('/')
def chartTest():
    x = np.arange(0,10)
    y = np.array([i**2 for i in x])
    plt.plot(y,x)
    plt.savefig('/home/arindam/codes/BRFS/brfss_website/template/new_plot.png')
    return render_template('format_2inputs.html', name = 'new_plot', url = '/home/arindam/codes/BRFS/brfss_website/template/new_plot.png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
