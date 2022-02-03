from flask import Flask, request, jsonify, Response
from simplet5 import SimpleT5
import pickle
from dotenv import load_dotenv
import os

# load model
with open(r"simplet5.pickle", "rb") as input_file:
	model = pickle.load(input_file)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# set env for secret key
load_dotenv()

secret_id = os.getenv('AI_SERVICE_SECRET_KEY')

# print(secret_id)
def check_for_secret_id(request_data):    
    try:
        if 'secret_id' not in request_data.keys():
            return False, "Secret Key Not Found."
        
        else:
            if request_data['secret_id'] == secret_id:
                return True, "Secret Key Matched"
            else:
                return False, "Secret Key Does Not Match. Incorrect Key."
    except Exception as e:
        message = "Error while checking secret id: " + str(e)
        return False,message

@app.route('/StoryTeller',methods=['POST'])  #main function
def main():
    params = request.get_json()
    input_query=params["data"]
    keywords = input_query[0]['keywords']
    key = params['secret_id']

    request_data = {'secret_id' : key}
    secret_id_status,secret_id_message = check_for_secret_id(request_data)
    print ("Secret ID Check: ", secret_id_status,secret_id_message)
    if not secret_id_status:
        return jsonify({'message':"Secret Key Does Not Match. Incorrect Key.",
                        'success':False}) 
    else:
    	result = model.predict(keywords)
    return jsonify({'Story':result[0]})

if __name__ == "__main__":    
    app.run()
