import urllib
try: import simplejson as json
except ImportError: import json
import decimal

class Junar:
    """ Base class, contains the configuration"""
    def __init__(self, auth_key, base_uri = 'http://apisandbox.junar.com'):
        self.auth_key = auth_key
        self.base_uri = base_uri

    def datastream(self, guid):
        """ Creates a datastream object.

        Keyword arguments:
        guid -- the guid of the datastream"""
        return DataStream(guid, self.auth_key, self.base_uri)

    def publish(self, dictionary):
        '''
        Encodes the dictionary into url form and then it publishes it to the junar API
        to retrieve the the information about this new datastream it retuns a datastream
        refering to this new ds in junar
        '''
        #TODO: Error handling
        publisher = Publisher(dictionary, self.auth_key, self.base_uri)
        guid = publisher.publish()
        if guid is not None:
            return DataStream(guid, self.auth_key, self.base_uri)

        return None

class Publisher:

    def __init__(self, dictionary, auth_key, base_uri):
        import urllib
        from urlparse import urlparse
        self.params = urllib.urlencode(dictionary)
        self.auth_key = auth_key
        self.base_uri = urlparse(base_uri)
        self.headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

    def publish(self):
        from httplib import HTTPConnection
        conn = HTTPConnection(self.base_uri.netloc)
        conn.request("POST", "/datastreams/publish", self.params, self.headers)
        response = conn.getresponse()
        return self.analyze(response)

    def analyze(self, response):
        print response.status
        if response.status == 200:
            import json
            data_from_junar = json.loads(response.read())
            return data_from_junar['id']
        return None





class DataStream:

    def __init__(self, guid, auth_key, base_uri):
        """ It can be used to invoke a datastream (that means, to get its data), and to get metada about it

        Keyword arguments:
        guid -- the guid of the datastream
        auth_key -- your auth_key to access the API
        base_uri -- the base uri of the API
        """
        self.auth_key = auth_key
        self.base_uri = base_uri
        self.guid = guid
        self.response = None
        self.output = '';

    def invoke(self, params = [], output = '', page = None, limit = None):
        """
        Gets the datastream's data.

        Keyword arguments:
        params -- a list of the parameters, (parameters are positional)
        output -- the format in which the document will be returned
                  for default junar json leave output blank, its structure is explained
                  here http://wiki.junar.com/index.php/API#JSON_Structure

        other options are:
        - prettyjson use this, with the collect tool at www.junar.com,
                     by enabling the advanced mode, and select "Add aliases", then follow the instructions
        - json_array, basic javascript array of arrays, in python a list of lists
        - csv
        - tsv
        - excel
        - xml, prettyjson sister, configuration here is not mandatory
        page -- a page number, starting by 1, to paginate the results
        limit -- a limit of rows to be retrieved
        """

        if not self.auth_key:
            raise Exception('Please configure your auth_key, get one at http://www.junar.com/developers/')

        # create the URL
        query = {'auth_key': self.auth_key}

        if isinstance(page, int) and isinstance(limit, int):
            query['page'] = page
            query['limit'] = limit

        i = 0
        for param in params:
            query['pArgument%d' % i] = param;
            i = i + 1

        if output:
            self.output = output
            query['output'] = output

        url = '/datastreams/invoke/%s?%s' % (self.guid, urllib.urlencode(query))
        return self._call_uri(url);

    def info(self):
        """ Gets the datastream's metadata. """
        # create the URL
        query = {'auth_key': self.auth_key}
        url = '/datastreams/invoke/%s?%s' % (self.guid, urllib.urlencode(query))
        return self._call_uri(url);

    def _call_uri(self, url):

        network_object = urllib.urlopen(self.base_uri + url)
        response       = network_object.read()

        if network_object.getcode() != 200:
            json_response = json.loads(response)
            raise Exception('Error: HTTP %s, %s' % (json_response['error'], json_response['message']))

        # parsing the content
        if self.output in ['', 'prettyjson', 'json_array']:
            self.response = json.loads(response, parse_float=decimal.Decimal)
        else:
            self.response = response

        return self.response
