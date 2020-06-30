from flask import Flask, request , jsonify
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app)

#utility method to validate  Client input
def check_postedData(Functioname , PostedData):
    if Functioname == "add" or Functioname == "Substract" or Functioname == "multiply":
        if "x" not in PostedData or "y" not in PostedData:
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


#add the classs to the API by using the Resource of flask_restful
api.add_resource(add,"/add")
api.add_resource(Substract,"/substract")

#test route
@app.route("/test")
def test_route():
    return "shitt works man!!!"


if __name__ == "__main__":
    app.run(debug=True)