from flask import Flask, redirect, request
import requests
#import requests.auth
application = Flask(__name__)

client_id = r"4Z3XRVHJ0N0LO12D3HJTOAA0LRJBBFS3NJCXAO42DBOZTBMZ"
secret_key = r"XUYACFXFKORZTKTJJI21PQWOMV5PADV3N0TNOATU2OJIM2R4"

redirect_uri = r"http://127.0.0.1:5000/app"
redirect_uri2 = r"http://127.0.0.1:5000/app2"

@application.route("/")
def index():
    url = r"https://foursquare.com/oauth2/authenticate"
    resp_type = "code"
    reqtext = url + "?" + "client_id=" + client_id + "&response_type=" + resp_type + "&redirect_uri=" + redirect_uri
    return redirect(reqtext, 302)

@application.route("/app", methods=['GET', 'POST'])
def app():
    if request.method == "POST":
        return request.data
    else:
        code = request.args.get('code')

        if code is None:
            return "bad request"

        k = requests.get('https://foursquare.com/oauth2/access_token?client_id=' + client_id + '&client_secret=' + secret_key + '&grant_type=authorization_code' + '&redirect_uri=' + redirect_uri2 + '&code=' + code)
        if k.status_code/100 != 2:
            return "Internal request error"
        access_token = k.json()["access_token"]


        url = r'https://api.foursquare.com/v2/users/self/lists?oauth_token=' + access_token + '&v=20141217'
        
        response = requests.get(url)
        if response.status_code/100 != 2:
            return "Internal request error"
        return response.text

@application.route("/app2", methods=['GET', 'POST'])
def app2():
    if request.method == "POST":
        return 'test'
    else:
    	return 'hi'

if __name__ == "__main__":
    application.run()
