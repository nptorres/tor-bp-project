import os
from datetime import datetime


class Filepath:
    def __init__(self) -> None:
        self.path_data_out = "data-out"
        self.path_data_in = "data-in"

    def make_filename(self, base: str, filetype: str) -> str:
        today = datetime.today().strftime("%Y%m%d-%H%M")
        return f"{base}-{today}.{filetype}"

    def make_filepath_today(self, base: str, filetype: str) -> str:
        filepath = os.path.join(
            self.path_data_out, filetype, self.make_filename(base, filetype)
        )
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        return filepath
