from cumulus_process import Process, s3
import os
from re import match, search
import copy


class DMRPPGenerator(Process):
    """
    Class to generate dmrpp files from hdf and netCDf files
    The input will be *.nc *nc4 *.hdf
    The output *.nc.dmrpp *nc4.dmrpp *.hdf.dmrpp
    """

    def __init__(self, **kwargs):
        self.processing_regex = '.*\\.(h(e)?5|nc(4)?)(\\.bz2|\\.gz|\\.Z)?'
        super(DMRPPGenerator, self).__init__(**kwargs)
        self.path = self.path.rstrip('/') + "/"


    @property
    def input_keys(self):

        return {
            'input_files': f"{self.processing_regex}(\\.cmr\\.xml|\\.json)?$"
        }


    def get_bucket(self, filename, files, buckets):
        """
        Extract the bucket from the files
        :param filename: Granule file name
        :param files: list of collection files
        :param buckets: Object holding buckets info
        :return: Bucket object
        """
        bucket_type = "public"
        for file in files:
            if match(file.get('regex', '*.'), filename):
                bucket_type = file['bucket']
                break
        return buckets[bucket_type]

    
    def upload_file(self, filename):
        """ Upload a local file to s3 if collection payload provided """
        info = self.get_publish_info(filename)
        if info is None:
            return filename
        try:
            return s3.upload(filename, info['s3'], extra={}) if info.get('s3', False) else None
        except Exception as e:
            self.logger.error("Error uploading file %s: %s" % (os.path.basename(os.path.basename(filename)), str(e)))

    

    def process(self):
        """
        Override the processing wrapper
        :return:
        """
        collection = self.config.get('collection')
        buckets = self.config.get('buckets')
        granules = self.input['granules']
        append_output = {}
        for granule in granules:
            granule_id = granule['granuleId']
            for file_ in granule['files']:
                output_file_path = self.dmrpp_generate(file_['filename'])
                if output_file_path:
                    s3_path = output_file_path.get('s3_path')
                    file_local_path = output_file_path.get('file_local_path')
                    append_output[granule_id] = append_output.get(granule_id, {'files': []})
                    append_output[granule_id]['files'].append(
                        {
                "bucket": self.get_bucket(file_['filename'], collection.get('files', []),buckets)['name'],
                "filename": s3_path,
                "name": os.path.basename(file_local_path),
                "size": os.path.getsize(file_local_path),
                "path": self.config.get('fileStagingDir'),
                "url_path": self.config.get('fileStagingDir')
                        }
                    )
        for granule in granules:
            granule_id = granule['granuleId']
            if append_output.get(granule_id, False):
                granule['files'] += append_output[granule_id]['files']
            
        return self.input


    def get_data_access(self, key, bucket_destination):
        """
        param key: filename
        param bucket_destination: destination bucket will the file exist
        return: access URL
        """
        key = key.split('/')[-1]
        half_url = ("%s/%s/%s" % (bucket_destination, self.config['fileStagingDir'], key)).replace('//','/')
        return "%s/%s"% (self.config.get('distribution_endpoint').rstrip('/'), half_url)


    def dmrpp_generate(self, input_file):
        """
        """
        if not match(f"{self.processing_regex}$", input_file):
            return {}
        try:
            file_name = s3.download(input_file, path=self.path)
            cmd = f"get_dmrpp -b {self.path} -o {file_name}.dmrpp {os.path.basename(file_name)}"
            self.run_command(cmd) 
            return {'file_local_path': f"{file_name}.dmrpp", 's3_path': self.upload_file(f"{file_name}.dmrpp")}
        except Exception as ex:
            self.logger.error(f"DMRPP error {ex}")
        return {}

if __name__ == "__main__":
    DMRPPGenerator.cli()