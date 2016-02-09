# clickle
Store Python Class data members in HDF5 files

# development 

Create a `Conda` environment:

    conda create -n clash python=3.5 h5py pyyaml

Install `clash` in development mode:

    source activate clash
    pip install -e .

Run tests:

    cd clash/test
    python test_clash.py
