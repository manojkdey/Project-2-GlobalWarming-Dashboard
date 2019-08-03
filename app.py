import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///db/globalWarming')
print (engine.table_names())



#################################################
# Database Setup
#################################################
#- Following line is to suppress the following message 
#- warnings.warn('SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  
#- Set it to True to suppress this warning.')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/globalWarming"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
GlobalCO2Emission = Base.classes.GlobalPercapitaCO2Emission
Samples = Base.classes.GlobalMnTemp
Samples_Metadata = Base.classes.GlobalMnTemp



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")




@app.route("/names")
def names():
    """Return a list of sample names."""

   # # Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

   # # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

   # selYear = [
   #     Samples.Year,
   # ]

   # Years = db.session.query(*selYear).all()
   # return jsonify(list(Years))

   
@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.Year,
        Samples_Metadata.Jan,
        Samples_Metadata.Feb,
        Samples_Metadata.Mar,
        Samples_Metadata.Apr,
        Samples_Metadata.May,
        Samples_Metadata.Jun,
        Samples_Metadata.Jul,
        Samples_Metadata.Aug,
        Samples_Metadata.Sep,
        Samples_Metadata.Oct,
        Samples_Metadata.Nov,
        Samples_Metadata.Dec,
        Samples_Metadata.DJF,
        Samples_Metadata.MAM,
        Samples_Metadata.JJA,
        Samples_Metadata.SON,
        Samples_Metadata.Jun,
    ]

    #results = db.session.query(*sel).filter(Samples_Metadata.Year == sample).all()
    results = db.session.query(*sel).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["Year"] = result[0]
        sample_metadata["Jan"] = result[1]
        sample_metadata["Feb"] = result[2]
        sample_metadata["Mar"] = result[2]
        sample_metadata["Apr"] = result[4]
        sample_metadata["May"] = result[5]
        sample_metadata["Jun"] = result[6]
        sample_metadata["Jul"] = result[7]
        sample_metadata["Aug"] = result[8]
        sample_metadata["Sep"] = result[8]
        sample_metadata["Oct"] = result[10]
        sample_metadata["Nov"] = result[11]
        sample_metadata["Dec"] = result[12]
        sample_metadata["DJF"] = result[13]
        sample_metadata["MAM"] = result[14]
        sample_metadata["JJA"] = result[15]
        sample_metadata["SON"] = result[16]
        sample_metadata["Jun"] = result[17]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return ``Year`,'Dec', 'DJF', 'MAM', 'JJA', 'SON', 'and `Dec`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df['Year'] < 2019, ["Year", sample]]
    sample_data.columns = ['Year', 'tempAnnamolies']
    sample_data['Month']=sample
    
    #sample_data['tempAnnamolies']=sample_data['tempAnnamolies'] * 10
    # Sort by sample
    sample_data.sort_values(by="Year", ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "Year": sample_data.Year.values.tolist(),
        "tempAnnamolies": sample_data.tempAnnamolies.values.tolist(),
         "Month": sample_data.Month.tolist(),
    }
    print(data)
    return jsonify(data)



if __name__ == "__main__":
    app.run()