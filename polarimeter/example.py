import acquire_data
import analyse_data

t, obj, ref = acquire_data.main(6144,1000)
print 'Delta Phi = %.3f rad' % (analyse_data.calc_delta_phi(t, obj, ref))