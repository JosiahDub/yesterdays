import requests
from typing import ClassVar


# Info API
# https://tessa2.lapl.org/digital/bl/dmwebservices/index.php?q=dmGetItemInfo/photos/111547.jpg/json
#
# File download
# https://tessa2.lapl.org/digital/download/collection/photos/id/111547/size/large


class ImageInfo:
    """
    Info API example
    https://tessa2.lapl.org/digital/bl/dmwebservices/index.php?q=dmGetItemInfo/photos/111547.jpg/json

    File download example
    https://tessa2.lapl.org/digital/download/collection/photos/id/111547/size/large
    """

    base_url: ClassVar[str] = "https://tessa2.lapl.org/digital"

    def __init__(self, image_id: str, image_collection: str):
        # Often ends with ".jpg"
        self.image_id: str = image_id
        # Not the real collection, but the collection field, usually "photos"
        self.image_collection: str = image_collection

    @classmethod
    def from_json(cls, image_dict: dict):
        """Creates from dictionary returned in search API call"""
        return cls(image_dict["find"], image_dict["collection"])

    @property
    def metadata_url(self) -> str:
        return f"{self.base_url}/digital/bl/dmwebservices/index.php?q=dmGetItemInfo/{self.image_collection}/{self.image_id}/json"

    @property
    def download_url(self) -> str:
        # Remove .jpg if present
        image_id = self.image_id.split(".")[0]
        return f"{self.base_url}/digital/download/collection/{self.image_collection}/id/{image_id}/size/large"

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
    "histor": "Hemet is a city in Riverside County that was founded in 1887 and incorporated on January 20, 1910 with 992 people. Members of the Cahuilla Indian tribe first inhabited the area. During the early 1800s, it became a cattle ranch for Mission San Luis Rey, which named the area Rancho San Jacinto. In 1895, the Hemet Dam was completed on the San Jacinto River creating Lake Hemet and providing a reliable water supply to the San Jacinto Valley. Despite a severe drought in 1898-1900 and a major Christmas Day earthquake in 1899, the town of Hemet continued to prosper. Every year since 1923 one of the city's claims to fame has been \"The Ramona Pageant\", an outdoor play based on Helen Hunt Jackson's novel \"Ramona\". In 1950, Hemet was home to 10,000 people; as of January 2007, the city had a population of 70,288 according to the California Department of Finance.",
    "descra": "Early view of a major street located in Hemet. Among the several buildings pictured, three have been identified as: the Opera House, Bank of Hemet, and Real Estate building. Horse-drawn carriages are parked along either side of the wide dirt road.",
    "publis": {},
    "subjec": "Horse-drawn vehicles--California--Hemet.; Storefronts--California--Hemet.; Buildings--California--Hemet.; Roads--California--Hemet.; Hemet (Calif.).",
    "covera": {},
    "format": "Photographic prints",
    "credit": {},
    "source": {},
    "rights": {},
    "reprod": "Images available for reproduction and use. Please see the Ordering & Use page at http://tessa.lapl.org/OrderingUse.html for additional information.",
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

# Search URL
# https://tessa2.lapl.org/digital/bl/dmwebservices/index.php?q=dmQuery/all/CISOSEARCHALL^riverside^all^and/title /title/20/1/0/0/0/0/0/json
"""
Pagination dict example:
"pager": {
    "start": "1"
    "maxrecs": "20",
    "total": 1340
},
"""


