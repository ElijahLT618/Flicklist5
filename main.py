from flask import Flask, request, redirect
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True

header = """
<!DOCTYPE html>
<html>
    <head>
        <title>Studio Flicklist 3</title>
    </head>
    <body>
        <h1>Studio Class 5</h1>
"""
footer = """
    </body>
</html>
"""

add_form = """
    <form action="/add" method="post"
        <label>
            I want to add
            <input type="text" name="new-movie"/>
            to my watchlist
        </label>
        <input type="submit" value="Add It"/>
    </form>
"""
def get_current_watchlist():
    return [ "28 Days Later", "I am Legend", 
            "ShawShank Remtempation", "Goodwill Hunting", "war of the Worlds" ]

crossoff_options = ""
for movie in get_current_watchlist():
    crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

crossoff_form = """
    <form action="/crossoff" method="POST">
        <label>
            I want to cross off
            <select name="crossed-off=movie"/>
                {0}
            </select>
            from my watchlist
        </label>
        <input type="submit" value="Cross It Off"/>
    </form>
""".format(crossoff_options)

bad_movies = [
        "Grease",
        "Pitch Perfect 2",
        "Coraline",
        "Twlight",
        "IT chapter two"
]

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        error="'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        return redirect("/?error=" + error)
    
    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + "has been crossed off your Watchlist."
    content = header + "<p>" + confirmation + "</p>" + footer

    return content 
    
@app.route("/add", methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']

    new_movie_element = "<strong>" + new_movie + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist!"
    content = header + "<p>" + sentence + "</p>" + footer

    return content

@app.route("/")
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = '<p class="error">' + error_esc + '</p>'
    else:
        error_element = ''
    
    main_content = header + add_form + crossoff_form + error_element
    
    content = header + main_content + footer
   
    return content

app.run()