from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Task Analyzer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #4285f4; }
        textarea { width: 100%; height: 100px; padding: 10px; margin: 10px 0; }
        button { background: #4285f4; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #357abd; }
        .result { background: #f1f3f4; padding: 20px; margin-top: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>🚀 Smart Task Analyzer</h1>
    <p>Powered by Google Gemini AI on Cloud Run</p>
    <form id="taskForm">
        <textarea id="taskInput" placeholder="Enter your task description..."></textarea>
        <button type="submit">Analyze Task</button>
    </form>
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('taskForm').onsubmit = async (e) => {
            e.preventDefault();
            const task = document.getElementById('taskInput').value;
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = 'Analyzing...';
            resultDiv.style.display = 'block';
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task: task})
            });
            const data = await response.json();
            resultDiv.innerHTML = '<h3>Analysis:</h3><pre>' + data.analysis + '</pre>';
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    task = data.get('task', '')
    
    prompt = f"""Analyze this task and provide:
1. Priority Level (High/Medium/Low)
2. Estimated Time to Complete
3. Key Steps to accomplish it
4. Potential Challenges

Task: {task}"""
    
    try:
        response = model.generate_content(prompt)
        return jsonify({'analysis': response.text})
    except Exception as e:
        return jsonify({'analysis': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
