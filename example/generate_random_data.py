'''
This code help you generate random compound structure data. 
The generated data can be used to test ezHDF
'''
import numpy as np 
import pandas as pd
import string
from random import *

# parameter ======
nrows = 20000
data_type = ['s','i','s','s','f','f','s']
fname = 'data2.csv'
# main ===========
def random_str(min_char=5, max_char=20, nrows = 10000):
    pwd = []
    for n in range(nrows):
        allchar = string.ascii_letters #+ string.punctuation + string.digits
        password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        pwd.append(password)
    return np.array(pwd)

def random_float(nrows = 10000):
    return np.random.rand(nrows)

def random_int(nrows):
    return np.random.randint(0,1000,nrows)

for n, typ in enumerate(data_type):
    if typ == 's':
        df_tmp = pd.DataFrame(random_str(nrows= nrows),columns = ['str'+str(n)])
    elif typ == 'i':
        df_tmp = pd.DataFrame(random_int(nrows= nrows),columns = ['int'+str(n)])
    elif typ == 'f':
        df_tmp = pd.DataFrame(random_float(nrows= nrows),columns = ['float'+str(n)])
    if n == 0:
        df = df_tmp
    else:
        df = pd.concat([df, df_tmp], axis = 1)
df.to_csv(fname, sep = ',', mode = 'w')