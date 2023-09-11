from flask import Flask, jsonify
import re
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder

swagger_template = {
	"swagger":"2.0",
	"info":{
		"title": "API Documentation for Data Processing and Modelling",
		"description": "Dokumentasi API untuk Data Processing dan Modelling",
		"version": "1.0.0"
	} 
}

swagger_config = {
	"headers" : [],
	"specs" : [
		{
			"endpoint" : 'docs',
			"route" : '/docs.json'
		}
	],
	"static_url_path" : '/flasgger_statis',
	"swagger_ui" : True,
	"specs_route" : "/docs/"
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.route('/upload_csv', methods=['POST'])
@swag_from('./docs/upload_csv.yml')
def upload_csv():
    file = request.files.getlist['file']
    file = pd.read_csv(file, sep=',', encoding="latin-1")
    file = file.lower()
	file = re.sub('rt',' ',file)
	file = re.sub('RT',' ',file)
	file = re.sub(r'@[^\s]+','',file
	file = re.sub(r'@','',file)
	file = re.sub('USER','',file)
	file = re.sub('user','',file)
	file = re.sub(r'https?://\S+|www\.\S+', '', file)
	file = re.sub ('URL', '', file)
	file = re.sub ('url', '', file)
	file = re.sub(r'[^\w\s]',' ', file)
	file = re.sub("\S*\d\S*", "", file).strip()
	Teks = re.sub(r"\b\d+\b", " ", file)
	file = re.sub('  +', ' ', file)
    return jsonify({'cleaned_data': file.to_json})

if __name__ == '__main__':
	app.run()
	