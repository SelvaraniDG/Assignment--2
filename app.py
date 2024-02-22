# importing library
import csv
import pandas as pd
import numpy as np

from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# binding flask ,sqlite db and marsmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///country.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Declaring model called Country and its field with properties for sqlite db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(100), nullable=False)
    Capital = db.Column(db.String(100), nullable=False)

# Here we define that our JSON response will have two keys(Country, Capital).
# Also we defined country_schema as instance of CountrySchema, and country_schemas as instances of list of CountrySchema.


class CountrySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('Country', 'Capital')


# init schema
country_schema = CountrySchema()
country_schema = CountrySchema(many=True)


# Reading country list with capital from country_list.txt file and adding it to the sqlite database
with open('country_list.txt', 'r', encoding="utf-8") as csvfile:
    # converting string to comma seperated values
    csv_reader = csv.reader(csvfile, delimiter=",")
    # converting comma seperated value to dataframe i.e to tabular form with columns Country, Capital and temp
    df = pd.DataFrame(csv_reader, columns=['Country', 'Capital', 'temp'])
    # Concatenating column temp with Capital only when temp has value
    df['Capital'] = np.where(df['temp'].isnull(
    ), df['Capital'], df['Capital']+'('+df['temp']+')')
    # Dropping column temp
    df = df.drop(columns=['temp'])
    # adding id column with range from 0 to no of rows
    df.insert(0, 'id', range(0, 0+len(df)))
    # insert bulk data frame value to database
    df.to_sql('country', con=db.engine, index=False, if_exists='replace')
csvfile.close()

# mapping index url
@app.route('/')
def index():
    capital = Country.query.all()
    return render_template('index.html', countryList=capital)

# api to get all country capital and take country input from user
@app.route('/capital', methods=['POST', 'GET'])
def capital():

    # Searching country
    if request.method == 'POST':
        country = request.get_json()
        return redirect('/capital/'+country['country'])
    else:
        capital = Country.query.all()
        # converting to JSON
        result = country_schema.dump(capital)
        return jsonify(result)


# api to get single country capital
@app.route('/capital/<country>', methods=['GET'])
def get_capital(country):

    capital = Country.query.filter(Country.Country == country)
    capital.first_or_404(
        description='There is no Country with name {}'.format(country))
    return country_schema.jsonify(capital)


# entry point to run the application
if __name__ == '__main__':
    app.run(debug=True)
