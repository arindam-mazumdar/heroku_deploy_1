#!/usr/bin/env python
import pandas as pd
import numpy as np
import pickle
from flask import Flask, flash, redirect, render_template, request, url_for
from matplotlib import pyplot as plt

import os

from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__,template_folder='template')



#app.config["CACHE_TYPE"] = "null"


#path = '/home/arindam/codes/BRFS/LLCP2020ASC/'
#df = pd.read_csv(path+'wrangled_data.csv')
#df = df.drop('Unnamed: 0', axis=1)
##df['BMI'] = df['WTKG3']/(pow(df['HEIGHT']/100., 2))
#df=df[df['_AGEG5YR']!=14]

age_list = ['18 to 24','25 to 29','30 to 34','35 to 39','40 to 44','45 to 49','50 to 54','55 to 59','60 to 64','65 to 69','70 to 74','75 to 79','80 or older']
sex_list = ['Male','Female']
smoke_list = ['Current smoker - now smokes every day','Current smoker - now smokes some days','Former smoker','Never smoked']
todo_list = ['Had physical activity or exercise in last 30 days', 'No physical activity or exercise in last 30 days']
hcov_list = ['Had health care coverage always', 'Did not have health care coverage always']
sleep_list = ['3','4','5','6','7','8','9','10','11']
drink_list = ['No', 'Yes']
diab_list = ['No', 'Yes']

#df=df[['_SEX','_AGEG5YR','_HCVU651','DIABETE4','_TOTINDA','_RFDRHV7','SLEPTIM1','SMOKE','MICHD']].astype(int)
#X = np.array(df[['_SEX','_AGEG5YR','_HCVU651','DIABETE4','_TOTINDA','_RFDRHV7','SLEPTIM1','SMOKE']])
#y = np.array(df['MICHD'])
#clf = MultinomialNB()
#clf.fit(X, y)


#### Import fitted model 

clf = pickle.load(open('NB_fitted', 'rb'))


    
fac_dict = pickle.load(open('factors', 'rb'))

fact_best=dict()
fact_best['smoke']= 'Never smoked'
fact_best['todo'] = 'Had physical activity or exercise in last 30 days'
fact_best['hcov'] = 'Had health care coverage always'
fact_best['sleep'] = ['8','9','10','11']
fact_best['drink'] = 'No'
fact_best['diab'] = 'No'    

######################################################################


def calculate_risk(age,sex,smoke, todo, hcov,sleep, drink,diab):
    for i in range(len(age_list)):
       if age == age_list[i]:
            age_num = i+1
    for i in range(len(sex_list)):
        if sex == sex_list[i]:
            sex_num = i+1
    for i in range(len(smoke_list)):
        if smoke == smoke_list[i]:
            smoke_num = i+1
    for i in range(len(todo_list)):
        if todo == todo_list[i]:
            todo_num = i+1
    for i in range(len(hcov_list)):
        if hcov == hcov_list[i]:
            hcov_num = i+1
    sleep_num = int(sleep)
    for i in range(len(drink_list)):
        if drink == drink_list[i]:
            drink_num = i+1
    for i in range(len(diab_list)):
        if diab == diab_list[i]:
            diab_num = i    
        
    #newdf = (df[(df['_AGEG5YR']== age_num) & (df['SMOKE'] == smoke_num) & (df['_SEX'] == sex_num) & (df['_TOTINDA']== todo_num) & 
    #        (df['_HCVU651']== hcov_num) & (df['SLEPTIM1']== sleep_num) & (df['_RFDRHV7']== drink_num) & (df['DIABETE4']== diab_num) ])
    
    #sum_num = sum(newdf['MICHD'])
    #len_num = len(newdf['MICHD'])
    #risk = sum_num/len_num * 100
    
    #'_SEX','_AGEG5YR','_HCVU651','DIABETE4','_TOTINDA','_RFDRHV7','SLEPTIM1','SMOKE'
    X_test = np.array([[sex_num, age_num, hcov_num, diab_num, todo_num, drink_num, sleep_num, smoke_num]])
    y_pred = clf.predict_proba(X_test)
    risk = y_pred[0][1]*100 
    return risk
    
    
def calculate_healthy(age,sex):
    return calculate_risk(age,sex,fact_best['smoke'], fact_best['todo'], fact_best['hcov'],'8', fact_best['drink'],fact_best['diab']) 
    
    
def get_pie(age,sex,smoke, todo, hcov,sleep, drink,diab):
    bad_dict = dict()
    for item in ['smoke', 'todo', 'hcov','sleep', 'drink','diab']:
        if eval(item) in fact_best[item]:
            pass
        else:
            bad_dict[item] = eval(item)
    if len(bad_dict) > 0 :
        prob_dict = {}
        for keys, values in bad_dict.items():
            prob_dict[keys] = fac_dict[keys][values]
        
        if os.path.exists("static/pie.png"):
            os.remove("static/pie.png")

        plt.pie(prob_dict.values(), labels= prob_dict.keys(), autopct='%1.1f%%', shadow=True)
        plt.savefig('static/pie.png', dpi=200)
        plt.close()
        return "../static/pie.png?dummy=8484744"
    else:
        return "../static/thumbs_up.jpg" 
            
    
def calculate_factor(age,sex,smoke, todo, hcov,sleep, drink,diab):
    
    bad_dict = dict()
    for item in ['smoke', 'todo', 'hcov','sleep', 'drink','diab']:
        if eval(item) in fact_best[item]:
            pass
        else:
            bad_dict[item] = eval(item)
    if len(bad_dict) > 0 :
        prob_dict = {}
        for keys, values in bad_dict.items():
            prob_dict[keys] = fac_dict[keys][values] 
            
        sort_dict =  sorted(prob_dict.items(), key = lambda x: x[1], reverse= True )      
    #    prob_list = [fac_dict['smoke'][smoke], fac_dict['todo'][todo], fac_dict['hcov'][hcov], fac_dict['sleep'][sleep], fac_dict['drink'][drink],
    #    fac_dict['diab'][diab] ]
        case_dict = {'smoke':'Smoking', 'todo':'Lack of Physical Ativity', 'hcov': 'Lack of Health Coverage', 'sleep': 'Less Sleeping', 'drink': 'Drinking', 'diab':'History of Diabetis'}
        return 'The main cause of this is: '+case_dict[sort_dict[0][0]]

    else:
        return "Don't worry! You are doing good for your age and gender"





@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template(
        'input_dropdown.html',
        data1=[{'name':  '18 to 24'},{'name':  '25 to 29'},{'name':  '30 to 34'},{'name':  '35 to 39'},{'name':  '40 to 44'},{'name':  '45 to 49'},{'name':  '50 to 54'},{'name':  '55 to 59'},{'name':  '60 to 64'},{'name':  '65 to 69'},{'name':  '70 to 74'},{'name':  '75 to 79'},{'name':  '80 or older'}],
        data2= [{'name':'Male'}, {'name':'Female'}],
        data3 = [{'name': 'Current smoker - now smokes every day'},{'name': 'Current smoker - now smokes some days'},{'name': 'Former smoker'},{'name': 'Never smoked'}],
        data4 = [{'name': 'Had physical activity or exercise in last 30 days'},{'name': 'No physical activity or exercise in last 30 days'}],
        data5 = [{'name':'Had health care coverage always'}, {'name':'Did not have health care coverage always'}],
        data6 = [{'name':'3'},{'name':'4'},{'name':'5'},{'name':'6'},{'name':'7'},{'name':'8'},{'name':'9'},{'name':'10'},{'name':'11'}],
        data7 = [{'name': 'No'},{'name': 'Yes'}],
        data8 = [{'name': 'No'},{'name': 'Yes'}])
   

@app.route("/test" , methods=['GET', 'POST'])
def test():
    age = request.form.get('comp_select1')
    sex = request.form.get('comp_select2')
    smoke = request.form.get('comp_select3')
    todo = request.form.get('comp_select4')
    hcov = request.form.get('comp_select5')
    sleep = request.form.get('comp_select6')
    diab = request.form.get('comp_select7')
    drink = request.form.get('comp_select8')
    #risk_out = '{:.2f}'.format(calculate_risk(age,sex,smoke))
    return render_template('output.html', risk_out = '{:.2f}'.format(calculate_risk(age,sex,smoke,todo, hcov,sleep, drink,diab)),
    ratio_out =  '{:.2f}'.format(calculate_risk(age,sex,smoke,todo, hcov,sleep, drink,diab)/calculate_healthy(age,sex)),
    pie_out = get_pie(age,sex,smoke,todo, hcov,sleep, drink,diab),
    case_out = calculate_factor(age,sex,smoke,todo, hcov,sleep, drink,diab) )

if __name__=='__main__':
    app.run(debug=True)

