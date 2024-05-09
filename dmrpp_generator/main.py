import logging
import os
import time
from re import search
import subprocess
from cumulus_process import Process, s3
from cumulus_logger import CumulusLogger
from .version import __version__
from .dmrpp_options import DMRppOptions

LOGGER_TO_CW = CumulusLogger(name="DMRPP-Generator")


class CmdStd:
    """
    class to satisfy stdout and stderr
    """
    stdout = ""
    stderr = ""


class DMRPPGenerator(Process):
    """
    Class to generate dmrpp files from hdf and netCDf files
    The input will be *.nc *nc4 *.hdf
    The output *.nc.dmrpp *nc4.dmrpp *.hdf.dmrpp
    """

    def __init__(self, **kwargs):
        config = kwargs.get('config', {})
        # any keys on collection config override keys from workflow config
        self.dmrpp_meta = {
            **config.get('dmrpp', {}),  # from workflow
            **config.get('collection', {}).get('meta', {}).get('dmrpp', {}),  # from collection
        }
        self.processing_regex = self.dmrpp_meta.get(
            'dmrpp_regex', '.*\\.(((?i:(h|hdf)))(e)?5|nc(4)?)(\\.bz2|\\.gz|\\.Z)?'
        )

        super().__init__(**kwargs)
        self.path = self.path.rstrip('/') + "/"
        self.path = '/efs/lambda/'
        # Enable logging the default is True
        enable_logging = os.getenv('ENABLE_CW_LOGGING', 'True') in [True, "true", "t", 1]
        self.dmrpp_version = f"DMRPP {__version__}"
        self.logger_to_cw = LOGGER_TO_CW if enable_logging else logging
        self.logger_to_cw.info(f'config: {self.config}')
        self.timeout = int(self.dmrpp_meta.get(
            'get_dmrpp_timeout', os.getenv('GET_DMRPP_TIMEOUT', '600'))
        )
        self.enable_subprocess_logging = self.dmrpp_meta.get(
            'enable_subprocess_logging', os.getenv('ENABLE_SUBPROCESS_LOGGING', False)
        )

        self.logger_to_cw.info(f'get_dmrpp_timeout: {self.timeout}')
        self.logger_to_cw.info(f'enagled_cw_logging: {enable_logging}')
        self.logger_to_cw.info(f'enable_subprocess_logging: {self.enable_subprocess_logging}')

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
            if search(collection_file.get('regex', '*.'), filename):
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
            if search(file.get('regex', '*.'), filename):
                bucket_type = file['bucket']
                break
        return buckets[bucket_type]

    def upload_file_to_s3(self, filename, uri):
        """ Upload a local file to s3 if collection payload provided """
        return s3.upload(filename, uri, extra={})

    def process(self):
        """
        Override the processing wrapper
        :return:
        """
        self.logger_to_cw.info(f'listdir: {os.listdir("/efs/lambda/")}')
        collection = self.config.get('collection')
        collection_files = collection.get('files', [])
        buckets = self.config.get('buckets')
        granules = self.input['granules']
        for granule in granules:
            dmrpp_files = []
            for file_ in granule['files']:
                self.logger_to_cw.info(f'file: {file_}')
                if not search(f"{self.processing_regex}$", file_['fileName']):
                    self.logger_to_cw.debug(f"{self.dmrpp_version}: regex {self.processing_regex}"
                                            f" does not match filename {file_['fileName']}")
                    continue
                self.logger_to_cw.debug(f"{self.dmrpp_version}: regex {self.processing_regex}"
                                        f" matches filename to process {file_['fileName']}")
                input_file_path = file_.get('fileName', f's3://{file_["bucket"]}/{file_["key"]}')
                self.logger_to_cw.info(f'input_file_path: {input_file_path}')
                temp = f'/efs/lambda/{input_file_path}'
                local = os.path.isfile(temp)
                self.logger_to_cw.info(f'local: {local}')
                output_file_paths = self.dmrpp_generate(
                    input_file=temp, local=local, dmrpp_meta=self.dmrpp_meta
                )

                for output_file_path in output_file_paths:
                    if output_file_path:
                        output_file_basename = os.path.basename(output_file_path)
                        dmrpp_file = {
                            "bucket": self.get_bucket(output_file_basename, collection_files, buckets)['name'],
                            "fileName": output_file_basename,
                            "key": os.path.join(os.path.dirname(file_.get('key')), output_file_basename),
                            "size": os.path.getsize(output_file_path),
                            "type": self.get_file_type(output_file_basename, collection_files),
                        }
                        dmrpp_files.append(dmrpp_file)
                        upload_location = f's3://{dmrpp_file["bucket"]}/{dmrpp_file["key"]}'
                        self.logger_to_cw.info(f'upload_location: {upload_location}')
                        self.upload_file_to_s3(output_file_path, f's3://{dmrpp_file["bucket"]}/{dmrpp_file["key"]}')

            if dmrpp_files == 0:
                raise Exception(f'No dmrpp files were produced for {granule}')

            self.strip_old_dmrpp_files(granule)
            granule['files'] += dmrpp_files

        self.verify_outputs_produced(granules)

        return self.input

    def clean_all(self):
        self.logger_to_cw.info('Not cleaning')

    @staticmethod
    def strip_old_dmrpp_files(granule):
        # Remove old dmrpp files if they exist before adding new ones
        i = 0
        while i < len(granule['files']):
            temp = granule['files'][i]
            if str(temp.get('fileName')).endswith('dmrpp'):
                granule['files'].pop(i)
            else:
                i += 1

    @staticmethod
    def verify_outputs_produced(granules):
        has_output = False
        for granule in granules:
            for file in granule['files']:
                if str(file.get('fileName')).endswith('dmrpp'):
                    has_output = True
                    break
            if has_output:
                break

        if not has_output:
            raise Exception('No dmrpp outputs produced.')

    def get_dmrpp_command(self, dmrpp_meta, input_path, output_filename, local=False):
        """
        Getting the command line to create DMRPP files
        """
        dmrpp_meta = dmrpp_meta if isinstance(dmrpp_meta, dict) else {}
        dmrpp_options = DMRppOptions(self.path)
        options = dmrpp_options.get_dmrpp_option(dmrpp_meta=dmrpp_meta)
        local_option = f"-u file://{output_filename}" if '-u' in options else ''

        s_option = ''
        if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
            s_option = '-s /etc/bes/site.conf'

        dmrpp_cmd = f"get_dmrpp {s_option} {options} {input_path} -o {output_filename}.dmrpp" \
                    f" {local_option} {os.path.basename(output_filename)}"
        return " ".join(dmrpp_cmd.split())

    def add_missing_files(self, dmrpp_meta, file_name):
        """
        Adds missing file
        """
        # If the missing file was not generated
        if not os.path.isfile(file_name):
            return []
        # If it was generated and the flag was set
        options = dmrpp_meta.get('options', [])
        if {'flag': '-M'} in options:
            return [file_name]
        return []

    def run_command(self, cmd):
        """ Run cmd as a system command """
        stdout = None
        stderr = None

        if self.enable_subprocess_logging:
            stdout = subprocess.PIPE
            stderr = subprocess.STDOUT

        self.logger_to_cw.info(f'Running cmd: {cmd}')
        out = subprocess.run(cmd.split(), stdout=stdout, stderr=stderr, timeout=self.timeout, check=True)

        return out

    def dmrpp_generate(self, input_file, local=False, dmrpp_meta=None, args=None):
        """
        Generate DMRPP from S3 file
        """
        # Force dmrpp_meta to be an object
        dmrpp_meta = dmrpp_meta if isinstance(dmrpp_meta, dict) else {}
        file_name = input_file if local else s3.download(input_file, path=self.path)
        self.logger_to_cw.info(f'file_name: {file_name}')
        cmd = self.get_dmrpp_command(dmrpp_meta, self.path, file_name, local)
        if args:
            cmd_split = cmd.split(' ', maxsplit=1)
            cmd = f'{cmd_split[0]} {" ".join(args)} {cmd_split[1]}'
        self.run_command(cmd)
        out_files = [f"{file_name}.dmrpp"] + self.add_missing_files(dmrpp_meta, f'{file_name}.dmrpp.missing')
        return out_files


def main(event, context):
    print('main event')
    print(event)
    return DMRPPGenerator(**event).process()


if __name__ == "__main__":
    dmr = DMRPPGenerator(input=[], config={})
    meta = {"options": [{"flag": "-s", "opt": "htp://localhost/config.conf", "download": "true"}, {"flag": "-M"}]}
    dmr.get_dmrpp_command(meta, dmr.path, "file_name.nc")
