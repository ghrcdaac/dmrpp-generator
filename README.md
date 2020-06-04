# dmrpp-file-generator-docker
Docker image to generate dmrpp files from netCDF and HDF files


# Generate DMRpp files locally
The folder `/tmp/rss` should contain netCDF and HDF files
```code
docker run --rm -it -v /tmp/rss/:/workstation dmrppfix
```
