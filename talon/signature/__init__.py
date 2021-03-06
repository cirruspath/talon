"""The package exploits machine learning for parsing message signatures.

The public interface consists of only one `extract` function:

>>> (body, signature) = extract(body, sender)

Where body is the original message `body` and `sender` corresponds to a person
who sent the message.

When importing the package classifiers instances are loaded.
So each process will have it's classifiers in memory.

The import of the package and the call to the `extract` function are better be
enclosed in a try-catch block in case they fail.

.. warning:: When making changes to features or emails the classifier is
trained against, don't forget to regenerate:

* signature/data/train.data and
* signature/data/classifier
"""

import os
import sys
from cStringIO import StringIO

from . import extraction
from . extraction import extract
from . learning import classifier

if 'TALON_DATA_DIR' in os.environ:
    DATA_DIR = os.environ['TALON_DATA_DIR']
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

EXTRACTOR_FILENAME = os.path.join(DATA_DIR, 'classifier')
EXTRACTOR_DATA = os.path.join(DATA_DIR, 'train.data')


def initialize():
    try:
        # redirect output
        so, sys.stdout = sys.stdout, StringIO()

        extraction.EXTRACTOR = classifier.load(EXTRACTOR_FILENAME,
                                               EXTRACTOR_DATA)
        sys.stdout = so
    except Exception, e:
        raise Exception(
            "Failed initializing signature parsing with classifiers", e)
