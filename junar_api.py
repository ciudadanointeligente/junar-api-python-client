import urllib
import json
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

    def invoke(self, params = [], output = ''):
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
        """

        if not self.auth_key:
            raise Exception('Please configure your auth_key, get one at http://www.junar.com/developers/')

        # create the URL
        query = {'auth_key': self.auth_key}

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
            raise Exception('Error HTTP status code = %s' % network_object.getcode())

        # parsing the content
        if self.output in ['', 'prettyjson', 'json_array']:
            self.response = json.loads(response, parse_float=decimal.Decimal)
        else:
            self.response = response

        return self.response
