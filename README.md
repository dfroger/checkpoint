# checkpoint

Checkpoints are like unit-tests inlined in your code.

## Development 

Create a `Conda` environment:

    conda create -n checkpoint python=3.5 h5py pyyaml

Install `checkpoint` in development mode:

    source activate checkpoint
    pip install -e .

Run tests:

    cd checkpoint/test
    python test_checkpoint.py
