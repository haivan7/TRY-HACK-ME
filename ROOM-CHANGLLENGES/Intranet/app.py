from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, render_template_string, send_file
from time import gmtime, strftime
import jinja2, os, hashlib, random

app = Flask(__name__, template_folder="/home/devops/templates")


###############################################
# Flag: THM{4ccacfd73710ac18b4ac15646b32380a} #
###############################################


key = "secret_key_"   str(random.randrange(100000,999999))
app.secret_key = str(key).encode()

def check_hacking_attempt(value):

        bad_chars = "#&;'\""
        error = ""

        if any(ch in bad_chars for ch in value):
                error = "Hacking attempt detected! "
                error  = "You have been logged as "
                error  = request.remote_addr
                return True, error

        else:
                return False, error


@app.route("/robots.txt", methods=["GET"])
def robots():
        return "<!-- Try harder --!>"



@app.route("/", methods=["GET"])
def root():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                return redirect("/home")


@app.route("/application", methods=["GET"])
def application():
        return abort(403)


@app.route("/application/console", methods=["GET"])
def console():
        return abort(403)


@app.route("/temporary", methods=["GET"])
def temporary():
    return abort(403)


@app.route("/temporary/dev", methods=["GET"])
def dev():
        return abort(403)


@app.route("/login", methods=["GET", "POST"])
def login():

        if session.get("logged_in"):
                return redirect("/home")

        if request.method == "POST":

                username = request.form["username"]
                attempt, error = check_hacking_attempt(username)
                if attempt == True:
                        error  = ". (Detected illegal chars in username)."
                        return render_template("login.html", error=error)

                password = request.form["password"]
                attempt, error = check_hacking_attempt(password)
                if attempt == True:
                        error  = ". (Detected illegal chars in password)."
                        return render_template("login.html", error=error)


                if username.lower() == "admin@securesolacoders.no":
                        error = "Invalid password"
                        return render_template("login.html", error=error)


                if username.lower() == "devops@securesolacoders.no":
                        error = "Invalid password"
                        return render_template("login.html", error=error)


                if username.lower() == "anders@securesolacoders.no":
                        if password == "securesolacoders2022":
                                session["username"] = "anders"

                                global sms_code
                                sms_code = random.randrange(1000,9999)

                                return redirect("/sms")
                        
                        else:
                                error = "Invalid password"
                                return render_template("login.html", error=error)
                else:
                        error = "Invalid username"
                        return render_template("login.html", error=error)

        return render_template("login.html")



@app.route("/sms", methods=["GET", "POST"])
def sms():

        if session.get("username"):
                if request.method == "POST":
                        sms = request.form["sms"]

                        if sms == str(sms_code):
                                session["logged_in"] = True
                                return redirect("/home")
                        else:
                                error = "Invalid SMS code"
                                return render_template("sms.html", error=error) 


                return render_template("sms.html")
        else:
                return redirect("/login")



@app.route("/logout", methods=["GET"])
def logout():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                session.clear()
                return redirect("/login")


@app.route("/home", methods=["GET"])
def home():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                current_ip = request.remote_addr

                templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
                templateEnv = jinja2.Environment(loader=templateLoader)
                t = templateEnv.get_template("home.html")
                return t.render(current_ip=current_ip)


@app.route("/admin", methods=["GET", "POST"])
def admin():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                if session.get("username") == "admin":

                        if request.method == "POST":
                                os.system(request.form["debug"])
                                return render_template("admin.html")

                        current_ip = request.remote_addr
                        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                        return render_template("admin.html", current_ip=current_ip, current_time=current_time)
                else:
                        return abort(403)


@app.route("/internal", methods=["GET", "POST"])
def internal():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                if request.method == "POST":
                        news_file = request.form["news"]
                        news = open("/opt/news/{}".format(news_file)).read()
                        return render_template("internal.html", news=news)

                return render_template("internal.html")


@app.route("/external", methods=["GET"])
def external():
        if not session.get("logged_in"):
                return redirect("/login")
        else:
                templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
                templateEnv = jinja2.Environment(loader=templateLoader)
                t = templateEnv.get_template("external.html")
                return t.render()


if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8080, debug=False)
