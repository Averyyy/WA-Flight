# WA-Flight
Final project for Database
[![Watch the video](https://i.imgur.com/vKb2F1B.png)](https://youtu.be/L46pCk0sd7k)

0. Before you read:
  This is a project wrote by Wendy and me and we only had about one week part time to finish it(with other things like learning and taking exams). Since that the time is very limited and we admit there are a lot that can be improved and we tried our best to add more functions and fix bugs. Anyways, Please enjoy reading! 
  
1. Overview
There are mainly two py files that control the whole WA Flight booking system. The APP.py connects the Database SQL and controls the htmls. The query utility function connects cursor, executes query retrieves and formats data. All htmls are in the templates file and css code is in the static file. 
The remaining part of the document describes the parts done by Avery & Wendy.

2.Hangkai Qian(Avery)’s Part

Most of the HTML Parts, including public_view, homepage customer, booking agent, sign_out, which includes form setting, position designing, and navbar, etc. of all the pages. 
All the CSS codes. (background designing, form styling, button animation styling, table formatting (animation styling, etc. ) 
3 Sign in functions (customer, agent, staff), including sign in function check. App.py gets information from different form names and I used a function to check if the attributes have something and direct to where they belong to. When directing to the customer home, for instance, it will check if the attributes are valid. If not, redirect to the sign in page, otherwise go to the home page. Same logic in booking agent and airline staff. 
Some of customer_home/agent_home in the flask app (related to sign in redirecting and error handling as explained above. 
All the staff part,  including creating new flights, updating status, creating airplanes and  other things. In this part, with a single “Edit flight ” button, you can easily do the three functions. The flask app of staff home will automatically decide which function you want to use through several if statements to check if the element satisfies all the requirements of the function. For example, if you entered flight number, price, departure time, arrival time, departure city, arrival city, etc.  , the function will know you want to create a flight and a create_flight function in the query utility will be executed. If status and flight number is entered, then it will know you want to change the status of a flight. Other functions work the same. 
Finalize and fix final bugs of the project, including registering airline staff(turned out to be html name error due to a gitHub merge), redirecting to the index when finish purchase the ticket(redirect error), and booking agent purchasing the ticket(turned out to be the route of html page is wrong to customer_home), airline staff edit flight decision error, and all other bugs. 

3. Wendy’s Part

#
Topics
Summary of the logic
Functions
Comments
Home page
Direct users to Public View page/ Sign in/ Sign up page
App.py:
init_app():

2.
Public view and filters
Default presents of all the upcoming flights in the public view page/ customer/ agent/ staff homepage, user can search flight on giving out filtering conditions. 
App.py:
def public_view(conn):
Query utility
public_view(conn)
filter_result(conn,html_get):

If the html request method is ‘GET’, the public_view function in Query utility will be executed which retrieves all upcoming flights and presents them in the html table. User could select conditions to filter the results and this triggers the ‘POST’ method. The corresponding result will be retrieved and passed to html table. 
3. 
Session
Reinforce the safety by adding session.clear ()  in both the log out part and whenever the user is returning to the root page.
Implemented a function to loop dictionary and save info into session
session.clear ()
Clear all the information stored in session
App.py: 
save_to_session(info_cus)
loop dictionary and save info into session
4. 
Sign up 
All three roles share one sign up page but they are required to fill out different info by clicking their corresponding tab
On filling all the necessary information and clicking sign up button, back end checks the logic
Registration validation check
Registration validation check
If sign up input is valid
Execute user add 
App.py: Usertype check 
Sign_up()
Grab all information from html, based on input information, determine the user type (i.e.) airline_name input indicate usertype: staff; meanwhile save all info into session
Query utility.py:
Validation check
reg_validation_cus(conn,session)
reg_validation_ba(conn,session)
reg_validation_as(conn,session)
Execute SQL to check whether the username/ email is already registered as user
Query utility.py:
Insert new user
add_cus(conn, session)
add_ba(conn, session)
add_as(conn, session):
If the user input pass the validation check, the insearsion of signup information passed using session will be formatted and executed in database
5.
Daytime Utility 
Utility functions that returns
Formatted date fitting SQL syntax
Giving back a datetime range for a selected date
Giving back period for month/ year
Query utility.py:
getting_date()
formatting_date(year,month,date)
getting_period(day)
getting_past_month_period(year,month,day)
getting_past_year_period(year,month,day)/
Mainly to solve the inconsistency of the front-end of a particular date to filter flight but the backend flight departure/ arrival time saved in datetime format.

END


