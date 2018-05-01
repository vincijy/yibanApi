#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

from flask import Flask, request, redirect, render_template

from yibanApi.raw_api import AccessToken, api

app = Flask(__name__)


@app.route('/')
def index():
    at = AccessToken(code=None)
    return redirect(at.init_url)


@app.route('/redirect')
def login():

    __code = request.args.get("code")
    at = AccessToken(code=__code)

    @at.access_by_token
    def user_me(access_token):
    	return api.user.me.get(access_token=access_token)

    @at.access_by_token
    def revoke(access_token):
    	return api.oauth.revoke_token.post(access_token=access_token, client_id=at.AppID)

    return user_me()


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=80)
