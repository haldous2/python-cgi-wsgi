import re

def add(v1, v2):
    return v1 + v2

def subtract(v1, v2):
    return v1 - v2

def multiply(v1, v2):
    return v1 * v2

def divide(v1, v2):
    if (v2 >= v1):
        return v1 / v2
    else:
        raise ZeroDivisionError

def strnum(v):
    """
    convert string to number, either to integer or float depending on decimal
    note: the regex that captures v will only pass numbers and decimals, no need to check for invalid strings
    """
    if v:
        try:
            return int(v)
        except ValueError:
            return float(v)
    else:
        return 0

def application(environ, start_response):

    path = environ.get('PATH_INFO', '')

    ##
    # Note: only two tests numbers allowed in, only four operations supported
    # ex: localhost:8080/add/1/2
    # ex: localhost:8080/subtract/2/1
    ##
    matches = re.search("/(add|subtract|multiply|divide)/([0-9.]+)/([0-9.]+)", path)
    if matches:
        matched = matches.groups()
        oper = matched[0]
        var1 = strnum(matched[1])
        var2 = strnum(matched[2])
    else:
        matches = re.search("/(add|subtract|multiply|divide)/([0-9.]+)", path)
        if matches:
            matched = matches.groups()
            oper = matched[0]
            var1 = matched[1]
            var2 = None
        else:
            matches = re.search("/(add|subtract|multiply|divide)", path)
            if matches:
                matched = matches.groups()
                oper = matched[0]
                var1 = None
                var2 = None
            else:
                matched = None
                oper = None
                var1 = None
                var2 = None

    strOut = ["Returning NADA - oper:%s var1:%s var2:%s" % (oper, var1, var2)]
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    #start_response(status, headers)
    #return ["<h1>No Progress Yet</h1> path:%s parameters:%s match:%s" % (path, parameters, matched)]

    try:

        if oper and var1 >= 0 and var2 >= 0:

            if oper == "add":
                strAns = add(var1, var2)
                strOut = ["%s + %s = %s" % (var1, var2, strAns)]
            if oper == "subtract":
                strAns = subtract(var1, var2)
                strOut = ["%s - %s = %s" % (var1, var2, strAns)]
            if oper == "multiply":
                strAns = multiply(var1, var2)
                strOut = ["%s / %s = %s" % (var1, var2, strAns)]
            if oper == "divide":
                strAns = divide(var1, var2)
                strOut = ["%s * %s = %s" % (var1, var2, strAns)]

        else:

            if oper is None:
                strOut = ["missing operator - /add, /subract, /multiply or /divide."]
            if oper is not None and var1 is None and var2 is None:
                strOut = ["missing operands - e.g. /add/x/y where x & y are the numeric operands"]
            if oper is not None and var1 is not None and var2 is None:
                strOut = ["missing last operand - e.g. /add/x/y where y is the last numeric operand"]

    except ZeroDivisionError:
        status = "501 Not Implemented"
        strOut = ["<h1>Zero Division Error!</h1>"]
    except:
        status = "500 Internal Server Error"
        strOut = ["<h1>Internal Server Error!</h1> %s" % sys.exc_info()[0]]
    finally:
        start_response(status, headers)
        return strOut

if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

    ## Testing
    oper = "add"
    var1 = strnum("1")
    var2 = strnum("2.23")
    print "var1:%s var2:%s" % (var1, var2)
    print add(var1, var2)
    ## Testing
