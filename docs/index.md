
# 📖 Release notes
## v4.0.5
This release:
* The subprocess call to Hyrax will now raise an exception based of result code: https://bugs.earthdata.nasa.gov/browse/GHRCCLOUD-4502
* S3 exceptions for upload will no longer be caught: https://bugs.earthdata.nasa.gov/browse/GHRCCLOUD-4515
## 🏃 Migration Steps to v4.0.5
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.5
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.5/dmrpp-generator.zip"
...
}
```

## v4.0.4
This release:
* Updated the desd docker image to 3.20.13-310 which should resolve issue with the Bathy_SBES dataset.
## 🏃 Migration Steps to v4.0.4
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.4
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.4/dmrpp-generator.zip"
...
}
```

## v4.0.3
This release:
* Updated the code to remove existing dmrpp files from the granule file list before adding newly created ones.
## 🏃 Migration Steps to v4.0.3
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.3
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.3/dmrpp-generator.zip"
...
}
```

## v4.0.2
This release:
* Updated the hyrax besd version to 3.20.13-184.
## 🏃 Migration Steps to v4.0.2
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.2
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.2/dmrpp-generator.zip"
...
}
```

## v4.0.1
This release:
* Updated the hyrax besd version to 3.20.13-130.
## 🏃 Migration Steps to v4.0.1
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.1
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.1/dmrpp-generator.zip"
...
}
```

## v4.0.0
This release:
* Updated to cumulus v11.1.3
## 🏃 Migration Steps to v4.0.0
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v4.0.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v4.0.0/dmrpp-generator.zip"
...
}
```

## v3.5.0
This release:
* Uses opendap/besd:3.20.10-462 as base image
* Supports:
* * Fix Hyrax issue where it was unable to produce missing data files for level 3&4 granules that do not contain explicit domain coordinate data values


## 🏃 Migration Steps to v3.5.0
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.5.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.5.0/dmrpp-generator.zip"
...
}
``` 


## v3.4.0
This release:
* Uses opendap/besd:3.20.10-386 as base image
* Supports:
* * Fix Hyrax/OLFS generated links/URLs so that ForceLinksToHTTPS 
* * Add support for HDF5 FIllValue chunks to the dmrpp_module
* * Add support for HDF5 FillValue feature to dmr++ generation

## 🏃 Migration Steps to v3.4.0
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.4.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.4.0/dmrpp-generator.zip"
...
}
``` 

## v3.3.1
This release:
* Compatible with Cumulus v10 and v11
*  docker_image variable default to the correct release (can be override from the module definition)

## 🏃 Migration Steps to v3.3.1
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.3.1
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.3.1/dmrpp-generator.zip"
...
// Override dmrpp docker image version
docker_image = "ghrcdaac/dmrpp-generator"
...
}
``` 

## v3.3.0.beta (🚨 Not an official release)
This release:
* Compatible with Cumulus v10
* fixes issue 24 [i_24](https://github.com/ghrcdaac/dmrpp-file-generator-docker/issues/24)

## 🏃 Migration Steps to v3.3.0.beta
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.3.0.beta
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.3.0.beta/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.3.0.beta tag
docker_image = "ghrcdaac/dmrpp-generator:v3.3.0.beta
...
}
``` 


## v3.2.1
This release:
* Support turning on and off logging to cloud watch `enable_cw_logging` variable [example](https://github.com/ghrcdaac/dmrpp-generator#deploying-with-cumulus-stack)
* Allow `dmrpp_config` to be defined within the worflow configuration. The collection definition defining `dmrpp_config` will override the one defined in the workflow configuration [example](https://github.com/ghrcdaac/dmrpp-generator#cumulus-workflow-configuration)
* Fixes DMRPP logging to cloudwatch duplicate entries

## 🏃 Migration Steps to v3.2.1
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.2.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.2.1/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.2.1 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.2.1
...
// To turn off logging to cloudwatch group
enable_cw_logging =  false
}
``` 

## 🏃 Migration Steps to v3.2.0
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.2.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.2.0/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.2.0 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.2.0
...
}
``` 
## v3.2.0
This release:
* Uses opendap/besd:3.20.9-91 as base image

## 🏃 Migration Steps to v3.2.0
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.2.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.2.0/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.2.0 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.2.0
...
}
``` 


## v3.1.2
This release:
* Add logging capability to cloudwatch log groups
* Uses a simpler logic to check the file regular expression [PR 22](https://github.com/ghrcdaac/dmrpp-file-generator-docker/pull/22)
* Uses opendap/besd:3.20.9-76
* Fixes [issue 14](https://github.com/ghrcdaac/dmrpp-generator/issues/14)

## 🏃 Migration Steps to v3.1.2
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.1.2
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.1.2/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.1.2 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.1.2
...
}
``` 


## v3.1.1
This release:
* Upgrades the base cumulus module to v10.1.1
* Uses opendap/besd:3.20.9-15 

## 🚨 Breaking Changes v3.1.1
* Works with Cumulus v10.1.1
* Relays on opendap/besd:3.20.9-15

## 🏃 Migration Steps to v3.1.1
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.1.1
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.1.1/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.1.1 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.1.1
...
}
``` 

## v3.1.0
This release:
* Uses cumulus v10.1.1
* Support custom DMRPP file reg_ex
* Support creating and validating locally


## 🚨 v3.1.0 Changes
Added the ability to custom the regular expression for DMRPP generator. For example this configuration
```code

{
    "config": {
        "meta": {
            "dmrpp": {
            "dmrpp_regex" : "^.*.H6",
          "options": [
            ...
          ]
        }
    }
}
```
Will process only files with `H6` extension

## 🏃 Migration Steps to v3.1.0
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.1.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.1.0/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.1.0 tag
docker_image = "ghrcdaac/dmrpp-generator:v3.1.0
...
}
``` 



## v3.0.1.beta
This release:
* Uses cumulus v10.1.1
* Support `HDF5 | hdf5` extensions
* Support get_dmrpp options and flags 




## 🚨 Breaking Changes v3.0.1.beta
To pass the flags you need to define the meta config as follow
```
{
    ...
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
        ...
    }
    ...
}
```
Check [DMR++](https://docs.opendap.org/index.php?title=DMR%2B%2B) for DMRPP options
## 🏃 Migration Steps to v3.0.1.beta
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v3.0.1.beta
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v3.0.1.beta/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v3.0.1.beta tag
docker_image = "ghrcdaac/dmrpp-generator:v3.0.1.beta"
...
}
``` 


## v2.1.1
This release:
* Support `H5` extension 


## 🏃 Migration Steps to v2.1.1
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v2.1.1
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v2.1.1/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v2.1.1 tag
docker_image = "ghrcdaac/dmrpp-generator:v2.1.1"
...
}
``` 

## 🚨 Breaking Changes v2.1.1
None

## v2.1.0
This release:
* Fixes the issue [issue 12](https://github.com/ghrcdaac/dmrpp-generator/issues/12)

## 🏃 Migration Steps to v2.1.0
 release
```code
module "dmrpp-generator" {
// Change the source url in your terraform file to point to v2.1.0
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v2.1.0/dmrpp-generator.zip"
...
// Change the value of your docker image to point to v2.1.0 tag
docker_image = "ghrcdaac/dmrpp-generator:v2.1.0"
...
// Add destination log to remote kinesis (optional)
log_destination_arn = var.log_destination_arn
}
``` 
## 🚨 Breaking Changes v2.1.0
Only compatible with Cumulus v7+ 

## v2.0.1
This release:
* Fixes the issue of `filepath` passed from `move-granules` step function



## v2.0.0
This release:
* Fixes the issue [issue 11](https://github.com/ghrcdaac/dmrpp-generator/issues/11).


## v1.1.0
This release:
* Fixes the file type issue, now you can define a custom dmrpp file type.
* Uses a new hyrax release [base_image](https://hub.docker.com/r/opendap/besd)

## v1.0.6
This release:
* Fixes the issue of AWS provider [issue#10](https://github.com/ghrcdaac/dmrpp-generator/issues/10)
* Reads from `url_path` key passed in the payload. Also, the provider was taking off from the main.tf

## v1.0.5
This release fixes the problem adding a type of meta data for the dmrpp file and also changing some spacings.

## v1.0.4
This release fixes the problem of assuming the granuleId is the same as the file name [issue#9](https://github.com/ghrcdaac/dmrpp-generator/issues/9)




## 🏃 Migration Steps to v2.0.1
Change the source url in your terraform file to point to v2.0.0 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v2.0.1/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v2.0.1 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v2.0.1"
}



## 🏃 Migration Steps to v2.0.0
Change the source url in your terraform file to point to v2.0.0 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v2.0.0/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v2.0.0 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v2.0.0"
}

```

## Features added to v2.0.0
Now you can pass DMRPP options via collection definition.
For more info about DMRPP options please refer to [DMRPP Documentation](https://docs.google.com/presentation/d/1ZTeWjk6bUBgKP5iD2NVb_Ur8ZcvOpVbfd7pAl8c5bCs/edit#slide=id.p)

```code
{
  "name" : "foo"
  ...
  "meta": {
      "dmrpp": {
        "create_missing_cf" : "-M"    
      }
      ...
  }
  ...
}
```
`create_missing_cf` is an arbitrary key name, you can achieve the same result by passing
```code
{
  "name" : "foo"
  ...
  "meta": {
      "dmrpp": {
        "option1" : "-M"    
      }
      ...
  }
  ...
}
```
For more supported DMRPP options (example `-v`)
```code
```code
{
  "name" : "foo"
  ...
  "meta": {
      "dmrpp": {
        "option1" : "-M",
        "option2" : "-v"    
      }
      ...
  }
  ...
}
```


## 🚨 Breaking Changes v2.0.0
DMRPP activity is using `url_path` instead of `filepath`.

## 🏃 Migration Steps to v1.1.0
Change the source url in your terraform file to point to v1.1.0 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.1.0/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.1.0 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.1.0"
}

```

## 🏃 Migration Steps to v1.0.6
Change the source url in your terraform file to point to v1.0.6 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.6/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.6 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.6"
}

```

## 🏃 Migration Steps to v1.0.5
Change the source url in your terraform file to point to v1.0.5 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.5/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.5 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.5"
}

```

## 🏃 Migration Steps to v1.0.4
Change the source url in your terraform file to point to v1.0.4 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.4/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.4 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.4"
}

```
## 🚨 Breaking Changes
The workflow is accepting the whole payload 
```code
   "HyraxProcessing": {
      "Parameters": {
        "cma": {
          "event.$": "$",
          "task_config": {
            "buckets": "{$.meta.buckets}",
            "distribution_endpoint": "{$.meta.distribution_endpoint}",
            "files_config": "{$.meta.collection.files}",
            "fileStagingDir": "{$.meta.collection.url_path}",
            "granuleIdExtraction": "{$.meta.collection.granuleIdExtraction}",
            "collection": "{$.meta.collection}"
          }
        }
      },
      "Type": "Task",
      "Resource": "${module.dmrpp-generator.dmrpp_task_id}",
      "Catch": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "ResultPath": "$.exception",
          "Next": "WorkflowFailed"
        }
      ],
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 2,
          "MaxAttempts": 3
        }
      ],
      "Next": "<Your next Step>"
    }
```
