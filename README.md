# dmrpp-file-generator-docker
Docker image to generate dmrpp files from netCDF and HDF files
# Supported get_dmrpp configuration

## Via Cumulus configuration
```code
{
    "config": {
        "dmrpp": {
            "create_missing_cf" : true    
        }
    }
}
```
## Via env vars

| Environment Variable | Valid Values | Tool flag | Description |
| -----------          | ------------ | ----------| ----------- | 
| CREATE_MISSING_CF    | true,false   | -M        | Create and merge missing CF coordinate domain variables into the dmrpp. If there are missing variables, a sidecar file named input_file_name_missing.suffix will be created in the same directory location as the input_data_file. |

# Generate DMRpp files locally
The folder `<path/to/nc/hdf/files>` should contain netCDF and HDF files
```code
docker run --rm -it -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
# Generate missing metadata for non-netcdf compliant data (the -b switch)
```code
docker run --rm -it --env CREATE_MISSING_CF=true -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
or 
```code
docker run --rm -it --env-file ./env.list -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
where the file env.list contains
```code
CREATE_MISSING_CF=true
```
