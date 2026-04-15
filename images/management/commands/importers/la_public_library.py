import requests
from typing import ClassVar


# Info API
# https://tessa2.lapl.org/digital/bl/dmwebservices/index.php?q=dmGetItemInfo/photos/111547.jpg/json
#
# File download
# https://tessa2.lapl.org/digital/download/collection/photos/id/111547/size/large

HEADERS = {"User-Agent": "Yesterdays/1.0 (https://inlandempire.place)"}

BASE_URL = "https://tessa2.lapl.org/digital"


class ImageInfo:
    """
    Info API example
    https://tessa2.lapl.org/digital/bl/dmwebservices/index.php?q=dmGetItemInfo/photos/111547.jpg/json

    File download example
    https://tessa2.lapl.org/digital/download/collection/photos/id/111547/size/large
    """

    def __init__(self, image_id: str, image_collection: str):
        # Often ends with ".jpg"
        self.image_id: str = image_id
        # Not the real collection, but the collection field, usually "photos". Remove slashes
        self.image_collection: str = image_collection.strip("/")

    @classmethod
    def from_json(cls, image_dict: dict):
        """Creates from dictionary returned in search API call"""
        return cls(image_dict["pointer"], image_dict["collection"])

    @property
    def metadata_url(self) -> str:
        return f"{BASE_URL}/bl/dmwebservices/index.php?q=dmGetItemInfo/{self.image_collection}/{self.image_id}/json"

    @property
    def download_url(self) -> str:
        return f"{BASE_URL}/download/collection/{self.image_collection}/id/{self.image_id}/size/large"

    @property
    def ui_url(self) -> str:
        return f"{BASE_URL}/collection/{self.image_collection}/id/{self.image_id}/rec/1"

    def get_metadata(self) -> dict:
        """
        Example image metadata
        "order": "00075855",
        "title": "Opera House, Hemet",
        "creato": {},
        "studio": {},
        "collec": "Security Pacific National Bank Collection",
        "locati": "Hemet-Streets.; S-003-731 4x5",
        "date": "Circa 1911",
        "descri": "1 photographic print :b&w ;21 x 26 cm.",
        "notes": "Title supplied by cataloger.",
        "histor": "Hemet is a city in Riverside County...",
        "descra": "Early view of a major street located in Hemet..."
        "publis": {},
        "subjec": "Horse-drawn vehicles--California--Hemet...",
        "covera": {},
        "format": "Photographic prints",
        "credit": {},
        "source": {},
        "rights": {},
        "reprod": "Images available for reproduction and use...",
        "donor": {},
        "audien": "CARL0000079021",
        "carl": "http://jpg1.lapl.org/00075/00075855.jpg",
        "type": {},
        "collea": "Security Pacific National Bank Photo Collection",
        "catalo": "scanning-PC\\mmattson",
        "editmm": {},
        "fullrs": {},
        "find": "111548.jpg",
        "dmaccess": {},
        "dmimage": {},
        "dmcreated": "2018-06-10",
        "dmmodified": "2018-06-10",
        "dmoclcno": {},
        "dmrecord": "111547",
        "restrictionCode": "1",
        "cdmfilesize": "116587",
        "cdmfilesizeformatted": "0.11 MB",
        "cdmprintpdf": "0",
        "cdmhasocr": "0",
        "cdmisnewspaper": "0"
        """
        res = requests.get(self.metadata_url, headers=HEADERS)
        res.raise_for_status()
        return res.json()

    def image_metadata(self) -> dict:
        """
        Returns a dictionary of fields needed to create an Image object.
        """
        metadata = self.get_metadata()
        image_metadata = {
            "title": metadata["title"],
            # Remove non-breaking space
            "collection": metadata["collec"].replace("\xa0", " "),
            "description": metadata["descra"].replace("\'", "'"),
            "ref": str(self.image_id),
            "original_url": self.ui_url,
            "creator": metadata["creato"],
            # TODO: extract date
            "original_date": metadata["date"],
            "edtf_date": "",
        }
        return image_metadata



class LAPLSearch:
    # Only returns title. Full metadata requires another call
    search_url: ClassVar[str] = ("{base_url}/digital/bl/dmwebservices/index.php?q=dmQuery/all"
                                 "/CISOSEARCHALL^{search_term}^all^and/title/title"
                                 "/{num_results}/{page}/0/0/0/0/0/json")

    def __init__(self, search_term: str, num_results: int = 20, page: int = 1):
        self.search_term: str = search_term
        self.num_results: int = num_results
        self.page: int = page
        """
        Pagination dict example:
        "pager": {
            "start": "1"
            "maxrecs": "20",
            "total": 1340
        },
        """
        self.pagination: dict = ...
        self.page_data: dict = ...

    def search(self) -> dict:
        search_url = self.search_url.format(
            base_url=BASE_URL,
            search_term=self.search_term,
            num_results=self.num_results,
            page=self.page,
        )
        res = requests.get(search_url, headers=HEADERS)
        res.raise_for_status()
        data = res.json()
        self.pagination = data["pager"]
        self.page_data = data["records"]
        return self.page_data

    def search_next_page(self):
        self.page += 1
        return self.search()

    def get_ids_on_page(self) -> list:
        return [image["pointer"] for image in self.page_data]

    @property
    def current_page(self) -> int:
        return self.pagination["start"]

    @property
    def total_results(self) -> int:
        return self.pagination["total"]


search = LAPLSearch("riverside")

results = search.search()

for result in results:
    image = ImageInfo.from_json(result)
    metadata = image.get_metadata()
    print(metadata)

