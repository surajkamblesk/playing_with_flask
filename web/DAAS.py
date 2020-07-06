'''
    Author : Suraj Kamble
    Date   : 5/07/2020
    Description : Database As A Service Using Flask.

'''
from flask import Flask, request , jsonify
from flask_restful import Api , Resource
from pymongo import MongoClient
import bcrypt
app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        posteddata = request.get_json(force=True)

        username = posteddata["username"]
        password = posteddata["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        users.insert({
            "Username":username,
            "password":hashed_pw,
            "Senetence":"",
             "tokens":6
        })

        retJson = {
            "status code": 200,
            "message": "successfully signed up "
        }

        return jsonify(retJson)

def verifyPw(username,password):
    hashed_pw = users.find({
        "username":username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens

class Store(Resource):
    def post(self):
        posteddata = request.get_json(force=True)

        username = posteddata["username"]
        password = posteddata["password"]
        sentence = posteddata["sentence"]

        correct_pw = verifyPw(username,password)
        if not correct_pw:
            login_error_json = {
                "staus code":302
            }
            return jsonify(login_error_json)

        #verify user has enough token 
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            token_error_json ={
                "status code": 301
            }
            return jsonify(token_error_json)
        
        users.update({
            "Username":username
        },{
            "$set":{
                "Sentence":sentence,
                "Tokens": num_tokens - 1
                }
        })

        sentence_saved_json = {
            "status code": 200,
            "message": "sentence saved successfully"
        }
        return jsonify(sentence_saved_json)

api.add_resource(Register,"/register")
api.add_resource(Store,"/store")

if __name__ == "__main__":
    app.run(debug=True)

