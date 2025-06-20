from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory
from multisim_matrix.simservice.VertexPlanarSheet import VertexPlanarSheet

SERVICE_NAME = 'VertexPlanarSheet'


class VertexPlanarSheetServiceWrap(TypeProcessWrap):
    _process_cls = VertexPlanarSheet


ServiceManagerLocal.register_service(SERVICE_NAME, VertexPlanarSheetServiceWrap)


def vertex_planar_sheet_simservice(*args, **kwargs):
    return process_factory(SERVICE_NAME, *args, **kwargs)
