import h5py
import numpy as np 
import pandas as pd

class dataset_explorer:
    def __init__(self, dataset):
        if 'ezHDF' not in dataset.attrs.keys():
            raise TypeError('not an ezHDF dataset !')
        self.dataset = dataset
        attrs = self.dataset.attrs
        self.column_names = [name.decode('utf-8') for name in dataset.attrs['column_names']] 
        self.column_dtype = attrs['column_dtype'].split(',')
        self.n_rows = attrs['n_rows']
        self.container_size = attrs['container_size']

    def __str__(self):
        attrs = self.dataset.attrs
        output = 'ezHDF hanlder object:\n'+\
                 '  dataset name: %s\n' % attrs['name']+\
                 '  column names: \n'+\
                 '  ['+' , '.join(self.column_names)+']\n'+\
                 '  column dtype:\n'+\
                 '  ['+' , '.join(self.column_dtype)+']\n'+\
                 '  size of data: %d\n' % self.n_rows+\
                 '  size of container %d' % self.container_size
        return output

    def __getitem__(self, item):
        item1, item2 = item

        # convert item2 to a list of column names
        if type(item2) != type([0]):
            item2 = [item2]
        if type(item2[0]) == type(0):
            item2 = [self.column_names[idx] for idx in item2]
            
        for n, col in enumerate(item2):
            df_tmp = pd.DataFrame(self.dataset[col][item1], columns = [col])
            if n == 0:
                df = df_tmp
            else:
                df = pd.concat([df,df_tmp], axis = 1)
                
        return df

class hdf_store:
    def __init__(self, wkdir = './', hdf_name = 'data.h5', mode ='a'):
        if wkdir[-1]!='/' and wkdir[-1]!='\\':
            wkdir +='/' 
        self.wkdir = wkdir     
        self.h5f = h5py.File(self.wkdir+hdf_name, mode)
        
    def new_dataset(self, ds_name, container_size, column_names, column_dtype):
        ds = self.h5f.create_group(ds_name) 
        ds.attrs['name'] = ds_name 
        ds.attrs['ezHDF'] = 0  
        ds.attrs['n_rows'] = 0
        ds.attrs['container_size'] = container_size
        ds.attrs['column_names'] = np.string_(column_names)  #column_names
        for n, col in enumerate(column_names):
            if column_dtype[n] == 's':
                typ = h5py.special_dtype(vlen=str)
            else:
                typ = column_dtype[n]
            ds.create_dataset(col, (container_size,), maxshape =(None,), dtype = typ) 
        ds.attrs['column_dtype'] = ' , '.join(column_dtype)

    def info(self):
        print('\n--- ezHDF hdf_store info ---\n')
        for ds_name in self.h5f.keys():
            ds = self.h5f[ds_name]
            print('dataset name: %s' % ds_name)
            print('column names:')
            print('  ',[ name.decode('utf-8') for name in ds.attrs['column_names']])
            print('column dtype:[ %s ]' % ds.attrs['column_dtype'])
            print('n_rows: %d' % ds.attrs['n_rows'])
            print('n_container: %d\n' % ds.attrs['container_size'])

    def resize(self, ds_name, new_n_rows):
        ds = self.h5f[ds_name]
        for col in ds.attrs['column_names']:
            ds[col.decode('utf-8')].resize((new_n_rows,))
        ds.attrs['container_size'] = new_n_rows        
        print('dataset (%s) now resized to (%d) rows' % (ds_name, new_n_rows))

    def append(self, ds_name, data):
        ds = self.h5f[ds_name]
        if type(data) != type(pd.DataFrame([])):
            raise TypeError('You can only append a pandas DataFrame. Found:', type(data))
        if data.shape[1] != len(ds.attrs['column_names']):
            raise ValueError('found chunk with %d columns but dataset has only %d.' 
                            % ( data.shape[1], len(ds.attrs['column_names'])),  
                            'check if row index is included. If so, use ' 
                            'chunk.drop(chunk.columns[0], axis = 1) to drop it before ' 
                            'using hdf_store.append.' 
                            )

        # check if resize dataset
        n_rows = ds.attrs['n_rows']
        container_size = ds.attrs['container_size']
        if n_rows+len(data) > container_size: 
            print(' auto resizing dataset to: %d' % ( n_rows + len(data)))

        for n, name in enumerate(ds.attrs['column_names']):
            name = name.decode('utf-8')
            if n_rows+len(data) > container_size: 
                ds.resize((n_rows+len(data),))
            ds[name][n_rows:n_rows+len(data)] = data.iloc[:,n]

        ds.attrs['n_rows'] += len(data)
    
    def auto_resize(self, ds_name):
        ds = self.h5f[ds_name]
        n_rows = ds.attrs['n_rows']
        if n_rows < ds.attrs['container_size']:
            self.resize(ds_name, n_rows)
        else:
            print(' size is consistent, no adjustment needed.')

    def explorer(self, ds_name):

        return dataset_explorer(self.h5f[ds_name])
    
    def close(self):
        self.h5f.close()