from connector import Connector
from log import Log


class Ckan:
    """CKAN API connector
    This class offers a few methods to export data as CSVs and to run PostgreSQL
    queries against data hosted by the City of Toronto Open Data CKAN portal.
    """

    def __init__(self) -> None:
        self.con = Connector()
        self.log = Log()
        self.url_base = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
        self.url_api = {
            "info": "/api/3/action/package_show",
            "csv": "/datastore/dump/",
            "query": "/api/3/action/datastore_search",
            "static": "/api/3/action/resource_show?id=",
        }
        return

    def set_package_id(self, package_id: str) -> None:
        self.params = {"id": package_id}
        return

    def get_pkg_info(self) -> None:
        req_params = {
            "method": "GET",
            "url": self.url_base + self.url_api["info"],
            "params": self.params,
        }
        try:
            res = self.con.make_request(req_params=req_params)
            self.pkg_info = res.json()
        except Exception as e:
            self.log.debug(f"CKAN script didn't work: {e}")
        return

    def find_resource_endpoints(self) -> None:
        self.endpoint_params = {
            "export": [],
            "query": None,
        }
        for resource in self.pkg_info["result"]["resources"]:
            if resource["datastore_active"]:
                self.endpoint_params["export"].append(
                    {
                        "method": "GET",
                        "url": self.url_base + self.url_api["csv"] + resource["id"],
                    }
                )
                self.endpoint_params["query"] = {
                    "method": "GET",
                    "url": self.url_base + self.url_api["query"],
                    "params": {
                        "resource_id": resource["id"],
                        "plain": False,  # Setting the plain flag to false enables the entire PostgreSQL full text search query language
                    },
                }
            if not resource["datastore_active"]:
                if resource["format"].lower() == "csv":
                    self.endpoint_params["export"].append(
                        {"method": "GET", "url": resource["url"]}
                    )
        return

    def export_csv(self, path) -> str:
        try:
            res = self.con.make_request(req_params=self.endpoint_params["export"][0])
            with open(path, "w") as f:
                f.write(res.text)
        except Exception as e:
            self.log.debug(f"CKAN script couldn't write csv: {e}")
        return
