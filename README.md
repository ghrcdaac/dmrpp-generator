# dmrpp-file-generator-docker
Docker image to generate dmrpp files from netCDF and HDF files
# Supported get_dmrpp configuration

## Via Cumulus configuration
```code
{
    "config": {
        "meta": {
            "dmrpp": {
          "options": [
            {
              "flag": "-M"
            },
            {
              "flag": "-s",
              "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config",
              "download": "true"
            },
            {
              "flag": "-c",
              "opt": "s3://ghrcsbxw-public/aces1cont__1/aces1cont_2002.212_v2.50.tar.cmr.json",
              "download": "false"
            }
          ]
        }
    }
}
```

`opt` is the value that will come after the flag, if provided with `"download": "true"` the value will be ignored and the file provided will be downloaded and used with the `flag`. 
If the `opt` is provided with `"download": "false"` or without `download` the value of `opt` will be used as a letteral string in `get_dmrpp` executable.
We are supporting HTTP and s3 protocols.

## Via env vars
Create a PAYLOAD environment variable holding dmrpp options
```
PAYLOAD='{"options":[{"flag": "-M"}, {"flag": "-s", "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config","download": "true"}]}'
```
# Generate DMRpp files locally
The folder `<path/to/nc/hdf/files>` should contain netCDF and/or HDF files
```code
docker run --rm -it -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
# Generate missing metadata for non-netcdf compliant data (the -b switch)
```code
docker run --rm -it --env PAYLOAD=$PAYLOAD -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
or 
```code
docker run --rm -it --env-file ./env.list -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
where the file env.list contains
```code
PAYLOAD={"options":[{"flag": "-M"}, {"flag": "-s", "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config","download": "true"}]}
```
