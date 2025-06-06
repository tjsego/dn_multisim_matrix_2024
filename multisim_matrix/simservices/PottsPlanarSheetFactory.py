from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory
from .PottsPlanarSheet import PottsPlanarSheet

SERVICE_NAME = 'PottsPlanarSheet'


class PottsPlanarSheetServiceWrap(TypeProcessWrap):
    _process_cls = PottsPlanarSheet


ServiceManagerLocal.register_service(SERVICE_NAME, PottsPlanarSheetServiceWrap)


def potts_planar_sheet_simservice(*args, **kwargs):
    return process_factory(SERVICE_NAME, *args, **kwargs)
