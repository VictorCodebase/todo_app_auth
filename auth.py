
"""
*Some key terms you might need to be familiar with getting to this:
*
* Libraries: Pre-written code that you can download (using: pip install library-name) and use in our code to make work easier
* 
* Frameworks take the concepts of libraries a step further. They bundle together libraries and other tools a developer might need to develop
* a solution of a certain nature. Some examples youll definitely come across are: Flask(python), Node(JS), Django(python)... You can check them out
*
* SQL (Standard Query Language) is a scripting language used to work with databases like SQLite, mySQL, MariaDb etc
* SQL syntax tends to differ differently from db to db depending on what features the database supports
* 
"""



# sqlite3 is a library that allows python to easily create and interact with SQLite databases.
# To use this you mut have at one point in this project ran: pip install sqlite3 (if you experience issues installing, try using a virtual environment)
import sqlite3 

# flask is a framework. From this you can see it offers a number of libraries all packed together (these are not all the libraries in flas definitely)
# 1. Session is a library that handles user sessions. Our server is NOT STATELESS. Meaning we keep track of who accesses the website by requiring a login
# 2. redirect is a library that has code that enable you (the dev) to redirect a user. So lets say a user tries to access a page they shouldn't, you can redirect them away
# 3. render_template is a special one. to use this, you html must be in a folder in this code called: templates. if not render template wont help you
# 4. Finall request gives you the ability to read what has been sent in the body of the message sent using POST
from flask import Flask, session, redirect, render_template, request


#Here we create an instance of flask. This shall make it possible for us to easily manage the backend. 
#To appreciate how much easier Flask makes this whole process, try checking out the manual process💔💔
app = Flask(__name__) 


# This is necessary for session management. It should generally be kept safe
app.secret_key = "fdsinH839dwefdsosidU23we2ewdws_ewds" 



# Ensure the database is available before anything
def init_db():

    # We create a python variable connection. This shall store the connection between python and the specified db (users.db)
    connection = sqlite3.connect("users.db")

    # The cursor method in sqlite3 gives you all you need to run SQL scrips within python!
    # Thats why its the first variable we create after connection
    cursor = connection.cursor()

    # Extra info: a database is made up of multiple tables. think of them as pages in a book. Each page stores its own unique records
    #
    # Here cursor runs this SQL script. It creates 2 empty tables. Notice that it does not add any data to the tables
    # Notice that the table tasks has the line "FOREIGN KEY (user_id) REFERENCES users(id)"
    # This line can be interprated this way:
    #   - FOREIGN KEY (user_id): this means the column user_id matches (references) another column in another table
    #   - REFERENCES users(id): this specifies that the id in the user_id matches with the column called id, in the table called users
    #
    # The other lines shouldnt be too hard to decipher
    # 
    # Extra info: this ensures that we are sure the tables exist in the database before we try reading or modifying them

    cursor.executescript(''' 
        CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
                         
        CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
    );
    '''
    )

    # here the code SQL you wrote above is ran, afterwards the database connection is closed
    # closing the db connection allows other processes to have access to the db
    # two processes cannot modify the db at the same time, so as long as you havent closed the db, other processes cannot access it
    connection.commit()
    connection.close()

# this must run before you try running any code that will try to access the db
init_db()



# Route for http://localhost:5000/login
# Here is the first route (order doesnt matter too much). this will be triggered when the client sends the route: http://localhost:5000/login
# The client sends this when a form with the action="/login" property is submitted
# This route also specifies that it ONLY expects the form to have the attribute method="POST"
@app.route("/login", methods=["POST"])
def login():

    # The imported library, requests, now comes in handy hapa
    # request.form["username"] expects that in the form you submitted, there is an input with name="username"
    # the value of that input shall be taken and fed into the variable username

    username = request.form["username"]
    password = request.form["password"] # It is very dangerous to store passords in the db without hasing them first. You could try ensuring youve hashed this first as a neat little exercise

    # The process here is very similar to what happens in the function init_db()
    # we establish connection with users.db and then set up cursor
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()


    # this is another SQL statement that we are running
    # this fetches the value of the id for a user whose username and password matches whta we have in the respective variables
    # the .fetchone() signifies that the db will return the first match it gets since we dont expect overlapping users
    user = cursor.execute("SELECT id FROM users WHERE username = ? AND PASSWORD = ?", (username, password)).fetchone()
    connection.close()

    # The variable user is not empty only if a user with matching credentials was found. If it is empty, then no such user exists
    if (user):
        # Checkout these prints to get why we are interested with the value of user[0], not just user
        print("User value is: ", user)
        print("User[0] value is: ", user[0])
        
        # Now that the user is logged in, we use the session library to tell the browser that user of a certain index is verified and they can have a session with the server
        session["user_id"] = user[0]

        # Here you see redirect library in action. Since the user has logged in, we can automatically take them to the page they were interested in
        return redirect("/todo")
    return ("invalid credentials")


# route for http://localhost:5000/signup
# In this bado we will be running another SQL statement
# This adds a new user to the db
@app.route("/signup", methods=["POST"])
def signup():

    # Here we shall use the request library just as last time to pick user inputs from their form. check line 96 - 101 for more info
    username = request.form["username"]
    password = request.form["password"]  # Again, it is very dangerous to handle passwords like this, research on how to make this secure

    # Again, we establish connection and use cursor to access some SQL runnning commands
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # this is a try-except block. 
    # the code in the try catch block is run first to observe errors. If no errors, it is ran to execute.
    # it ensures that the code failes gracefully (without breaking)
    # It is a good way handle any errors. in this case, an error we are looking for is where a username that is already signed up tries to signup again
    try:

        # Here is where we run the SQL to add data to the db
        # Breakdown of the line: 
        #   INSERT INTO users (username, password) - this bit instructs the db that the columns username and password will get values
        #   VALUES (?, ?) - in this part, always ensure the number of question marks matches the number of values that will be added. this lets the db know how many values you are adding
        #   (username, password) - in this line, we pass the values in the variables username and password to SQL for exectuion
        # Note that the order in (username, password) is important
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()


        #Here is the error we expect to get if a user is signing up, and they are already signed up
        # the db will raise an integrity error
    except sqlite3.IntegrityError:
        connection.close()
        return "Username already exists, try another."

    connection.close()
    return redirect("/todo")


# Route for http://localhost:5000/todo
@app.route("/todo")
# Here, we check whether the user is in session before allowing them to access the page
# if they are not logged in, they are redirected to the login page
def todo():
    if "user_id" not in session:
        return redirect("/")
    
    return render_template("/todo.html")


# route for http://localhost:5000/
# this is the default route to people coming to the page
# we want peopole coming here to be redirected to login if they have no session. 
# However, if they have a session, they are redirected to the /todo page
@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/todo")
    
    return render_template("/login.html")


#Run the app
app.run(debug=True)