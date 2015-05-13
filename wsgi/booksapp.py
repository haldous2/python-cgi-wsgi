import re

from bookdb import BookDB
from cgi import parse_qs

DB = BookDB()

def book(book_id):
    #return "<h1>a book with id %s</h1>" % book_id
    page = """
    <h1>{title}</h1>
    <table>
        <tr><th>Author</th><td>{author}</td></tr>
        <tr><th>Publisher</th><td>{publisher}</td></tr>
        <tr><th>ISBN</th><td>{isbn}</td></tr>
    </table>
    <a href="/">Back to the list</a>
    """
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    return page.format(**book)

def books():
    #return "<h1>a list of books</h1>"
    all_books = DB.titles()
    body = ['<h1>My Bookshelf</h1>', '<ul>']
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append('</ul>')
    return '\n'.join(body)

def application(environ, start_response):

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    #path = environ.get('PATH_INFO', '').lstrip('/') # This removes the leading slash.. not sure what that is good for (yet)
    path = environ.get('PATH_INFO', '')

    # Only need to see what is right after book/(-->here<--)
    matches = re.search("/book/(id[0-9]+)", path)
    if matches:
        matched = matches.groups()
    else:
        matched = None

    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    #start_response(status, headers)
    #return ["<h1>No Progress Yet</h1> path:%s parameters:%s match:%s" % (path, parameters, matched)]

    try:

        if matched is None:
            strOut = books()
        else:
            strOut = book(matched[0])

    except NameError:
        status = "404 Page Not Found"
        strOut = ["<h1>Page Not Found!</h1>"]
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
