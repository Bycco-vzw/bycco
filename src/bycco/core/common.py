import yaml
from reddevil.filestore.filestore import get_file


async def load_common():
    _icd = getattr(load_common, "common", None)
    if not _icd:
        icdr = await get_file("data", "common.yml")
        _icd = yaml.load(icdr.body, Loader=yaml.SafeLoader)
        setattr(load_common, "common", _icd)
    return _icd
