from flask import Flask, request , jsonify
from flask_restful import Api , Resource
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
usernum = db["usernum"]

usernum.insert({
    'num_of_user':0
})


# increaments the num of users every time a user visits the web page
class Visit(Resource):
    def get(self):
        prev_num = usernum.find({})[0]['num_of_user']
        new_num = prev_num + 1
        usernum.update({}, {"$set":{"num_of_user":new_num}})
        return str("hello user"+ str(new_num))

#utility method to validate  Client input
def check_postedData(Functioname , PostedData):
    if Functioname == "add" or Functioname == "Substract" or Functioname == "multiply" or Functioname == "Devide":
        if "x" not in PostedData or "y" not in PostedData :
            return 422
    else:
        return 200

#addition class and method 
class add(Resource):
    def post(self):
        PostedData = request.get_json(force = True)
        Status_Code = check_postedData("add", PostedData)
        if Status_Code != 200:
            error_json = {
                "message":"An error Occured",
                "status code ":Status_Code
            }
            return jsonify(error_json)
            
        x = PostedData["x"]
        y = PostedData["y"]
        x = int(x)
        y = int(y)
        z = x+y
        answer_json = {
            "Answer":z,
            "status code ":Status_Code
        }
        return jsonify(answer_json)


# Substraction class and method
class Substract(Resource):
    def post(self):
        Posted_Data = request.get_json(force=True)
        Status_Code=check_postedData("Substract",Posted_Data)
        if Status_Code != 200:
            error_json = {
                "message":"An error occured",
                "status code":Status_Code
            }
            return jsonify(error_json)
        x = int(Posted_Data["x"])
        y = int(Posted_Data["y"])
        z = x - y
        answer_json = {
            "answer":z,
            "status code":Status_Code
        }
        return jsonify(answer_json)

class Multiply(Resource):
    def post(self):
        Posted_Data = request.get_json(force=True)
        Status_Code = check_postedData("Multiply",Posted_Data)
        if Status_Code != 200:
            error_json = {
                "message":"an error occured",
                "status code":Status_Code
            }
            return jsonify(error_json)

        x = int(Posted_Data["x"])
        y = int(Posted_Data["y"])
        z = x *y
        answer_json = {
            "answer":z,
            "status code": Status_Code
        }
        return jsonify(answer_json)


class Devide(Resource):
    def post(self):
        Posted_Data = request.get_json(force=True)
        Status_Code = check_postedData("Devide",Posted_Data)
        print(Status_Code)
        if Status_Code != 200:
            error_json = {
                "message":"an error occured",
                "status code":Status_Code
            }
            return jsonify(error_json)
        x = int(Posted_Data["x"])
        y = int(Posted_Data["y"])
        z = x/y
        answer_json = {
            "answer":z,
            "status code": Status_Code
        }
        return jsonify(answer_json)




#add the classs to the API by using the Resource of flask_restful
api.add_resource(add,"/add")
api.add_resource(Substract,"/substract")
api.add_resource(Multiply,"/multipy")
api.add_resource(Devide,"/devide")
api.add_resource(Visit,"/hello")


#test route
@app.route("/test")
def test_route():
    return "shitt works man!!!"


if __name__ == "__main__":
    app.run(debug=True)