import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
import pickle
#import mysql.connector
#from sklearn.linear_model import LogisticRegression
#import sklearn.linear_model.logistic



# Load the machine learning model
model = pickle.load(open('/home/Amitabhp/mysite/model_lr_ch1.pkl', 'rb'))

#l=[0,10,1,1,30,1,1,1,1,120,110,150,40,70,6]
#prediction2 = model.predict([l])
#print("Pred", prediction2[0])


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.H1("CHD Prediction"),
    dcc.Input(id='input-male', type='text', placeholder='Male(1)/Female(0)', required=True),
    dcc.Input(id="age" ,type='text',placeholder="Age" ,required=True),
	dcc.Input(id="education",type="text",placeholder="Education(1,2,3,4)",required=True),
    dcc.Input(id='currentSmoker', type='text', placeholder='currentSmoker(1/0)', required=True),
    dcc.Input(id='cigsPerDay', type='text', placeholder='cigarettesPerDay', required=True),
    dcc.Input(id='BPMeds', type='text', placeholder='BP Medications taken(1/0)', required=True),
    dcc.Input(id='prevalentStroke', type='text', placeholder='prevalentStroke(1/0)', required=True),
    dcc.Input(id='prevalentHyp', type='text', placeholder='prevalentHypertension(1/0)', required=True),
    dcc.Input(id='diabetes', type='text', placeholder='diabetes(1/0)', required=True),
    dcc.Input(id='totChol', type='text', placeholder='totChol', required=True),
    dcc.Input(id='sysBP', type='text', placeholder='systolic BP', required=True),
    dcc.Input(id='diaBP', type='text', placeholder='diastolic BP', required=True),
    dcc.Input(id='BMI', type='text', placeholder='BMI', required=True),
    dcc.Input(id='heartRate', type='text', placeholder='heartRate', required=True),
    dcc.Input(id='glucose', type='text', placeholder='glucose', required=True),
    # Add similar Input components for other features

    html.Button(id='submit-button', n_clicks=0, children='Submit'),


    html.Div(id='prediction-text'),

    #Modal for displaying the chart
    html.Div([
    dcc.Graph(id='input-chart'),
    html.Button('Close Chart', id='close-chart-button')
    ], id='chart-modal', style={'display': 'none'}),

    html.P([
    html.Br(),
    html.A('Trends', href='http://localhost:4848/single/?appid=C%3A%5CUsers%5CAmit%5CDocuments%5CQlik%5CSense%5CApps%5CMedapp.qvf&sheet=0b538c64-59d3-4693-9e60-ebfb421c6a27&opt=ctxmenu', target='_blank')
   ])
])

@app.callback(
    [Output('prediction-text', 'children'),
     Output('input-chart', 'figure'),
     Output('chart-modal', 'style')],
    [Input('submit-button', 'n_clicks')],
    [
     dash.dependencies.State('input-male', 'value'),
     dash.dependencies.State('age', 'value'),
     dash.dependencies.State('education', 'value'),
     dash.dependencies.State('currentSmoker', 'value'),
     dash.dependencies.State('cigsPerDay', 'value'),
     dash.dependencies.State('BPMeds', 'value'),
     dash.dependencies.State('prevalentStroke', 'value'),
     dash.dependencies.State('prevalentHyp', 'value'),
     dash.dependencies.State('diabetes', 'value'),
     dash.dependencies.State('totChol', 'value'),
     dash.dependencies.State('sysBP', 'value'),
     dash.dependencies.State('diaBP', 'value'),
     dash.dependencies.State('BMI', 'value'),
     dash.dependencies.State('heartRate', 'value'),
     dash.dependencies.State('glucose', 'value')]
     # Add similar State components for other features
)

def update_prediction(n_clicks, input_male, age, education, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose):
    if n_clicks > 0:
        # Preprocess input data and make prediction
        input_data = [input_male, age, education, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose]


        # Print the input data being sent to the model
        #print("Input Data:", input_data)


        prediction = model.predict([np.array(input_data)])
        output = int(prediction[0])

# Print the model prediction
        print("Model Prediction:", output)

        # Insert data into the database
#        add_user = ("INSERT INTO user (currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose, TenYearCHD) "
 #                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        # Create a bar chart for input data
        chart_labels = ['input_male', 'age',' education','currentSmoker', 'cigsPerDay', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        chart_values = [float(value) for value in input_data]
         #print(chart_values)
        fig = px.bar(x=chart_labels, y=chart_values, labels={'x': 'Input Feature', 'y': 'Value'}, title='Input Data')

        # Display prediction result
        prob = "high" if output == 1 else "low"
        modal_style = {'display': 'block'}

        return f'Possibility to get CHD in the next 10 years is {prob}', fig, modal_style

    # Display the chart by setting the modal style to 'display: block'



        # Insert data into the database
        #add_user = ("INSERT INTO user (Dates, uname, TenYearCHD, male, age, education, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose) "
         #           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        #data_user = [date, name, output] + input_data[2:]  # Skip first two elements as they are already in the query
       # cursor.execute(add_user, data_user)
        #cnx.commit()

        # Display prediction result
        #prob = "high" if output == 1 else "low"
        #return f'Possibility to get CHD in the next 10 years is {prob}'

if __name__ == '__main__':
    app.run_server(debug=True)
