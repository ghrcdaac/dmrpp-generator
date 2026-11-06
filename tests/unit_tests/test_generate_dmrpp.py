import copy
import os
from collections.abc import Callable
from typing import Any

import pytest

from dmrpp_generator.main import DMRPPGenerator

GRANULE_NAME = "ISS_LIS_BG_V3.0_20170702_000346_FIN.nc"
HDF_GRANULE_NAME = "ISS_LIS_BG_V3.0_20170702_000346_FIN.hdf"
EXPECTED_HDF_FILE_COUNT = 5


@pytest.fixture
def dmrpp_output(
    process_factory: Callable[..., DMRPPGenerator],
    mock_process_pipeline: Callable[..., None],
    isolated_granule: Callable[[str], str],
) -> tuple[DMRPPGenerator, dict[str, Any]]:
    """Run process() against a real netCDF granule in an isolated tmp dir."""
    working_dir = isolated_granule(GRANULE_NAME)
    mock_process_pipeline(GRANULE_NAME, source_dir=working_dir)
    process_instance = process_factory(GRANULE_NAME, path=working_dir)
    return process_instance, process_instance.process()


def test_dmrpp_file_created(
    dmrpp_output: tuple[DMRPPGenerator, dict[str, Any]],
) -> None:
    """The generated .dmrpp file should exist on disk."""
    process_instance, _ = dmrpp_output
    expected_file_path = f"{process_instance.path}/{GRANULE_NAME}.dmrpp"
    assert os.path.exists(expected_file_path)


def test_output_schema(dmrpp_output: tuple[DMRPPGenerator, dict[str, Any]]) -> None:
    """The process output should only contain the 'granules' key."""
    _, output = dmrpp_output
    assert list(output.keys()) == ["granules"]


def test_dmrpp_file_present_in_output(
    dmrpp_output: tuple[DMRPPGenerator, dict[str, Any]],
) -> None:
    """The generated .dmrpp file should be listed in the output granule files."""
    _, output = dmrpp_output
    dmrpp_file = f"{GRANULE_NAME}.dmrpp"
    filenames = {
        file["fileName"] for granule in output["granules"] for file in granule["files"]
    }
    assert dmrpp_file in filenames


def test_s3_extra_requester_pay_default(
    process_factory: Callable[..., DMRPPGenerator],
) -> None:
    """requester_pay defaults to disabled, so no extra S3 args are added."""
    process_instance = process_factory(GRANULE_NAME)
    extra_dict = process_instance._get_s3_extra()
    assert not extra_dict


def test_s3_extra_requester_pay_enabled(
    process_factory: Callable[..., DMRPPGenerator],
    payload_rp_data: dict[str, Any],
) -> None:
    """requester_pay enabled in the collection meta should add RequestPayer."""
    process_instance = process_factory(GRANULE_NAME, config=payload_rp_data)
    extra_dict = process_instance._get_s3_extra()
    assert extra_dict["RequestPayer"] == "requester"


def test_fail_on_no_matching_regex(
    process_factory: Callable[..., DMRPPGenerator],
    mock_process_pipeline: Callable[..., None],
    isolated_granule: Callable[[str], str],
) -> None:
    """https://eosdis.slack.com/archives/CQF7K5U82/p1756324842641589?thread_ts=1755709180.274919&cid=CQF7K5U82
    When a file created by the dmrpp process does not match any of the file regexes
    defined within the collection definition, the process should fail.
    """
    working_dir = isolated_granule(HDF_GRANULE_NAME)
    mock_process_pipeline(HDF_GRANULE_NAME, source_dir=working_dir)
    process_instance = process_factory(HDF_GRANULE_NAME, path=working_dir)

    with pytest.raises(Exception) as exception_test:
        process_instance.process()
    assert str(exception_test.value) == (
        "File 'ISS_LIS_BG_V3.0_20170702_000346_FIN.hdf_mvs.h5' does not match any "
        "file regex defined within the collection definition."
    )


def test_strip_old_inputs(
    process_factory: Callable[..., DMRPPGenerator],
    mock_process_pipeline: Callable[..., None],
    isolated_granule: Callable[[str], str],
    config_data: dict[str, Any],
) -> None:
    """Old dmrpp/mvs.h5 file entries already on the granule should be stripped
    and replaced by the newly generated ones.
    """
    working_dir = isolated_granule(HDF_GRANULE_NAME)
    mock_process_pipeline(HDF_GRANULE_NAME, source_dir=working_dir)

    local_config = copy.deepcopy(config_data)
    local_config["collection"]["files"].append(
        {
            "bucket": "protected",
            "regex": r"^ISS_LIS_BG_V3.\d_.*_mvs\.h5$",
            "sampleFileName": "ISS_LIS_BG_V3.0_20231116_203042_FIN.hdf_mvs.h5",
        }
    )
    process_instance = process_factory(
        HDF_GRANULE_NAME,
        config=local_config,
        path=working_dir,
        extra_files=[
            {
                "bucket": "fake-cumulus-protected",
                "fileName": f"{HDF_GRANULE_NAME}.dmrpp",
                "key": f"{HDF_GRANULE_NAME}.dmrpp",
                "size": 18232,
                "type": "metadata",
            },
            {
                "bucket": "fake-cumulus-protected",
                "fileName": f"{HDF_GRANULE_NAME}_mvs.h5",
                "key": f"fakepath/2020/001/{HDF_GRANULE_NAME}_mvs.h5",
                "size": 11645,
                "type": "metadata",
            },
        ],
    )

    output = process_instance.process()
    assert len(output["granules"][0]["files"]) == EXPECTED_HDF_FILE_COUNT
