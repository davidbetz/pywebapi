from .general import debug

from .sample_processor import Processor

from .repo.item_repo import ItemRepo
from .repo.azure_repo import AzureItemRepo
from .repo.image_repo import PictureRepo

from .json_formatter import JsonFormatter
from .binary_formatter import BinaryFormatter
#from xml_formatter import XmlFormatter

from .aws.calc_skill import CalcSkill

aws_skills = [
    (r'aws/calc$', CalcSkill),
]

resources = [
    (r'item/?(?P<id>\d+)?$', ItemRepo),
    (r'image/?(?P<id>[\w]+)?$', PictureRepo),
    (r'config/?(?P<id>[!\w]+)?$', AzureItemRepo)
]

processor = Processor()
processors = [
    (r'contact$', { 'get': processor.contact, 'post': processor.contact_post }),
    (r'$', processor.home),
]

formatters = [
    JsonFormatter(),
    BinaryFormatter(),
    #XmlFormatter()
]
