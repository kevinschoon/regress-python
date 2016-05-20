### regress-python

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