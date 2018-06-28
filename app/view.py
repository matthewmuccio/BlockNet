#!/usr/bin/env python3


import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app


# Stores the node's address.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
# Stores all the posts in the node.
posts = []

# Gets the data from node's /chain endpoint, parses the data, and stores it locally.
def fetch_posts():
	get_chain_address = "{0}/chain".format(CONNECTED_NODE_ADDRESS)
	response = requests.get(get_chain_address)
	if response.status_code == 200:
		content = []
		chain = json.loads(response.content.decode("utf-8"))
		for block in chain["chain"]:
			for tx in block["transactions"]:
				tx["index"] = block["index"]
				tx["hash"] = block["previous_hash"]
				content.append(tx)
		global posts
		posts = sorted(content, key=lambda k: k["timestamp"], reverse=True)

# Creates a new endpoint, and binds the function to the URL.
@app.route("/")
# Renders the index.html (home page).
def index():
	fetch_posts()
	return render_template("index.html", \
				title="BlockNet", \
				subtitle="A Decentralized Network for Content Sharing", \
				posts=posts, \
				node_address=CONNECTED_NODE_ADDRESS, \
				readable_time=timestamp_to_string)

# Creates a new endpoint, and binds the function to the URL.
@app.route("/submit", methods=["POST"])
# The endpoint to create a new tranaction.
def submit_textarea():
	post_content = request.form["content"]
	author = request.form["author"]
	post_object = {
		"author" : author,
		"content" : post_content,
	}
	# Submit a new transaction.
	new_tx_address = "{0}/new_transaction".format(CONNECTED_NODE_ADDRESS)
	requests.post(new_tx_address, json=post_object, headers={"Content-type" : "application/json"})
	return redirect("/")

# Converts a timestamp (in UNIX time) to a string.
def timestamp_to_string(unix_time):
	return datetime.datetime.fromtimestamp(unix_time).strftime("%H:%M")
