# Need PYTHONPATH to contain wrapper directory
# Also need LD_LIBRARY_PATH to include it for libwannier_serial.so
import wan90

ftn_output = wan90.w90_helper_types.get_fortran_stdout()

data = wan90.w90_helper_types.lib_global_type()
w90data = wan90.w90_helper_types.lib_w90_type()
comm = wan90.w90_comms.w90comm_type()
wan90.w90_helper_types.input_reader(data, w90data, "diamond", ftn_output, status, comm)

if not data.kmesh_info.explicit_nnkpts :
    wan90.w90_helper_types.create_kmesh(data, ftn_output, status, comm)

import numpy

m_matrix = numpy.zeros((data.num_wann, data.num_wann, data.kmesh_info.nntot, data.num_kpts), dtype=numpy.cdouble, order='F')
u_matrix = numpy.zeros((data.num_wann, data.num_wann, data.num_kpts), dtype=numpy.cdouble, order='F')
a_matrix = numpy.zeros((data.num_bands, data.num_wann, data.num_kpts), dtype=numpy.cdouble, order='F')
wan90.w90_helper_types.set_m_matrix(w90data, m_matrix)
wan90.w90_helper_types.set_u_matrix(data, u_matrix)
wan90.w90_helper_types.set_a_matrix(w90data, a_matrix)

#m_matrix.flags.f_contiguous should be true

if data.num_wann == data.num_bands:
    m_orig = numpy.zeros((1, 1, 1, 1), dtype=numpy.cdouble, order='F')
    wan90.w90_helper_types.set_m_orig(w90data, m_orig)
    u_opt = numpy.zeros((1, 1, 1), dtype=numpy.cdouble, order='F')
    wan90.w90_helper_types.set_u_opt(data, u_opt)
    wan90.w90_helper_types.overlaps(data, ftn_output, status, comm)
else:
    u_opt = numpy.zeros((data.num_bands, data.num_wann, data.num_kpts), dtype=numpy.cdouble, order='F')
    wan90.w90_helper_types.set_u_opt(data, u_opt)
    m_orig = numpy.zeros((data.num_bands, data.num_bands, data.kmesh_info.nntot, data.num_kpts), dtype=numpy.cdouble, order='F')
    wan90.w90_helper_types.set_m_orig(w90data, m_orig)
    wan90.w90_helper_types.overlaps(data, w90data, ftn_output, status, comm)
    wan90.w90_helper_types.disentangle(data, w90data, ftn_output, status, comm)
    
wan90.w90_helper_types.wannierise(data, w90data, ftn_output, status, comm)


#wan90.w90_helper_types.checkpoint(data, w90data, "postwann", ftn_output, comm)

wan90.w90_helper_types.plot_files(data, w90data, ftn_output, status, comm)

#wan90.w90_helper_types.transport(data, w90data, ftn_output, status, comm)

wan90.w90_helper_types.print_times(data, ftn_output)
