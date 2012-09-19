from flask import Flask, request, render_template, url_for, make_response, Response, send_from_directory
from collections import Counter
import urllib2, simplejson, re, io, sys, os
from StringIO import StringIO

app = Flask(__name__)

def filterLists(arr):
    resp = []
    ans = []
    for i in arr:
        i = re.sub('[^A-Za-z0-9.]+', '', i)
        resp.append(i)
    for j in resp:
        ans.append(str(j.lower()))
    return ans

def fetch_tweets(handle):
	url = "http://api.twitter.com/1/statuses/user_timeline.json?suppress_response_codes&trim_user=true&include_entities=false&include_rts=true&exclude_replies=true&count=1000&screen_name=" + handle
	data = urllib2.urlopen(url)
	js = simplejson.load(data)
	tweets = []
	for k in js:
		tweet = k['text']
		count = filterLists(tweet.split())
		tweets.append(len(count))
	d = {}
	for j in tweets:
		d[j] = d.get(j, 0) + 1
	resp = []
	tup = sorted(d.items(), reverse=False)
	result = []
	for i in tup:
		result.append(i)
	return result

@app.route("/")
def index():
	handle = request.args.get('handle', None)
	if not handle:
		return render_template('index.html')
	else:
		d = fetch_tweets(handle)
	return render_template('result.html', ans=d)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
