from cumulus_process import Process, s3
from os import environ, path
from re import match, search


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

    def get_bucket(self, filename, files):
        """
        Extract the bucket from the files
        :param filename: Granule file name
        :param files: list of collection files
        :return: Bucket name
        """
        for file in files:
            if match(file.get('regex', '*.'),filename):
                return file['bucket']
        return 'public'
    
    def upload_file(self, filename):
        """ Upload a local file to s3 if collection payload provided """
        info = self.get_publish_info(filename)
        if info is None:
            return filename
        try:
            return s3.upload(filename, info['s3'], extra={}) if info.get('s3', False) else None
        except Exception as e:
            self.logger.error("Error uploading file %s: %s" % (path.basename(path.basename(filename)), str(e)))
    def process(self):
        """
        Override the processing wrapper
        :return:
        """
        input_files = self.fetch('input_files')
        self.output = self.dmrpp_generate(input_files)
        uploaded_files = self.upload_output_files()
        collection = self.config.get('collection')
        granule_data = {}
        for uploaded_file in uploaded_files:
            if uploaded_file is None or not uploaded_file.startswith('s3'):
                continue
            filename = uploaded_file.split('/')[-1]
            potential_extensions = f"({self.processing_regex})(\\.cmr.xml|\\.json.xml|\\.dmrpp)?"
            granule_id = match(potential_extensions, filename).group(1)
            if granule_id not in granule_data.keys():
                granule_data[granule_id] = {'granuleId': granule_id, 'files': []}
            granule_data[granule_id]['files'].append(
                {
                    "path": self.config.get('fileStagingDir'),
                    "url_path": self.config.get('fileStagingDir'),
                    "bucket": self.get_bucket(filename, collection.get('files', [])),
                    "filename": uploaded_file,
                    "name": uploaded_file
                }
            )

        final_output = list(granule_data.values())
        return {"granules": final_output, "input": uploaded_files}

    def get_data_access(self, key, bucket_destination):
        """
        param key: filename
        param bucket_destination: destination bucket will the file exist
        return: access URL
        """
        key = key.split('/')[-1]
        half_url = ("%s/%s/%s" % (bucket_destination, self.config['fileStagingDir'], key)).replace('//',
                                                                                                   '/')
        return "%s/%s"% (self.config.get('distribution_endpoint').rstrip('/'), half_url)

    def dmrpp_generate(self, input_files):
        """
        """
        outputs = []
        for input_file in input_files:
            if not match(f"{self.processing_regex}$", input_file):
                outputs += [input_file]
                continue
            cmd = f"get_dmrpp -b {self.path} -o {input_file}.dmrpp {path.basename(input_file)}"
            self.run_command(cmd)
            outputs += [input_file, f"{input_file}.dmrpp"]
        return outputs


if __name__ == "__main__":
    DMRPPGenerator.cli()