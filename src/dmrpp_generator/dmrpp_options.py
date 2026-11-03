import logging
import os
import re
from tempfile import mkdtemp
import boto3
import requests


class DMRppOptions:
    """
    DMRpp Options
    """
    def __init__(self, host_path=mkdtemp()) -> None:
        self.s3_client = boto3.client('s3')
        self.session = requests.Session()
        self.host_path = host_path.rstrip("/")

    def __download_files(self, link):
        """
        Calls the corresponding download function for the url's protocol.
        :param link: Location to find the file to download
        """
        filename = os.path.basename(link)
        local_path = f'{self.host_path}/{filename}'
        protocol = re.match(r'.+?(?=:)', link).group()
        switcher = {'http': self.__get_http_file, 'https': self.__get_http_file,
                    's3': self.__get_s3_file}
        if not os.path.isfile(local_path):
            switcher.get(protocol, self.__switcher_default)(link=link, local_path=local_path, protocol=protocol)
        return local_path

    @staticmethod
    def __switcher_default(protocol, **kwargs):
        """

        """
        message = f"The protocol {protocol} is not implemented yet: called using {kwargs}"
        logging.error(message)
        raise Exception(message)

    def __get_http_file(self, link, local_path, **kwargs):
        """
        Downloads the file at the url and stores it at the local path.
        :param url: Url of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        try:
            response = self.session.get(link)
            with open(local_path, 'wb') as file:
                file.write(response.content)
        except Exception as err:
            err_msg = f"called using {kwargs}, error : {err}"
            logging.error(msg=str(err_msg))
            raise err
        pass

    def __get_s3_file(self, link, local_path, **kwargs):
        """
        Downloads the file at the s3_link and stores it at the local path.
        :param s3_link: s3 link of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        reg_res = re.match(r'^.*://([^/]*)/(.*)', link)
        bucket_name = reg_res.group(1)
        key = reg_res.group(2)
        try:
            self.s3_client.download_file(bucket_name, key, local_path)
        except Exception as err:
            err_msg = f"called using {kwargs}, error : {err}"
            logging.error(msg=str(err_msg))
            raise err
        pass

    def get_dmrpp_option(self, dmrpp_meta):
        """
        :param dmrpp_meta: DMR meta string
        :return A sequential string with the flags and URLs in order
        """
        res_str = ''
        for option in dmrpp_meta.get('options', []):
            flag = option.get('flag')
            if not flag:
                raise Exception("A DMRPP flag should be present")
            res_str = f'{res_str} {flag}'
            file_link = option.get('opt', '')
            download = option.get('download') == 'true'
            location = self.__download_files(file_link) if download else file_link
            res_str = f'{res_str} {location}'
        return " ".join(f"{res_str}".split())


if __name__ == '__main__':
    pass
