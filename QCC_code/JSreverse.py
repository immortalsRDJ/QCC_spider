import execjs
import furl

def get_header(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    with open('qichacha.js', 'r') as js_file:
        js = execjs.compile(js_file.read())
        url_info = furl.furl(url)
        get_headers = js.call('main', str(url_info.path))

        headers[get_headers['key']] = get_headers['value']

        return headers

