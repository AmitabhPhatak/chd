import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import mysql.connector
import datetime 

##Connect to SQL database and table

cnx = mysql.connector.connect(user='Amitabh', password='Asp1234$',database='medapp')
cursor = cnx.cursor()

app = Flask(__name__,template_folder='C:/Users/Amit')
model = pickle.load(open('model.pkl', 'rb'))

#Loads index html file

@app.route('/')
def home():
    return render_template('index.html')

##takes input from values entered on homepage 

@app.route('/predict',methods=['POST'])
def predict():
    
    int_features = [x for x in request.form.values()]
    cat_features=int_features[0:2]
    
    int_features=int_features[2:]    ##values needed for model,omit entries like date and name
    int_features = [int(x) for x in int_features]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)



#Commit the values to Msql database
    
    #output = int(prediction[0,1])
    output=int(prediction)
    cnx = mysql.connector.connect(user='Amitabh', password='Asp1234$',database='medapp')
    cursor = cnx.cursor()
    add_user = ("INSERT INTO user "
          "                (Dates,uname,TenYearCHD,male,age,education,currentSmoker,cigsPerDay,BPMeds,prevalentStroke,prevalentHyp,diabetes,totChol,sysBP,diaBP,BMI,heartRate,glucose)      "
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    int_features.insert(0,cat_features[0])
    int_features.insert(1,cat_features[1])
    int_features.insert(2,output)
    data_user = int_features
    prob=""
    if output==1: 
        prob="high"
    else:
        prob="low"  
# Insert new user
    cursor.execute(add_user, data_user)

# Make sure data is committed to the database
    cnx.commit()
    
    cursor.close()
    cnx.close()
    return render_template('index.html', prediction_text=' Possibility to get CHD in next 10 years is {}'.format(prob))

##Outputs prediction score to Homepage

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = int(prediction[0,1])
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)