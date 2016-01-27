#!/usr/bin/env python3
def add (x, y):
    return x + y
def subtract (x, y):
    return x - y
def multiply (x, y):
    return x * y
def divide (x, y):
    return x / y

def page():
    front_page = """<html>
    <head>
    <title>Simple Calculator</title>
    </head>

    <body>
    <p>This simple calculator can perform the following math related operations:</p>
    <p>Addition</p>
    <p>ex: http://localhost:8080/add/5/3</p>
    <p>Subtraction</p>
    <p>ex: http://localhost:8080/subtract/5/3</p>
    <p>Multiplication</p>
    <p>ex: http://localhost:8080/multiply/5/3</p>
    <p>Division</p>
    <p>ex: http://localhost:8080/divide/5/3</p>
    </body>
    </html>"""
    return front_page

def calculate (operator, operands):
    answer_page = """<html>
    <head>
    <title>Simple Calculator</title>
    </head>
    <body>
    Answer: {}
    </body>
    </html>"""
    if operator == 'add':
        answer = add(*operands)
    elif operator == 'subtract':
        answer = subtract (*operands)
    elif operator == 'multiply':
        answer = multiply(*operands)
    elif operator == 'divide':
        answer = divide(*operands)
    else:
        raise ValueError
    return answer_page.format(answer)

def resolve_path(path):
    parts = path.strip('/').split('/')[-3:]
    operator = parts[0]
    operands = map(int, parts[-2:])
    return operator, operands

def application(environ, start_response):
    #import pdb; pdb.set_trace()
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        operator, operands = resolve_path(path)
        #import pdb; pdb.set_trace()
        if operator:
            body = calculate(operator, operands)
            status = "200 OK"
        else:
            body = page()
            status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except ZeroDivisionError:
        status = "500 Division by Zero"
        body = "<h1>Division by Zero Error</h1>"
    except Exception as e:
        status = "500 Internal Server Error"
        body = "<h1>The error is: {}</h1>".format(e)
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()