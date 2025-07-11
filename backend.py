from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')
    user_input = request.json.get('input', '')
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp:
        temp.write(code)
        temp_filename = temp.name
    try:
        result = subprocess.run(
            ['python', temp_filename],
            input=user_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5  # 5 seconds timeout
        )
        output = result.stdout.decode()
        error = result.stderr.decode()
    except subprocess.TimeoutExpired:
        output = ''
        error = 'Error: Code execution timed out.'
    except Exception as e:
        output = ''
        error = str(e)
    finally:
        os.remove(temp_filename)
    return jsonify({'output': output, 'error': error})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080) 