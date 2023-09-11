from flask import Flask, jsonify
import re
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

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

@app.route('/input_cleansing', methods=['POST'])
@swag_from('./docs/input.yml')
def clean():
	Teks = request.form['Teks']
	Teks = Teks.lower()
	Teks = re.sub('rt',' ',Teks)
	Teks = re.sub('RT',' ',Teks)
	Teks = re.sub(r'@[^\s]+','',Teks)
	Teks = re.sub(r'@','',Teks)
	Teks = re.sub('USER','',Teks)
	Teks = re.sub('user','',Teks)
	Teks = re.sub(r'https?://\S+|www\.\S+', '', Teks)
	Teks = re.sub ('URL', '', Teks)
	Teks = re.sub ('url', '', Teks)
	Teks = re.sub(r'[^\w\s]',' ',Teks)
	Teks = re.sub("\S*\d\S*", "", Teks).strip()
	Teks = re.sub(r"\b\d+\b", " ", Teks)
	Teks = re.sub('  +', ' ', Teks)

	return jsonify({'cleaned_data': Teks})

if __name__ == '__main__':
	app.run()