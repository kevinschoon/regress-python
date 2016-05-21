## regress-python [regress.vektor.nyc](http://regress.vektor.nyc)

Regress performs simple linear regression against an uploaded data set.

The uploaded dataset is expected to be in csv format similar to
the examples in the `sample_data` directory:

    $ head sample_data/Housing.csv
    $ head -n 3 sample_data/Housing.csv
    "","price","lotsize","bedrooms","bathrms","stories","driveway","recroom","fullbase","gashw","airco","garagepl","prefarea"
    "1",42000,5850,3,1,2,"yes","no","yes","no","no",1,"no"
    "2",38500,4000,2,1,1,"yes","no","no","no","no",0,"no"

When uploading the CSV you must specify a `name`, `x_field`, `y_field`, optionally you
may also specify a `description`.


### Running Locally

    $ docker build -t regress-python .
    $ docker run -d -p 8000:8000 regress-python --w 2 -b 0.0.0.0:8000 regress.main:app
    # Load some sample data
    $ cd sample_data
    $ curl -XPOST -H "Content-Type: multipart/form-data" -F "name=Housing Data" -F "description=Housing Prices vs Lot Size" -F "x_field=price" -F "y_field=lotsize" -F "file=@Housing.csv" "http://localhost:8000/upload"


### Original Requirements

* A web app run from AWS
* User can access web-based service via a web browser, containing a simple front end
* User can upload a file
* file contains two columns (x and y data) that follow a linear relationship with each other (with some noise)
* File is uploaded to a database in AWS
* User can run linear regression, where x is the input and y is the output
* Ideally use R to run the regression, but you can use Python instead
* User can download a file which is the same as the original file, but with an additional column which are estimated y values generated using the model for each value of x in the table
* Code is checked into github, or something similar, so it can be viewed to showcase your coding

###### Nice to have
* Once the input file is uploaded, the user can ask the web front end to display the input data table loaded in the database
* Once the regression is run, the web front end plots the actual (x & y) data points as well as the (x & estimated y) data points.
