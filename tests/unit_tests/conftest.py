import json
import os
import shutil
from collections.abc import Callable
from typing import Any

import pytest

from dmrpp_generator.main import DMRPPGenerator


@pytest.fixture(scope="session")
def fixture_path() -> str:
    return os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope="session")
def granule_id() -> str:
    return "ISS_LIS_BG_V3.0_20170702_000346_FIN"


@pytest.fixture(scope="module")
def config_data(fixture_path: str) -> dict[str, Any]:
    with open(os.path.join(fixture_path, "payload.json"), encoding="UTF-8") as fle:
        return json.load(fle)["config"]


@pytest.fixture(scope="module")
def payload_rp_data(fixture_path: str) -> dict[str, Any]:
    with open(
        os.path.join(fixture_path, "payload_requester_pay.json"), encoding="UTF-8"
    ) as fle:
        return json.load(fle)["config"]


@pytest.fixture
def process_factory(
    granule_id: str, config_data: dict[str, Any], fixture_path: str
) -> Callable[..., DMRPPGenerator]:
    def _make_instance(
        filename,
        config: dict[str, Any] | None = None,
        path: str | None = None,
        extra_files: list[dict[str, Any]] | None = None,
    ) -> DMRPPGenerator:
        input_file = {
            "granules": [
                {
                    "granuleId": granule_id,
                    "sync_granule_duration": 3759,
                    "files": [
                        {
                            "bucket": "fake-cumulus-protected",
                            "checksum": "aa5204f125ae83847b3b80fa2e571b00",
                            "checksumType": "md5",
                            "fileName": filename,
                            "key": f"fakepath/2020/001/{filename}",
                            "size": 18232098,
                            "type": "data",
                        },
                        {
                            "bucket": "fake-cumulus-public",
                            "fileName": f"{filename}.md5",
                            "key": f"fakepath/2020/001/{filename}.md5",
                            "size": 98,
                            "type": "metadata",
                        },
                        {
                            "bucket": "fake-cumulus-public",
                            "fileName": f"{filename}.cmr.json",
                            "key": f"{filename}.cmr.json",
                            "size": 1381,
                            "type": "metadata",
                        },
                        *(extra_files or []),
                    ],
                    "version": "2019.0",
                }
            ]
        }
        return DMRPPGenerator(
            input=input_file, config=config or config_data, path=path or fixture_path
        )

    return _make_instance


@pytest.fixture(scope="session")
def dmrpp_cli(fixture_path) -> DMRPPGenerator:
    return DMRPPGenerator(input=[], config={}, path=fixture_path)


@pytest.fixture
def isolated_granule(tmp_path, fixture_path: str) -> Callable[[str], str]:
    """Copy a fixture granule file into a private tmp dir.

    gen_dmrpp_side_car writes its output next to the input file, so running
    process() against the shared fixtures/ directory would let output from one
    test leak into the next (dmrpp_generate() scans the whole working
    directory for output files). Copying the single file we need into an
    isolated tmp dir keeps each test's generated output private to that test.
    """

    def _copy_in(granule_name: str) -> str:
        src = os.path.join(fixture_path, granule_name)
        dst = os.path.join(tmp_path, granule_name)
        shutil.copy(src, dst)
        return str(tmp_path)

    return _copy_in


@pytest.fixture
def mock_process_pipeline(mocker) -> Callable[..., None]:
    """Patch the external (non-filesystem) calls made during process()."""

    def _apply(
        granule_name: str, source_dir: str, dmrpp_name: str | None = None
    ) -> None:
        dmrpp_name = dmrpp_name or f"{granule_name}.dmrpp"
        mocker.patch(
            "dmrpp_generator.main.DMRPPGenerator.upload_file_to_s3",
            return_value={"granuleId": f"s3://{dmrpp_name}"},
        )
        mocker.patch(
            "cumulus_process.Process.fetch_all",
            return_value={"input_key": [os.path.join(source_dir, granule_name)]},
        )
        mocker.patch("os.remove", return_value=granule_name)
        mocker.patch(
            "cumulus_process.s3.download",
            return_value=os.path.join(source_dir, granule_name),
        )

    return _apply
