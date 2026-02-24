from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    status = int(request.form['status'])
    age_group = int(request.form['age_group'])
    education = int(request.form['education'])
    ai_risk = int(request.form['ai_risk'])
    salary = float(request.form['salary'])
    
    industry = request.form['industry']
    location = request.form['location']
    
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    
    # Convert industry to one-hot
    ind_edu = 1 if industry == 'Education' else 0
    ind_fin = 1 if industry == 'Finance' else 0
    ind_health = 1 if industry == 'Healthcare' else 0
    ind_retail = 1 if industry == 'Retail' else 0
    ind_tech = 1 if industry == 'Technology' else 0
    
    # Convert location to one-hot
    loc_bang = 1 if location == 'Bangalore' else 0
    loc_delhi = 1 if location == 'Delhi' else 0
    loc_hyd = 1 if location == 'Hyderabad' else 0
    loc_mum = 1 if location == 'Mumbai' else 0
    loc_rural = 1 if location == 'Rural' else 0
    loc_sub = 1 if location == 'Suburban' else 0
    loc_urban = 1 if location == 'Urban' else 0
    
    # Create DataFrame
    input_data = pd.DataFrame({
        'Status': [status],
        'Age Group': [age_group],
        'Education': [education],
        'AI Risk': [ai_risk],
        'Monthly Salary (INR)': [salary],
        'Industry_Education': [ind_edu],
        'Industry_Finance': [ind_fin],
        'Industry_Healthcare': [ind_health],
        'Industry_Retail': [ind_retail],
        'Industry_Technology': [ind_tech],
        'Location_Bangalore': [loc_bang],
        'Location_Delhi': [loc_delhi],
        'Location_Hyderabad': [loc_hyd],
        'Location_Mumbai': [loc_mum],
        'Location_Rural': [loc_rural],
        'Location_Suburban': [loc_sub],
        'Location_Urban': [loc_urban],
        'Year': [year],
        'Month': [month],
        'Day': [day]
    })
    
    # Predict
    prediction = model.predict(input_data)
    result = round(prediction[0], 1)
    
    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)