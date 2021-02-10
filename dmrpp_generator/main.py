from cumulus_process import Process, s3
import os
from re import match, search
import copy

def nsidc_debug(msg):
    with open('log.txt', 'a') as f:
        f.write(str(msg))
        f.write('\n')
        f.write('\n')
    s3.upload('log.txt', 's3://nsidc-cumulus-int-internal/logging/log.txt')

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

    
    def upload_file(self, filename, uri):
        """ Upload a local file to s3 if collection payload provided """
        try:
            return s3.upload(filename, uri, extra={})
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
        for granule in granules:
            dmrpp_files = []
            for file_ in granule['files']:
                if not match(f"{self.processing_regex}$", file_['filename']):
                    continue
                nsidc_debug(f"file_='{file_}'")
                output_file_path = self.dmrpp_generate(file_['filename'])
                if output_file_path:
                    dmrpp_file = {
                        "bucket": self.get_bucket(file_['filename'], collection.get('files', []),buckets)['name'],
                        "name": os.path.basename(output_file_path),
                        "size": os.path.getsize(output_file_path),
                        "url_path": file_['url_path'],
                        "type": "metadata"
                    }
                    dmrpp_file['filename'] = f's3://{dmrpp_file["bucket"]}/{dmrpp_file["url_path"]}/{dmrpp_file["name"]}'
                    nsidc_debug(f"dmrpp_file='{dmrpp_file}'")
                    dmrpp_files.append(dmrpp_file)
                    self.upload_file(output_file_path, dmrpp_file['filename'])
            granule['files'] += dmrpp_files
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
        try:
            file_name = s3.download(input_file, path=self.path)
            cmd = f"get_dmrpp -b {self.path} -o {file_name}.dmrpp {os.path.basename(file_name)}"
            self.run_command(cmd) 
            return f"{file_name}.dmrpp"
        except Exception as ex:
            self.logger.error(f"DMRPP error {ex}")
            return None

if __name__ == "__main__":
    DMRPPGenerator.cli()