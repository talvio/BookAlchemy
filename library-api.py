"""" This file ended up being unnecessary for the project. At least so far. """

import requests

API_URL_AUTHORS = "https://openlibrary.org/search/authors.json"
API_URL_SEARCH = "https://openlibrary.org/search.json"
CONNECTION_TIMEOUT = 3
READ_TIMOUT = 10

"""
https://openlibrary.org/dev/docs/api/search 

Author: https://openlibrary.org/authors/OL23919A.json
Works: https://openlibrary.org/authors/OL23919A/works.json
You can append ?limit=1000 to return the first 1000 works by an author like so:
https://openlibrary.org/authors/OL1394244A/works.json?limit=100

If you want to paginate, you can set offset like so:
https://openlibrary.org/authors/OL1394244A/works.json?offset=50

Gotchas

Note that by default, navigating to https://openlibrary.org/authors/OL23919A will 
redirect to https://openlibrary.org/authors/OL23919A/J._K._Rowling (appending the human 
readable slug "J._K._Rowling"). Adding .json to the end of the slug 
(e.g. https://openlibrary.org/authors/OL23919A/J._K._Rowling.json) will not work. 
You must first remove the human readable slug and append .json directly to the end 
of the author's key, e.g. https://openlibrary.org/authors/OL23919A.json.

https://openlibrary.org/search.json?q=the+lord+of+the+rings
https://openlibrary.org/search.json?title=the+lord+of+the+rings
https://openlibrary.org/search.json?author=tolkien&sort=new
https://openlibrary.org/search.json?q=the+lord+of+the+rings&page=2
https://openlibrary.org/search/authors.json?q=twain

You can use the olid (Open Library ID) for authors and books to fetch covers by olid, e.g.:
https://covers.openlibrary.org/a/olid/OL23919A-M.jpg

offset / limit	Use for pagination.
page / limit	Use for pagination, with limit corresponding to the page size. Note page starts at 1.
{
    "start": 0,
    "num_found": 629,
    "docs": [
        {...},
        {...},
        ...
        {...}]
}
{
    "cover_i": 258027,
    "has_fulltext": true,
    "edition_count": 120,
    "title": "The Lord of the Rings",
    "author_name": [
        "J. R. R. Tolkien"
    ],
    "first_publish_year": 1954,
    "key": "OL27448W",
    "ia": [
        "returnofking00tolk_1",
        "lordofrings00tolk_1",
        "lordofrings00tolk_0",
    ],
    "author_key": [
        "OL26320A"
    ],
    "public_scan_b": true
}
The fields in the doc are described by Solr schema which can be found here:
https://github.com/internetarchive/openlibrary/blob/b4afa14b0981ae1785c26c71908af99b879fa975/openlibrary/plugins/worksearch/schemes/works.py#L38-L91

EDITIONS
https://openlibrary.org/search.json?q=crime+and+punishment&fields=key,title,author_name,editions
"""

def access_open_library_api(params, api):
    """
    A fault tolerant way to access the Wikipedia API.
    :param params:
    :return: Tuple where the first value is True if the call was successful, False is not.
             The second is the result of the API call.
    """
    try:
        data = requests.get(api, params=params, timeout=(CONNECTION_TIMEOUT, READ_TIMOUT)).json()
    except requests.exceptions.Timeout:
        return False, "(No description available. Access to API timed out.)"
    except requests.exceptions.ConnectionError:
        return False, "(No description available. Access to API failed.)"
    except requests.exceptions.HTTPError as err:
        return False, f"(No description available. Access to API failed: {err}.)"
    except requests.exceptions.RequestException as err:
        return False, f"(No description available. Access to API failed: {err}.)"
    return True, data

if __name__ == '__main__':
    #params = {
    #    'q': 'Stephen King'
    #}
    #params = {
    #        'title': "Cat's cradle"
    # }
    params = {
            'isbn': "9780394758282"
    }
    is_success, data = access_open_library_api(params, API_URL_SEARCH)

    print(data)
