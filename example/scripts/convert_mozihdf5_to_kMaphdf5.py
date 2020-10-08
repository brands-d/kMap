# Third Party Imports
import h5py
import numpy as np

# this script demonstrates how the hdf5-files created by Mozi can be converted to 
# the format used in kMap.py 

def mozi_to_kmap(mozi_h5_file,kmap_h5_file,
                 alias=None,          # A short alternative to 'name'. Can not be an empty string.
                 axis1type='+BE'):    # choose between '+BE' or '-BE' (binding energy) or 'E_kin' (kinetic energy)

    old     = h5py.File(mozi_h5_file,'r')  # open old hdf5 file
    new     = h5py.File(kmap_h5_file,'w')  # create new file

    # extract information from old hdf5
    oldkeys = ['filenumber','fermiLevel','kStepSize','list_index','list_kAxis','list_BE_real','list_BE',
                'arcwidth','polarshift','rotation','negPolar_avgs','sym_anglemin','sym_anglemax','symmode']
    filenumber   = old['filenumber'][()]
    fermiLevel   = old['fermiLevel'][()]
    list_kAxis   = old['list_kAxis'][()]
    list_BE_real = old['list_BE_real'][()]
    list_BE      = old['list_BE'][()]

    if   axis1type == '+BE':   # binding energy with positive sign convention
        axis_1_range = [ list_BE_real[-1], list_BE_real[0]]      
    
    elif axis1type == '-BE':   # binding energy with negative sign convention  
        axis_1_range = [-list_BE_real[0], -list_BE_real[-1]] 

    elif axis1type == 'E_kin':   # kinetic energy 
        axis_1_range = [fermiLevel-list_BE_real[0], fermiLevel-list_BE_real[-1]] 

    meta_data = {'filenumber'    : old['filenumber'][()],
                 'fermiLevel'    : old['fermiLevel'][()],
                 'kStepSize'     : old['kStepSize'][()],
                 'arcwidth'      : old['arcwidth'][()],
                 'polarshift'    : old['polarshift'][()],
                 'rotation'      : old['rotation'][()],
                 'negPolar_avgs' : old['negPolar_avgs'][()],
                 'sym_anglemin'  : old['sym_anglemin'][()],
                 'sym_anglemax'  : old['sym_anglemax'][()],
                 'symmode'       : old['symmode'][()]}
           
    # write header info in new hdf5
    new.create_dataset('name',        data=filenumber)
    if alias != None: new.create_dataset('alias',data=alias)
    new.create_dataset('axis_1_label',data=axis1type)
    new.create_dataset('axis_2_label',data='kx')
    new.create_dataset('axis_3_label',data='ky')
    new.create_dataset('axis_1_units',data='eV')
    new.create_dataset('axis_2_units',data='1/Å')
    new.create_dataset('axis_3_units',data='1/Å')
    new.create_dataset('axis_1_range',data=axis_1_range)
    new.create_dataset('axis_2_range',data=[list_kAxis[0,0],list_kAxis[0,-1]])
    new.create_dataset('axis_3_range',data=[list_kAxis[0,0],list_kAxis[0,-1]])
    for key in meta_data:
        new.create_dataset(key,data=meta_data[key])

    # extract data from old hdf5 and write 3D-array to new hdf5
    nx    = len(list_BE)
    ny    = list_kAxis.shape[1]
    nz    = ny
    data  = np.zeros((nx,ny,nz))
   
    for count, BE in enumerate(old['data_kmaps']):
        if axis1type == '+BE':
            i = count
        else:
            i = nx - count - 1

        data[i,:,:] = old['data_kmaps'][BE][()]

    new.create_dataset('data',data=data,
                        dtype='f8',compression='gzip', compression_opts=9)

    old.close()
    new.close()
    return



mozi_to_kmap('kmaps_3271_BEstep0.1.hdf5','example4_3271.hdf5',
             axis1type='E_kin',
             alias='multilayer 5A HOMO')



