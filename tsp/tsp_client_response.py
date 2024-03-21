# The MIT License (MIT)
#
# Copyright (C) 2020 - Ericsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""TspClientResponse class file."""

import json
from tsp.response import GenericResponse, GenericResponseEncoder
from tsp.output_descriptor_set import OutputDescriptorSet
from tsp.output_descriptor import OutputDescriptorEncoder

MODEL_KEY = "model"
OUTPUT_DESCRIPTOR_KEY = "output"
RESPONSE_STATUS_KEY = "status"
STATUS_MESSAGE_KEY = "statusMessage"


# pylint: disable=too-few-public-methods
class TspClientResponse:
    '''
    Class that for providing the tsp
    '''

    def __init__(self, model, status, status_message, size=None):
        '''
        Constructor
        '''

        # The model of TSP call or None
        self.model = model

        # The HTTP status code
        self.status = status

        # The status message
        self.status_message = status_message

        self.size = size
    
    def is_ok(self):
        return self.status >= 200 and self.status < 400
    
    def __repr__(self):
        return 'TspClientResponse ({}, {}, {})'.format(self.status, self.status_message, self.model)

class TspClientResponseEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, TspClientResponse):
            # Convert TspClientResponse to a dictionary
            if isinstance(obj.model, GenericResponse):
                return {
                    'model': GenericResponseEncoder().default(obj.model),
                    RESPONSE_STATUS_KEY : obj.status,
                    STATUS_MESSAGE_KEY: obj.status_message
                }
            elif isinstance(obj.model, OutputDescriptorSet):
                return {
                    'model': [OutputDescriptorEncoder().default(output_descriptor) for output_descriptor in obj.model.descriptors],
                    RESPONSE_STATUS_KEY: obj.status,
                    STATUS_MESSAGE_KEY: obj.status_message
                }
            else:
                return {
                    'model': obj.model,
                    RESPONSE_STATUS_KEY: obj.status,
                    STATUS_MESSAGE_KEY: obj.status_message
                }
        return super().default(obj)
