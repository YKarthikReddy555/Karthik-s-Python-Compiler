from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    if not request.is_json:
        return jsonify({'output': '', 'error': 'Invalid request: JSON body required.'}), 400
    data = request.get_json()
    code = data.get('code', '')
    user_input = data.get('input', '')
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
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port) 