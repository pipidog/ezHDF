import sys; sys.path.insert(0,'/Users/shutingpi/Dropbox/ezHDF')
from ezHDF.ezHDF import hdf_store
import pandas as pd
import os

# parameter ==============
wkdir = os.path.dirname(os.path.realpath(__file__))
col_name1 = ['str0','int1','float2','float3','str4','str5','str6']
dtype1 = ['s','i','f','f','s','s','s']
col_name2 = ['str0','int1','str2','str3','float4','float5','str6']
dtype2 = ['s','i','s','s','f','f','s']

# main ===================
# read data from csv, set a chunksize = 100, useful when reading huge file
reader1 = pd.read_csv(wkdir+'/data1.csv', sep = ',', engine = 'c', 
                    error_bad_lines=False, warn_bad_lines=False, index_col = False,
                    chunksize= 100)

reader2 = pd.read_csv(wkdir+'/data2.csv', sep = ',', engine = 'c', 
                    error_bad_lines=False, warn_bad_lines=False, index_col = False,
                    chunksize= 100)

# create a hdf_store onject, use mode ='w' to create a new hdf file
store = hdf_store(wkdir = wkdir, hdf_name = 'my_hdf.h5', mode = 'w')

# let's create two new datasets to store our data
store.new_dataset(ds_name = 'data1', container_size = 12000, column_names = col_name1, column_dtype = dtype1)
store.new_dataset(ds_name = 'data2', container_size = 22000, column_names = col_name2, column_dtype = dtype2)

# check info 
store.info()

# resize container size
store.resize('data1', 15000)
stire.resize('data2', 25000)
store.info()

# put data1 into dataset data1
for chunk in reader1:
    chunk = chunk.drop(chunk.columns[0], axis = 1)
    store.append_to_dataset(ds_name = 'data1', chunk = chunk)

# put data2 into dataset data2
for chunk in reader2:
    chunk = chunk.drop(chunk.columns[0], axis = 1)
    store.append_to_dataset(ds_name = 'data2', chunk = chunk)

# check information of the HD file again, n_container > n_rows
store.info()

# let resize n_container = n_rows, to save storage size
store.auto_match_size(ds_name = 'data1')
store.auto_match_size(ds_name = 'data2')

# check info again
store.info()

#store.auto_match_size('raw_data')
store.close()

