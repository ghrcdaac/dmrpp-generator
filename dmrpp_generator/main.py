from cumulus_process import Process, s3
from .dmrpp_options import DMRppOptions
import os
from re import match
import logging

class DMRPPGenerator(Process):
    """
    Class to generate dmrpp files from hdf and netCDf files
    The input will be *.nc *nc4 *.hdf
    The output *.nc.dmrpp *nc4.dmrpp *.hdf.dmrpp
    """

    def __init__(self, **kwargs):
        self.processing_regex = '.*\\.(((?i:(h|hdf)))(e)?5|nc(4)?)(\\.bz2|\\.gz|\\.Z)?'
        super(DMRPPGenerator, self).__init__(**kwargs)
        self.path = self.path.rstrip('/') + "/"

    @property
    def input_keys(self):

        return {
            'input_files': f"{self.processing_regex}(\\.cmr\\.xml|\\.json)?$"
        }

    @staticmethod
    def get_file_type(filename, files):
        """
        Get custom file type, default to metadata
        :param filename: Granule file name
        :param files: list of collection files
        :return: file type if defined
        """

        for collection_file in files:
            if match(collection_file.get('regex', '*.'), filename):
                return collection_file.get('type', 'metadata')
        return 'metadata'

    @staticmethod
    def get_bucket(filename, files, buckets):
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

    def upload_file_to_s3(self, filename, uri):
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
        collection_files = collection.get('files', [])
        collection_meta = collection.get('meta', {})
        dmrpp_meta = collection_meta.get('dmrpp', {})
        buckets = self.config.get('buckets')
        granules = self.input['granules']
        for granule in granules:
            dmrpp_files = []
            for file_ in granule['files']:
                if not match(f"{self.processing_regex}$", file_['filename']):
                    continue
                output_file_paths = self.dmrpp_generate(input_file=file_['filename'],
                                                       dmrpp_meta=dmrpp_meta)
                for output_file_path in output_file_paths:
                    output_file_basename = os.path.basename(output_file_path)
                    url_path = file_.get('url_path', self.config.get('fileStagingDir'))
                    filepath = os.path.dirname(file_.get('filepath', url_path))
                    if output_file_path:
                        dmrpp_file = {
                        "name": os.path.basename(output_file_path),
                        "path": self.config.get('fileStagingDir'),
                        "url_path": url_path,
                        "bucket": self.get_bucket(output_file_basename, collection_files, buckets)['name'],
                        "size": os.path.getsize(output_file_path),
                        "type": self.get_file_type(output_file_basename, collection_files)
                        }
                        dmrpp_file['filepath'] = f"{filepath}/{dmrpp_file['name']}".lstrip('/')
                        dmrpp_file['filename'] = f's3://{dmrpp_file["bucket"]}/{dmrpp_file["filepath"]}'
                        dmrpp_files.append(dmrpp_file)
                        self.upload_file_to_s3(output_file_path, dmrpp_file['filename'])
            granule['files'] += dmrpp_files
        return self.input

    def get_dmrpp_command(self, dmrpp_meta, input_path, output_filename, local=False):
        """
        Getting the command line to create DMRPP files
        """
        dmrpp_meta = dmrpp_meta if isinstance(dmrpp_meta, dict) else {}
        dmrpp_options = DMRppOptions(self.path)
        options = dmrpp_options.get_dmrpp_option(dmrpp_meta=dmrpp_meta)
        local_option = f"-u file://{output_filename}" if local else ""
        dmrpp_cmd = f"get_dmrpp {options} {input_path} -o {output_filename}.dmrpp {local_option} {os.path.basename(output_filename)}"
        return " ".join(dmrpp_cmd.split())


    def add_missing_files(self, dmrpp_meta, file_name):
        """
        """
        # If the missing file was not generated
        if not os.path.isfile(file_name):
            return []
        # If it was generated and the flag was set
        options = dmrpp_meta.get('options', [])
        if {'flag': '-M'} in options:
            return [file_name]
        return []

    def dmrpp_generate(self, input_file, local=False, dmrpp_meta=None):
        """
        Generate DMRPP from S3 file
        """
        # Force dmrpp_meta to be an object
        dmrpp_meta = dmrpp_meta if isinstance(dmrpp_meta, dict) else {}
        # If not running locally use Cumulus logger
        logger = logging if local else self.logger
        cmd_output = ""
        try:
            file_name = input_file if local else s3.download(input_file, path=self.path)
            cmd = self.get_dmrpp_command(dmrpp_meta, self.path, file_name, local)
            cmd_output = self.run_command(cmd)
            out_files = [f"{file_name}.dmrpp"] + self.add_missing_files(dmrpp_meta, f'{file_name}.dmrpp.missing')
            return out_files

        except Exception as ex:
            logger.error(f"DMRPP error {ex}: {cmd_output}")
            return []


if __name__ == "__main__":
    dmr = DMRPPGenerator(input = [], config = {})
    meta = {"options": [{"flag": "-s", "opt": "htp://localhost/config.conf", "download": "true"}, {"flag": "-M"}]}
    dmr.get_dmrpp_command(meta, dmr.path, "file_name.nc")

