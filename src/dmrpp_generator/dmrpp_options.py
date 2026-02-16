import logging
import os
import re
from typing import Any
from tempfile import mkdtemp

import boto3
import requests


class DMRppOptions:
    """
    DMRpp Options
    """

    def __init__(self, host_path: str = mkdtemp()):
        self.s3_client = boto3.client("s3")
        self.session = requests.Session()
        self.host_path = host_path.rstrip("/")

    def _download_files(self, link: str) -> str:
        """
        Calls the corresponding download function for the url's protocol.
        :param link: Location to find the file to download
        """
        filename = os.path.basename(link)
        local_path = f"{self.host_path}/{filename}"
        protocol = ""
        if p_match := re.match(r".+?(?=:)", link):
            protocol = p_match.group()

        if not os.path.isfile(local_path):
            match protocol:
                case "http" | "https":
                    self._get_http_file(
                        link=link, local_path=local_path, protocol=protocol
                    )
                case "s3":
                    self._get_s3_file(
                        link=link, local_path=local_path, protocol=protocol
                    )
                case _:
                    self._switcher_default(protocol, link=link, local_path=local_path)
        return local_path

    @staticmethod
    def _switcher_default(protocol: str, **kwargs) -> None:
        """
        Logs unsupported protocol and raises an exception.
        """
        message = (
            f"The protocol {protocol} is not implemented yet: called using {kwargs}"
        )
        logging.error(message)
        raise Exception(message)

    def _get_http_file(self, link: str, local_path: str, **kwargs) -> None:
        """
        Downloads the file at the url and stores it at the local path.
        :param url: Url of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        try:
            response = self.session.get(link)
            with open(local_path, "wb") as file:
                file.write(response.content)
        except Exception as err:
            err_msg = f"called using {kwargs}, error : {err}"
            logging.error(msg=str(err_msg))
            raise err
        pass

    def _get_s3_file(self, link: str, local_path: str, **kwargs) -> None:
        """
        Downloads the file at the s3_link and stores it at the local path.
        :param s3_link: s3 link of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        bucket_name = ""
        key = ""
        if reg_res := re.match(r"^.*://([^/]*)/(.*)", link):
            bucket_name = reg_res.group(1)
            key = reg_res.group(2)
        try:
            self.s3_client.download_file(bucket_name, key, local_path)
        except Exception as err:
            err_msg = f"called using {kwargs}, error : {err}"
            logging.error(msg=str(err_msg))
            raise err
        pass

    def get_dmrpp_option(self, dmrpp_meta: dict[str, Any]) -> str:
        """
        :param dmrpp_meta: DMR meta string
        :return A sequential string with the flags and URLs in order
        """
        res_str = ""
        for option in dmrpp_meta.get("options", []):
            flag = option.get("flag")
            if not flag:
                raise Exception("A DMRPP flag should be present")
            res_str = f"{res_str} {flag}"
            file_link = option.get("opt", "")
            download = option.get("download") == "true"
            location = self._download_files(file_link) if download else file_link
            res_str = f"{res_str} {location}"
        return " ".join(f"{res_str}".split())
