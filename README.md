# dmrpp-file-generator-docker
Docker image and commandline utility to generate dmrpp files from netCDF and HDF files.

# Supported get_dmrpp configuration
## Via env vars
Create a PAYLOAD environment variable holding dmrpp options
```
PAYLOAD='{"dmrpp_regex": "^.*.nc4", "options":[{"flag": "-M"}, {"flag": "-s", "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config","download": "true"}]}'
```
# Generate DMRpp files locally without Hyrax server
```
$./generate_and_validate_dmrpp --help
usage: generate_and_validate_dmrpp [-h] -p NC_HDF_PATH [-prt PORT]
                                   [-pyld PAYLOAD] [-vldt VALIDATE]

Generate and validate DMRPP files.

optional arguments:
  -h, --help            show this help message and exit
  -p NC_HDF_PATH, --path NC_HDF_PATH
                        Path to netCDF4 and HDF5 folder
  -prt PORT, --port PORT
                        Port number to Hyrax local server
  -pyld PAYLOAD, --payload PAYLOAD
                        Payload to execute get_dmrpp binary
  -vldt VALIDATE, --validate VALIDATE
                        Validate netCDF4 and HDF5 files against OPeNDAP local
                        server
```

The folder `<path/to/nc/hdf/files>` should contain netCDF and/or HDF files
```code
./generate_and_validate_dmrpp -p <path/to/nc/hdf/files> -vldt false
Note: If you don't have python3 in /usr/bin/python run the command with your explicit python
generate_and_validate_dmrpp -p <path/to/nc/hdf/files> -vldt false
```
<a href="https://asciinema.org/a/UbhNufu2FsHqiDCWvOaqMQykk" target="_blank"><img src="https://asciinema.org/a/UbhNufu2FsHqiDCWvOaqMQykk.svg" /></a>
# Generate DMRpp files locally with Hyrax server (for validation)

```code
./generate_and_validate_dmrpp -p <path/to/nc/hdf/files>
A prompt will ask you to visit localhost:8080
# If you want to change the default port run the command with
./generate_and_validate_dmrpp -p <path/to/nc/hdf/files> -prt 8889
Now you can validate the result in localhost:8889
```

<a href="https://asciinema.org/a/Tzcgm0FwT6smYF520f3uqxvMu" target="_blank"><img src="https://asciinema.org/a/Tzcgm0FwT6smYF520f3uqxvMu.svg" /></a>

# Generate missing metadata for non-netcdf compliant data (the -b switch)
```code
./generate_and_validate_dmrpp -p <path/to/nc/hdf/files> -pyld $PAYLOAD
```
or 
```code
docker run --rm -it --env-file ./env.list -v <path/to/nc/hdf/files>:/workstation ghrcdaac/dmrpp-generator
```
where PAYLOAD contains your flags and switches
```code
PAYLOAD={"options":[{"flag": "-M"}, {"flag": "-u", "opt": "/usr/share/hyrax"}]}
```
