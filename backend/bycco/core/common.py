import logging
from yaml import load, SafeLoader


logger = logging.getLogger(__name__)

def _read_common():
    with open ('./common.yaml') as f:
        try:
            data =  load(f, SafeLoader)
        except Exception as e:
            logger.error('Failed to load common.yaml')
            data = None
        return data


def get_common():
    """
    singleton
    """
    if not hasattr(get_common, "common"):
        setattr(get_common, "common", _read_common())
    return getattr(get_common, "common")