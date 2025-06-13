from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory
from multisim_matrix.simservice.CenterPlanarSheet import CenterPlanarSheet

SERVICE_NAME = 'CenterPlanarSheet'


class CenterPlanarSheetServiceWrap(TypeProcessWrap):
    _process_cls = CenterPlanarSheet


ServiceManagerLocal.register_service(SERVICE_NAME, CenterPlanarSheetServiceWrap)


def center_planar_sheet_simservice(*args, **kwargs):
    return process_factory(SERVICE_NAME, *args, **kwargs)
