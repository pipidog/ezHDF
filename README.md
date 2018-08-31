# Welcome to ezHDF
## What is ezHDF5
ezHDF is a simple tool you help you use HDF5 in combination with pandas to store and read hugh amount of data.

HDF5 is a novel data storage format. It can read, store and query huge amount of data without any difficult. It can also help you handle large data even in your light-weighted laptop thank to its memory-map based mechnism (i.e. move data to RAM only when you slice it). So you can slice into multi-terabyte datasets stored on disk, as if they were real NumPy arrays. For an quick introduction, see the official website of [hyp5](http://docs.h5py.org/en/stable/). 

## Why do we need ezHDF?
There are many options to use HDF5 in python, e.g. [hyp5](http://docs.h5py.org/en/stable/) and [PyTables](https://www.pytables.org/). [Pandas](https://pandas.pydata.org/pandas-docs/stable/io.html#hdf5-pytables) also has provides an user interface to PyTables. Alghouth they are all very powerful tools, they are all hard to use (at least, for me) because there are many "mysterious" tricks to use them properly. For example, if you want append new string data to a dataset in Pandas / PyTables, [you may get error message if the length of strings of newly appended data are different](https://stackoverflow.com/questions/22710738/pandas-pytable-how-to-specify-min-itemsize-of-the-elements-of-a-multiindex). Also, appending new data will become [extremely slow when the dataset become larger and larger and eventually crashes.](https://stackoverflow.com/questions/22934996/pandas-pytables-append-performance-and-increase-in-file-size) 

h5py also has it own disadvantages. hyp5 is highly compatible to numpy but it does not offer any user interface to pandas. In addition, hyp5 also requires [special tricks when storing compound data types.](https://github.com/h5py/h5py/issues/735) If you want to use h5py to store pandas data frame, you may want to use "dataset.attrs" to store some information of the dafa frame. However, it also requires [additional cautions when using strings](http://docs.h5py.org/en/latest/strings.html). 

In short, neither h5py nor PyTables are very user friendly tools for new users (again, for me at least) who just want to store and explore large data. That's why I develop ezHDF. 

ezHDF provides a simple and convenient interfaces to bridge h5py and pandas. Users can quickly and painlessly store large amounts of data and restore a pandas data frame by just a few commands. 

## How does ezHDF work?
ezHDF is essentially an API to h5py. HDF5 is a hierarchical data format which means you can have two data level: "group" and "dataset". Based on my experience (so, maybe not universally correct), if a dataset has the same data type, it can be much faster than compound data type. Besides, using only one type in a data set can also avoid possible issues due to compound data type. 

Therefore, in ezHDF, I split each column in a pandas data frame as a single "dataset" in HDF5 and combined all dataset (i.e. all columns) as a group. It makes HDF5 runs very fast and avoid all the issues due the compound data in a single dataset. 

Despite the above idea is useful for data storage, it makes the data slicing tedious. Therefore, I redefined a new data structure, "ezHDF dataset", to help users conveniently fetch data from a HDF file. Users can eaily fetch data using a pandas-like format and automatically returns a pandas data frame. 

## Benchmark
To have a benchmark test, I used a csv file that contains 30M rows (8 Gb on hard disk). Each row has 7 columns, 4 of them are variable length strings and the other three are integers, float and float respectively. Then I use pandas to read the file with 100K rows per chunk and pass to ezHDF for storing. The output h5 files has 16G. It takes only 4 mins to finish the job on my laotop (i7-4750HQ). That means dealing with **25G (8G in + 16G out) throughput less than 300 seconds in an old laptop !**. 

very fast ! isn't it? 

## Installation

**pip install ezHDF**

## Usage
Note that, the term "dataset" in ezHDF is different from the term "dataset" in h5py. Since ezHDF use a group in h5py to store all columns in Pandas, there is no "group" in ezHDF. 

There are two Jupyter files in the examples folder:  
* ex_store_data.ipynb: this file shows how to store huge amout of data using ezHDF

* ex_explore_data.ipynb: this file shows how to explore a ezHDF file using it built API. 

If you want to generate your own test dataset, you can use the file **generate_random_data.py** to generate your own test dataset. 

You should be able to fully understand how to use it within a few minutes by reading the above files carefully. 

## Quick Guide:
I strongly recommend you read the examples files, so you will have a comprehensive understanding of ezHDF. I provide a quick guide for those who just want to browse the whole project:

Consider we have a dataset like this:
<p align="center">
    <img src="./img/data.png">
</p>
There 6 columns with types string, integer, ..., etc. Their column names are 'int1', 'float2', ..., etc. If you want to store the data, follow the stpes:
<p align="center">
    <img src="./img/store_data.png">
</p>

If a file is stored using ezHDF, you can also explore the data using ezHDF's built API:
<p align="center">
    <img src="./img/explore_data.png">
</p>

## More Advanced Use
ezHDF is just an API of h5py. Therefore, you can absolute h5py or any other HDF5 tools to explore the file. 