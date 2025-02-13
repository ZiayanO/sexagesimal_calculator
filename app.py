from flask import Flask, render_template, request

app = Flask(__name__)

def parse_sexagesimal(sexagesimal_str):
    sexagesimal_str = sexagesimal_str.strip()
    if ";" not in sexagesimal_str:
        raise ValueError("Invalid format! Ensure the number contains a ';' separator.")
    integer_part, fractional_part = sexagesimal_str.split(";")
    integer_part = int(integer_part)
    fractional_parts = list(map(int, fractional_part.split(","))) if fractional_part.strip() else []
    return [integer_part] + fractional_parts

def sexagesimal_to_decimal(sexagesimal):
    return sum(sexagesimal[i] / (60 ** i) for i in range(len(sexagesimal)))

def decimal_to_sexagesimal(decimal, precision):
    result = []
    for _ in range(precision):
        int_part = int(decimal)
        result.append(int_part)
        decimal = (decimal - int_part) * 60
    return result

def format_sexagesimal(sexagesimal):
    integer_part = sexagesimal[0]
    fractional_parts = ",".join(map(str, sexagesimal[1:])) if len(sexagesimal) > 1 else ""
    return f"{integer_part};{fractional_parts}" if fractional_parts else str(integer_part)

def perform_operation(num1, num2, operation):
    if isinstance(num1, list):
        num1 = sexagesimal_to_decimal(num1)
    if isinstance(num2, list):
        num2 = sexagesimal_to_decimal(num2)

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        result = num1 / num2
    else:
        raise ValueError("Invalid operation!")

    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        num1 = request.form["num1"]
        num2 = request.form["num2"]
        operation = request.form["operation"]
        format_choice = request.form["format"]
        precision = int(request.form["precision"])

        num1_parts = parse_sexagesimal(num1) if ";" in num1 else float(num1)
        num2_parts = parse_sexagesimal(num2) if ";" in num2 else float(num2)

        result_decimal = perform_operation(num1_parts, num2_parts, operation)

        if format_choice == "sexagesimal":
            result = format_sexagesimal(decimal_to_sexagesimal(result_decimal, precision))
        else:
            result = f"{result_decimal:.{precision}f}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
