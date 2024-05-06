import inspect
import requests
from retrying import retry
from helpers.log import Log


class Connector:
    """
    Simple connector that makes requests with retries
    """

    def __init__(self) -> None:
        self.allowed_request_args = inspect.getfullargspec(requests.Request).args
        self.log = Log().get_logger()
        self.retry_max = 9
        self.retry_wait_min = (1000,)
        self.retry_wait_max = (16000,)
        self.retry_codes = [500, 501, 502, 503, 504]
        self.retry_init_config()

    def retry_init_config(self) -> None:
        self.retry_cfg = {
            "stop_max_attempt_number": self.retry_max,
            "wait_exponential_multiplier": self.retry_wait_min,
            "wait_exponential_max": self.retry_wait_max,
            "retry_on_result": self.retry_code,
        }
        return

    def build_request_params(self, req_params:dict) -> None:
        unknown_args = [key not in self.allowed_request_args for key in req_params.keys()]
        if unknown_args:
            if len(unknown_args) == 1:
                KeyError(f"The arg '{unknown_args}' is not valid for the requests.Request method")
            else:
                unk_args_str = "', '".join(unknown_args)
                KeyError(f"The arg(s) '{unk_args_str}' are not valid for the requests.Request method")
        else: 
            self.request_cfg = req_params

    def retry_code(self, result) -> bool:
        return result in self.retry_codes

    def make_request(self, req_params:dict) -> requests.Request:
        self.build_request_params(req_params)
        retry_cfg = self.retry_cfg
        retry_cfg["retry_on_result"] = self.retry_code

        @retry(**self.retry_cfg)
        def _make_request() -> requests.Request:
            res = requests.request(**self.request_cfg)
            if res.status_code == 200:
                self.log.debug(f"Successful request (response code 200)")
                return res
            else:
                status_code = res.status_code
                self.log.error(f"Unsuccessful request, status code: {status_code}")
                return status_code

        return _make_request()

    def get_url(self, url: str) -> requests.Request:
        return self.make_request({'url': url, 'method': "GET"})
