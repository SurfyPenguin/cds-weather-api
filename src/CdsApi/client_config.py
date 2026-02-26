import cdsapi
from .exceptions import ClientError
import os
from typing import Any, overload

API_CREDS_FILE = ".cdsapirc"
HOME_DIR = os.path.expanduser("~")

class ClientConfig:

    @staticmethod
    def check_api_credentials(**kwargs):
        kwargs_missing = not kwargs.get("key") or not kwargs.get("url")
        file_missing = not os.path.isfile(os.path.join(HOME_DIR, API_CREDS_FILE))

        if kwargs_missing and file_missing:
            raise ClientError(f"Please provide api credentials in client config.\n\tor\ncreate an {API_CREDS_FILE} in 'home' directory.")

    @overload
    @staticmethod
    def config(
        *,
        url: str | None = None,
        key: str | None = None,
        quiet: bool = False,
        debug: bool = False,
        verify: bool = True,
        timeout: float | tuple[float, float] = 60,
        progress: bool = True,
        full_stack: bool = False,
        delete: bool = False,
        retry_max: int = 500,
        sleep_max: int = 120,
        wait_until_complete: bool = True,
        **extra: Any,
    ) -> cdsapi.Client:
        
        ...

    @classmethod
    def config(cls, **kwargs: Any) -> cdsapi.Client:
        """Create or replace the default `cdsapi.Client`.

        Reference: https://ecmwf.github.io/ecmwf-datastores-client/_api/datastores/Client.html.

        Args:
            url (str | None, optional): API URL. If None, infer from ECMWF_DATASTORES_URL or ECMWF_DATASTORES_RC_FILE. Defaults to None.
            key (str | None, optional): API Key. If None, infer from ECMWF_DATASTORES_KEY or ECMWF_DATASTORES_RC_FILE. Defaults to None.
            quiet (bool, optional): Avoid getting update announcements in terminal. Defaults to False.
            debug (bool, optional): Defaults to False.
            verify (bool, optional): Whether to verify the TLS certificate at the remote end. Defaults to True.
            timeout (float | tuple[float, float], optional): How many seconds to wait for the server to send data, as a float, or a (connect, read) tuple. Defaults to 60.
            progress (bool, optional): Whether to display the progress bar during download. Defaults to True.
            full_stack (bool, optional): Defaults to False.
            delete (bool, optional): Delete download requests after completion. Defaults to False.
            retry_max (int, optional): Defaults to 500.
            sleep_max (int, optional): Defaults to 120.
            wait_until_complete (bool, optional): Allows to submit requests asynchronously without pausing the script to wait for completion. Defaults to True.

        Returns:
            cdsapi.Client: Cdsapi client with provided config.
        """
        cls.check_api_credentials(**kwargs)
        return cdsapi.Client(**kwargs)