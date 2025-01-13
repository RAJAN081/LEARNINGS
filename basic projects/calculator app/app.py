from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)
# Function to evaluate mathematical expressions
def calculate_expression(expression):
    try:
        # Evaluate the expression securely
        result = eval(expression, {"__builtins__": None}, {
            "sqrt": math.sqrt, "pow": math.pow, "abs": abs, "round": round,
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log
        })
        return result
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    result = calculate_expression(expression)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
