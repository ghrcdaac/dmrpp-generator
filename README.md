# dmrpp-file-generator-docker
Docker image to generate dmrpp files from netCDF and HDF files


# Generate DMRpp files locally
The folder `<path/to/nc/hdf/files>` should contain netCDF and HDF files
```code
docker run --rm -it -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
