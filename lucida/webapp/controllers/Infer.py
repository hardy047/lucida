from flask import *

from AccessManagement import login_required
from ThriftClient import thrift_client
from commandcenterlib.query_classifier import query_classifier
from commandcenterlib.utilities import log, check_image_extension

import os
import httplib2
import urllib
import string 
import random


infer = Blueprint('infer', __name__, template_folder='templates')


@infer.route('/infer', methods=['GET', 'POST'])
@login_required
def infer_route():
	options = {}
	if os.environ.get('ASR_ADDR_PORT'):
		options['asr_addr_port'] = os.environ.get('ASR_ADDR_PORT')
	else:
		options['asr_addr_port'] = 'ws://localhost:8081'
	try:
		form = request.form
		# Deal with POST requests.
		if request.method == 'POST':
			# If the request does not contain an "op" field.
			if not 'op' in form:
				raise RuntimeError('Did you click the Ask button?')
			# When the "op" field is equal to "add_image".
			elif form['op'] == 'infer':
				# Check input file.
				upload_file = request.files['file'] if 'file' in request.files \
					else None
				if not upload_file is None and upload_file.filename != '':
					check_image_extension(upload_file)
				# Classify the query.
				speech_input = form['speech_input'] if 'speech_input' in form \
					else ''
				print '@@@@@@@@@@', speech_input
				services_needed = \
					query_classifier.predict(speech_input, upload_file)
				options['result'] = thrift_client.infer(session['username'], 
					services_needed, speech_input, upload_file.read()
					if upload_file else None)
                                options['result_audio'] = get_audio(options['result'])
				log('Result ' + options['result'])
				# Check if Calendar service is needed.
				# If so, JavaScript needs to receive the parsed dates.
				if services_needed.has_service('CA'):
					options['dates'] = options['result']
					options['result'] = None
					return render_template('infer.html', **options)
			else:
				raise RuntimeError('Did you click the Ask button?')
	except Exception as e:
		log(e)
		if str(e) == 'TSocket read 0 bytes':
			e = 'Back-end service encountered a problem'
		options['error'] = e
		return render_template('infer.html', **options)
	# Display.
	return render_template('infer.html', **options)

def get_audio(input_text):
    mary_host = "localhost"
    mary_port = "59125"
    query_hash = {"INPUT_TEXT":input_text,
              "INPUT_TYPE":"TEXT", # Input text
              "LOCALE":"en_US",
              "VOICE":"cmu-slt-hsmm", # Voice informations  (need to be compatible)
              "OUTPUT_TYPE":"AUDIO",
              "AUDIO":"WAVE", # Audio informations (need both)
              }
    query = urllib.urlencode(query_hash)
    h_mary = httplib2.Http()
    resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)
    if (resp["content-type"] == "audio/x-wav"):
        # Write the wav file.
        clean_voice_dir()
        filename = id_generator() + '.wav'
        filepath = 'static/music/' + filename
        f = open(filepath, "wb")
        f.write(content)
        f.close()
    return filename


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def clean_voice_dir():
    for f in os.listdir("./static/music"):
        file_path = os.path.join("./static/music", f)
        try:
            os.remove(file_path)
        except Exception as e:
            pass

