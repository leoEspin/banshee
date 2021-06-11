#!/bin/bash

conda remove -y --name banshee --all
# remove associated kernel
jupyter kernelspec uninstall banshee
# can check if kernel was removed here:
ls ~/.local/share/jupyter/kernels