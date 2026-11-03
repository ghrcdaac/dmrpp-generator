"""Constructs DMRPP command and executes it via Docker."""

import argparse
import importlib.metadata
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from time import sleep

# The only docker compose invocation forms this tool will ever execute.
# Used for validation to meet S603.
_DOCKER_EXECUTABLE = shutil.which("docker")
_DOCKER_COMPOSE_LEGACY_EXECUTABLE = shutil.which("docker-compose")

_MIN_PORT = 1
_MAX_PORT = 65535

# Set of valid service names _run_docker_compose() will ever be
# asked to start. Used for validation to meet S603.
_VALID_DMRPP_SERVICES = frozenset({"dmrpp-generator", ""})


def _resolve_docker_compose_command() -> list[str]:
    """Resolve the docker executable needed to run`docker compose.
    :return: Argument list prefix, e.g. ["docker", "compose"] or ["docker-compose"].
    :raises FileNotFoundError: If neither docker nor docker-compose is installed.
    """
    if _DOCKER_EXECUTABLE is not None:
        return [_DOCKER_EXECUTABLE, "compose"]
    if _DOCKER_COMPOSE_LEGACY_EXECUTABLE is not None:
        return [_DOCKER_COMPOSE_LEGACY_EXECUTABLE]
    raise FileNotFoundError("Neither 'docker' nor 'docker-compose' was found on PATH.")


def check_docker_version(log_file_path: str) -> list[str]:
    """Check docker version.
    :param log_file_path: Path to log.
    :return: Correct docker compose command prefix, as an argument list.
    """
    dkr_comp_version = _resolve_docker_compose_command()
    with open(log_file_path, "a+", encoding="utf-8") as output:
        subprocess.run(  # noqa: S603 - fully-resolved, non-shell argument list
            [*dkr_comp_version, "version"],
            shell=False,
            check=False,
            stdout=output,
            stderr=output,
        )
    return dkr_comp_version


@dataclass
class DockerComposeRequest:
    """Parameters needed to start the DMRPP generator docker container."""

    payload: str
    dmrpp_args: str
    nc_hdf_path: str
    port: str | int
    dmrpp_service: str
    log_file_path: str

    def __post_init__(self) -> None:
        """Validate inputs that end up as subprocess argv/env values."""
        if self.dmrpp_service not in _VALID_DMRPP_SERVICES:
            raise ValueError(
                f"dmrpp_service must be one of {sorted(_VALID_DMRPP_SERVICES)}, "
                f"got {self.dmrpp_service!r}"
            )
        resolved_path = Path(self.nc_hdf_path).resolve(strict=True)
        if not resolved_path.is_dir():
            raise NotADirectoryError(
                f"nc_hdf_path is not a directory: {self.nc_hdf_path}"
            )
        self.nc_hdf_path = str(resolved_path)

        port_num = int(self.port)
        if not _MIN_PORT <= port_num <= _MAX_PORT:
            raise ValueError(
                f"port must be between {_MIN_PORT} and {_MAX_PORT}, got {self.port}"
            )
        self.port = port_num

        # Ensure payload is valid JSON before it is forwarded to the container.
        json.loads(self.payload)


def _run_docker_compose(request: DockerComposeRequest) -> None:
    """Start DMRPP generator docker container.
    :param request: Parameters needed to start the docker container.
    """
    docker_compose = f"{os.path.dirname(os.path.realpath(__file__))}/docker-compose.yml"
    dkr_comp_version = check_docker_version(request.log_file_path)
    if "DMRPP_VERSION" not in os.environ:
        os.environ["DMRPP_VERSION"] = importlib.metadata.version("dmrpp-generator")
    with open(request.log_file_path, "r+", encoding="utf-8") as output:
        try:
            env = os.environ.copy()
            env["PAYLOAD"] = request.payload
            env["DMRPP_ARGS"] = request.dmrpp_args
            env["NC_FILES_PATH"] = request.nc_hdf_path
            env["PORT"] = str(request.port)
            cmd = [*dkr_comp_version, "-f", docker_compose, "up", request.dmrpp_service]
            compose_ps = subprocess.run(  # noqa: S603 - argv built from validated values
                cmd,
                shell=False,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                capture_output=True,
                text=True,
                env=env,
            )

            for line in compose_ps.stdout:
                line_strip = line.strip()
                output.write(f"{line_strip}\n")
                print(line_strip)

        except KeyboardInterrupt:
            print("\nShutting down the Hyrax server. Please wait...")
            cmd = [
                *dkr_comp_version,
                "-f",
                docker_compose,
                "down",
                request.dmrpp_service,
            ]
            subprocess.run(  # noqa: S603 - argv built from validated values
                cmd, shell=False, check=False, stdout=output, stderr=output
            )


def main():
    """Construct DMRPP command and execute it."""
    print(f"dmrpp-generator {importlib.metadata.version('dmrpp-generator')}\n")
    parser = argparse.ArgumentParser(
        description="Generate and validate DMRPP files. Any DMR++ commandline option "
        "can be provided in addition to the options listed below. "
        "To see what options are available check the documentation: "
        "https://docs.opendap.org/index.php?title=DMR%2B%2B#Command_line_options"
    )
    parser.add_argument(
        "-p",
        "--path",
        dest="nc_hdf_path",
        required=True,
        help="Path to netCDF4 and HDF5 folder",
    )
    parser.add_argument(
        "-prt",
        "--port",
        dest="port",
        default="8080",
        help="Port number to Hyrax local server",
    )
    parser.add_argument(
        "-pyld",
        "--payload",
        dest="payload",
        default=os.getenv("PAYLOAD", "{}"),
        help="Payload to pass to the besd get_dmrpp call. "
        "If not set, will check for PAYLOAD environment variable, or default to '{}'"
        'The value should be a json dictionary string \'{"key": "value"}\'',
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate netCDF4 and HDF5 files against OPeNDAP local server. "
        "This is the default behavior",
    )
    parser.add_argument(
        "--no-validate",
        dest="validate",
        action="store_false",
        help="Do not validate netCDF4 and HDF5 files against OPeNDAP local server. "
        "The default behavior is --validate.",
    )
    parser.set_defaults(validate=True)

    args, unknown = parser.parse_known_args()
    unknown_str = json.dumps(unknown)
    nc_hdf_path, port, payload, validate = [getattr(args, ele) for ele in vars(args)]
    log_file_location = tempfile.mkstemp(prefix="dmrpp-generator-")[1]
    print(f"Log file: {log_file_location}")

    dmrrpp_service = "dmrpp-generator"
    if validate:
        dmrrpp_service = ""
        visit_link_path_message = (
            f"http://localhost:{port}/opendap (^C to kill the server)"
        )
        message_visit_server = f"Results served at : {visit_link_path_message}"
        print(message_visit_server)
        sleep(2)

    _run_docker_compose(
        DockerComposeRequest(
            payload=payload,
            dmrpp_args=unknown_str,
            nc_hdf_path=nc_hdf_path,
            port=port,
            dmrpp_service=dmrrpp_service,
            log_file_path=log_file_location,
        )
    )


if __name__ == "__main__":
    main()
