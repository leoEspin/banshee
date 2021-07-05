#!/bin/bash

# conda create -n banshee python=3.9.1
# conda activate banshee
#conda install -c anaconda lxml
# conda install pandas
# conda install ipykernel

conda env create -f env.yaml
# add new env. as a jupyter kernel
eval "$(conda shell.bash hook)"
conda activate banshee
python -m ipykernel install --user --name=banshee
conda deactivate banshee
