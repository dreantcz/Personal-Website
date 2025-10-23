from flask import Flask, render_template, request, redirect, url_for
import os
import DAL


# 2. Create a instance of the Flask() class with the only parameter being
#    a "system" variable called __name__. If you want to see what is in __main__
#    create a new Python program file and print it and see what it prints.
#    Call the instance/object "app"
app = Flask(__name__)

# 3. We then use the route() decorator (aka function) to tell Flask what URL should trigger our function.
#    / means the root or "top" level
@app.route("/")     # Default page when you only type the Server URL
@app.route("/home") # Explicit name when you type the Server URL and the route name
# 4. Now let’s tell the website what we should send to the person's web browser who visited our page
def hello_world():
    return """<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Home | Drew Antczak</title>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>
<header class="site-header">
<div class="container header-content">
<h1 class="logo">Drew Antczak</h1>
<nav class="navbar">
<ul>
<li><a href="/" class="active">Home</a></li>
<li><a href="/subfolder/about">About</a></li>
<li><a href="/subfolder/resume">Resume</a></li>
<li><a href="/subfolder/projects">Projects</a></li>
<li><a href="/subfolder/contact">Contact</a></li>
</ul>
</nav>
</div>
</header>


<section class="hero">
<div class="container">
<h2>Welcome to My Digital Portfolio</h2>
<p>Hi, I’m Drew — a MSIS student passionate about using data, strategy, and creativity to solve complex business challenges.</p>
<a href="/subfolder/about" class="btn">Learn More</a>
</div>
</section>


<section class="highlights container">
<div class="highlight">
<h3>Data-Driven Decision Maker</h3>
<p>Strong foundation in data analysis and business intelligence tools like Python, SQL, and Tableau.</p>
</div>
<div class="highlight">
<h3>Collaborative Leader</h3>
<p>Proven ability to work cross-functionally, helping teams align around strategy and execution.</p>
</div>
<div class="highlight">
<h3>Creative Thinker</h3>
<p>Combining analytics with design and storytelling to create meaningful business insights.</p>
</div>
</section>


<footer>
<p>&copy; 2025 Drew Antczak | <a href="mailto:dreantcz@iu.com">dreantcz@iu.com</a></p>
</footer>
</body>
</html>"""

# 5. Create another route (aka page) but this time put it in a virtual
#    subfolder called subfolder. Don't forget that when you link back to
#    the home page you have to tell Python that the home page is in the
#    parent folder.
@app.route("/subfolder/about")
def secondPage():
    return """
            <html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About | Drew Antczak</title>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>
<header class="site-header">
<div class="container header-content">
<h1 class="logo">Drew Antczak</h1>
<nav class="navbar">
<ul>
<li><a href="/">Home</a></li>
<li><a href="/subfolder/about" class="active">About</a></li>
<li><a href="/subfolder/resume">Resume</a></li>
<li><a href="/subfolder/projects">Projects</a></li>
<li><a href="/subfolder/contact">Contact</a></li>
</ul>
</nav>
</div>
</header>


<main class="container">
<section class="about-section">
<img src="/static/images/Headshot.jpg" alt="Photo of Drew Antczak" class="profile-pic large">
<div class="bio">
<h2>About Me</h2>
<p>Hello! I'm Drew Antczak, a MSIS student with a passion for turning data into actionable insights. My academic and professional experiences have shaped my ability to combine analytical rigor with creative storytelling. I believe in using data to inform smart, human-centered decisions.</p>
<p>Beyond academics, I enjoy exploring new technologies, watching films, and collaborating on projects that push boundaries in innovation and design. I’m currently seeking opportunities that let me bridge business strategy with technology implementation.</p>
</div>
</section>
</main>


<footer>
<p>&copy; 2025 Drew Antczak</p>
</footer>
</body>
</html>
            """

@app.route("/subfolder/contact", methods=['GET','POST'])
def thirdPage():
    # This page is converted to a project submission form.
    # GET -> render form; POST -> add project to database and redirect to projects page
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image = request.form.get('image', '').strip()  # expected filename present in static/images
        if title and description and image:
            DAL.add_project(title, description, image)
            return redirect(url_for('fourthPage'))
        else:
            error = 'All fields are required (Title, Description, Image filename).'
            return render_template('form.html', error=error)

    return render_template('form.html')

@app.route("/subfolder/projects")
def fourthPage():
    # Render projects from the database using a template
    projects = DAL.get_projects()
    return render_template('projects.html', projects=projects)

@app.route("/subfolder/resume")
def fifthPage():
    return """
            <html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resume | Drew Antczak</title>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>
<header class="site-header">
<div class="container header-content">
<h1 class="logo">Drew Antczak</h1>
<nav class="navbar">
<ul>
<li><a href="/">Home</a></li>
<li><a href="/subfolder/about">About</a></li>
<li><a href="/subfolder/resume" class="active">Resume</a></li>
<li><a href="/subfolder/projects">Projects</a></li>
<li><a href="/subfolder/contact">Contact</a></li>
</ul>
</nav>
</div>
</header>


<main class="container resume">
<section>
<h2>Resume</h2>
<p>Download or view my resume below:</p>
<iframe src="/static/docs/Antczak_Andrew_Resume_Raymond_James.pdf" width="100%" height="600px" title="Drew Antczak Resume PDF"></iframe>
</section>

</main>


<footer>
<p>&copy; 2025 Drew Antczak</p>
</footer>
</body>
</html>"""

@app.route("/subfolder/thankyou")
def sixthPage():
    return """
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thank You | Drew Antczak</title>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>
<header class="site-header">
<div class="container header-content">
<h1 class="logo">Drew Antczak</h1>
<nav class="navbar">
<ul>
<li><a href="/">Home</a></li>
<li><a href="/subfolder/about">About</a></li>
<li><a href="/subfolder/resume">Resume</a></li>
<li><a href="/subfolder/projects">Projects</a></li>
<li><a href="/subfolder/contact">Contact</a></li>
</ul>
</nav>
</div>
</header>


<main class="thankyou container">
<section class="thankyou-section">
<h2>Thank You!</h2>
<p>Your form has been successfully submitted. I appreciate your message and will get back to you soon.</p>
<a href="/" class="btn">Return to Home</a>
</section>
</main>


<footer>
<p>&copy; 2025 Drew Antczak</p>
</footer>
</body>
</html>"""

if __name__=='__main__':
    #app.run()
    app.run(debug=True)