from pkg_resources import get_distribution, DistributionNotFound

from dream.dream import run 

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
