from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def bmi_calculator():
    bmi_result = None
    if request.method == "POST":
        weight_unit = request.form["weight_unit"]
        height_unit = request.form["height_unit"]
        
        # Get weight and height values
        weight = float(request.form["weight"])
        height_ft = float(request.form["height_ft"])
        height_inch = float(request.form["height_inch"])
        
        # Convert weight to kilograms if necessary
        if weight_unit == "pounds":
            weight = weight * 0.453592
        
        # Convert height to meters if in feet and inches
        if height_unit == "feet_inches":
            height_in_meters = (height_ft * 0.3048) + (height_inch * 0.0254)
        else:
            height_in_meters = height_ft  # Assuming it's already in meters if not feet_inches
        
        # Calculate BMI
        bmi = weight / (height_in_meters * height_in_meters)
        bmi_result = round(bmi, 2)
    
    return render_template("index.html", bmi_result=bmi_result)

if __name__ == "__main__":
    app.run(debug=True)
