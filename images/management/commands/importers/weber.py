import os
from pathlib import Path
from images.models import Collection, Image
from images.tasks import generate_iiif_tiles
from images.utils import R2Uploader

TITLES = [
    ['La Casa Contenta, Eighth Street, Riverside, California', 1951],
    ['Canyon Crest, Riverside, California', 1951],
    ['McKinley Avenue and Weber House grove, Riverside, California', 1933],
    ['McKinley Avenue and Weber House grove, Riverside, California', 1933],
    ['Eighth Street and Weber grove, Riverside, California', 1935],
    ['Formwork tower and Chevrolet AK truck, St Francis de Sales Auditorium construction, Riverside, California', 1943],
    ['St Francis de Sales Auditorium construction, Riverside, California', 1943],
    ['St Francis de Sales Auditorium construction, Riverside, California', 1943],
    ['Palm Springs High School, Palm Springs, California', 1938],
    ['Lugonia Kindergarten, Redlands', 1937],
    ['Weber House driveway entrance and arbor with 1929 Plymouth Coupe', 1937],
    ['Fremont School, Riverside', 1937],
    ['Grant School, Riverside', 1937],
    ['Grant School, 14th & Brockton, Riverside, California', 1935],
    ['Grant School, 14th & Brockton, Riverside, California', 1937],
    ['Fairmount Park, Riverside, California', 1939],
    ['San Bernardino Valley College Auditorium, San Bernardino', 1938],
    ['San Bernardino Valley College Auditorium, San Bernardino', 1938],
    ['East Wing, Riverside General Hospital, Riverside', 1938],
    ['East Wing, Riverside General Hospital, Riverside', 1938],
    ['Powerhouse and Laundry addition with Tuberculosis Building in background, Riverside General Hospital, Riverside', 1938],
    ['Powerhouse and Laundry addition, Riverside General Hospital, Riverside', 1938],
    ['East Wing, Riverside General Hospital, Riverside', 1938],
    [' Jefferson Elementary School Library, Corona', 1938],
    ['Jefferson Elementary School Library Wing, Corona', 1938],
    ['Corona Junior High School, Corona', 1938],
    ['Corona Junior High School, Corona', 1938],
    ['City Hall, Brawley, California', 1939],
    ['Southern Sierras Power Company Office, Brawley, California', 1939],
    ['St Francis de Sales Convent and Chapel, Riverside, California', 1940],
    ['1984 Bonnie Brae Street, Riverside, California', 1940],
    ['Blaine Street Federal Housing, Riverside, California', 1943],
    ['Blaine Street Federal Housing, Riverside, California', 1943],
    ['Blaine Street Federal Housing, Riverside, California', 1943],
    ['Riverside Engine Company #4, Riverside', 1938],
    ['Riverside Engine Company #4, Riverside', 1938],
    ['Peter N. Weber and dog on McKinley Street at edge of Weber grove, Riverside, California', 1952],
    ['First Presbyterian Church, Anaheim, California', 1950],
    ['Ridge Cottage Triplex (architect Lloyd Wright), Institute of Mentalphysics, Joshua Tree, Cailfornia', 1956],
    ['Spanish Patio, Mission Inn, Riverside, California', 1928],
    ['Anton Clock and Carrie Jacobs Bond Suite, Mission Inn, Riverside, California', 1928],
    ['Las Salas de los Escritorios (Authors’ Row) from the Court of the Bells, Mission Inn, Riverside, California', 1928],
    ['Alhambra Suite and Carmel Dome, Mission Inn, California', 1928],
    ['Alhambra Suite and Carmel Dome, Mission Inn, Riverside, California', 1928],
    ['Spanish Patio, Riverside, California', 1928],
    ['Old Adobe, Campanario, and Carillon Tower, Mission Inn, Riverside, California ', 1928],
    ['Spanish Wing and Frank Miller Suite, Mission Inn, Riverside, California', 1928],
    ['Carrie Jacobs Bond Suite, Las Salas de los Escritorios (Authors’ Row), Mission Inn, California ', 1928],
    ['Spanish Patio, Mission Inn, Riverside, California', 1928],
    ['East courtyard, Soldiers’ Memorial and Municipal Auditorium Building, Riverside, California', 1928],
    ['East steps of Soldiers’ Memorial and Municipal Auditorium Building, Riverside, California', 1928],
    ['Court of the Bells and Cloister Wing, Mission Inn, California', 1928],
    ['Carillon Tower and Spanish Courtyard, Mission Inn, Riverside, California ', 1928],
    ['Las Salas de Los Escritorios (Authors’ Row), Mission Inn, Riverside, California ', 1928],
    ['Cloister Wing, Mission Inn, Riverside CA', 1928],
]

def add_arguments(parser):
    pass

def handle(options):
    current_dir = Path(__file__).parent.resolve()
    image_dir = Path(current_dir).joinpath("images")

    collection = Collection.objects.get(
        name="Peter J. Weber Collection",
    )
    r2_uploader = R2Uploader()

    for index, file_name in enumerate(sorted(os.listdir(image_dir), key=lambda x: int(x.split("-")[0]))):

        title, year = TITLES[index]
        year = str(year)
        print(f"Processing {index}: {file_name}")
        full_path = os.path.join(image_dir, file_name)

        try:
            # Create the record first to get an ID
            img_obj = Image.objects.create(
                collection=collection,
                title=title,
                description="",
                creator="Peter J. Weber",
                ref=f"pjw-{index}",  # Unique ref based on index
                original_date=year,
                edtf_date=year,
                license=options["license"],
            )

            # Extract file to memory and upload
            with open(full_path, "rb") as f:
                file_data = f.read()
                r2_url = r2_uploader.upload_file_content(
                    file_data,
                    r2_uploader.generate_key_from_url(img_obj.ref),
                    overwrite=True,
                )

            if r2_url:
                Image.objects.filter(pk=img_obj.id).update(permalink=r2_url)
                generate_iiif_tiles.delay(img_obj.id)
                print(f"Uploaded {file_name}")
            else:
                print("Upload failed?")

        except Exception as e:
            print(f"Failed {file_name}: {e}")
            raise
full_description = {
    "base": "https://photos.adobe.io/v2/spaces/88b5889703184af48fdc7bdaadcd2063/",
    "album": {
        "id": "e5e6ad020f7f4c34963ceebb91d95d12",
        "links": {
            "self": {
                "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12"
            }
        }
    },
    "resources": [
        {
            "id": "6188b831de104f59a885c22305424fd6",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "89bb8ecc4c3e406095524274cec6b513"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/dd401ef9284445f692d9b359e5fce50c"
                }
            },
            "asset": {
                "id": "dd401ef9284445f692d9b359e5fce50c",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:03.528331Z",
                "updated": "2026-04-23T02:46:49.622798Z",
                "links": {
                    "self": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c"
                    },
                    "/rels/comments": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/309e44b8672c4ce5a98bbcdd39c5d445/renditions/03ac52c8e70414cee5635df3aa6bdd97"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/309e44b8672c4ce5a98bbcdd39c5d445/renditions/be07538745571f30b2dea7602f637956"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/309e44b8672c4ce5a98bbcdd39c5d445/renditions/862a8c6b798dc3b72e0addc746f0da05"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/309e44b8672c4ce5a98bbcdd39c5d445/renditions/686e437d262ab41d51cd0b0d49ca3f24"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/82869073af9357f967608a7613a7f6ee/renditions/cf29424a8f8347348c4c3e6969d50a5a"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/dd401ef9284445f692d9b359e5fce50c/revisions/82869073af9357f967608a7613a7f6ee/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1357,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "45e34fcc14c607745e76a6034b4efad6b6c3950804ab69464cb76d1f01cf7073"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:54.450Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2023-10-22T16:47:36.007-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "xmp": {
                            "CreateDate": "2005-12-30T19:24:28-08:00",
                            "ModifyDate": "2025-06-01T15:17:39-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1951-042",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "La Casa Contenta, Eighth Street, Riverside, California"
                        }
                    },
                    "captureDate": "2023-10-22T16:47:36.007-08:00",
                    "importSource": {
                        "originalHeight": 1357,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1951-042.jpg",
                        "fileSize": 505588,
                        "originalWidth": 2000,
                        "sha256": "f1a405487603808eed0e6bd3603fe854500cff8845875a3f774378ec2ff4bfcf",
                        "originalDigest": "29CEFF6173BC2529C83F5281A2CB8DB3",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:54.450Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 35,
                        "created": "2025-06-01T22:21:49Z",
                        "dof": 11,
                        "emphasis": 0,
                        "harmony": 42,
                        "lighting": 26,
                        "repetition": 8,
                        "rot": 7,
                        "score": 75,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": 19
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "d4d213b3210b4603a34fc1209a7c2e66",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "d98f03eb74f148d38c5494d72a0fca16"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/5ed5fabc01c8468583c98d83d933e454"
                }
            },
            "asset": {
                "id": "5ed5fabc01c8468583c98d83d933e454",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:03.549100Z",
                "updated": "2026-04-23T02:52:44.495423Z",
                "links": {
                    "self": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454"
                    },
                    "/rels/comments": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/7389ab5806cb4b759e902cb22f4e8460/renditions/4233371328d932a468162e4b0e033893"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/7389ab5806cb4b759e902cb22f4e8460/renditions/93ec462d451860e88dbeed796a9aedd7"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/7389ab5806cb4b759e902cb22f4e8460/renditions/fd3297b1a361bf593c0b8e86201a59fa"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/7389ab5806cb4b759e902cb22f4e8460/renditions/32232c762fbe34064c10e7207b8561b4"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/3202b4d833ac38219c852536ab5ef36e/renditions/9f00fe64670c4eec8dc443e413c59d56"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/5ed5fabc01c8468583c98d83d933e454/revisions/3202b4d833ac38219c852536ab5ef36e/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1289,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "90793993cdc7c498fadc67d1642c2ab4d9174c3084905d23acce271b458ba6f2"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:54.474Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2023-10-22T16:47:36.007-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "xmp": {
                            "CreateDate": "2003-05-01T16:07:53-07:00",
                            "ModifyDate": "2025-06-01T15:17:38-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1951-041",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Canyon Crest, Riverside, California"
                        }
                    },
                    "captureDate": "2023-10-22T16:47:36.007-08:00",
                    "importSource": {
                        "originalHeight": 1289,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1951-041.jpg",
                        "fileSize": 952428,
                        "originalWidth": 2000,
                        "sha256": "1a9a4c32bc150a2915f57dcf4ba3505f5bf8e20bafdddf0bc1f922e0b2e35e1d",
                        "originalDigest": "F9229CF5CB09CB1DF4675F62A23DC9E9",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:54.474Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 15,
                        "content": 64,
                        "created": "2025-06-01T22:21:25Z",
                        "dof": 5,
                        "emphasis": -3,
                        "harmony": 67,
                        "lighting": 44,
                        "repetition": 9,
                        "rot": 15,
                        "score": 85,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": 25
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "b5334adf69264721acb095910358a687",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "5b0736fad214498890bb463241bfee27"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/778a33ea4d6d43a095b19a6cca8b404b"
                }
            },
            "asset": {
                "id": "778a33ea4d6d43a095b19a6cca8b404b",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.258120Z",
                "updated": "2026-04-23T02:52:44.379912Z",
                "links": {
                    "self": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b"
                    },
                    "/rels/comments": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/8df3760795464b70a7ce5e7070d31679/renditions/3bc9763516266f91017d671ddeea43c9"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/8df3760795464b70a7ce5e7070d31679/renditions/32e208c45f019044d0b4ef65bbb6d6aa"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/8df3760795464b70a7ce5e7070d31679/renditions/ffb2613ceac56dbafc9c3298eba879ec"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/8df3760795464b70a7ce5e7070d31679/renditions/af6831a56d15476d243b9758590b9c37"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/3206a8349442923d1df8d924f9185322/renditions/d370796e850c40daaf398ecaaf455e74"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/778a33ea4d6d43a095b19a6cca8b404b/revisions/3206a8349442923d1df8d924f9185322/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1356,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.426Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-02T00:51:36.096-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1933-007",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "McKinley Avenue and Weber House grove, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-02T00:51:36.96-08:00",
                            "ModifyDate": "2025-06-01T14:23:17-07:00"
                        }
                    },
                    "captureDate": "2024-03-02T00:51:36.96-08:00",
                    "importSource": {
                        "originalHeight": 1356,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1933-007.jpg",
                        "fileSize": 478827,
                        "originalWidth": 2000,
                        "sha256": "56851c948bd3c5935e4b5275341a77be21edb301a92423d26b262c861c3c549c",
                        "originalDigest": "A36077186E4CE2251876BE858C015093",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.426Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -3,
                        "created": "2025-06-01T22:22:57Z",
                        "dof": 0,
                        "emphasis": -18,
                        "harmony": 6,
                        "lighting": -29,
                        "repetition": 5,
                        "rot": 0,
                        "score": 62,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -50
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "784f6fc4ffa1489e88b9395fe4eca36c",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "f7c09cfa8bf54f749084bc06927b7bbf"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/f924c7e8f0c7407bad20c80105c7b3c1"
                }
            },
            "asset": {
                "id": "f924c7e8f0c7407bad20c80105c7b3c1",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.606927Z",
                "updated": "2026-04-23T02:52:44.668601Z",
                "links": {
                    "self": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1"
                    },
                    "/rels/comments": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/f0d8a6c4ef1a4bd8a56e6d5164b6c244/renditions/e7660b867618545c3cc69bd61e999901"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/f0d8a6c4ef1a4bd8a56e6d5164b6c244/renditions/ee41e727142e345e7548df5ac445481f"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/f0d8a6c4ef1a4bd8a56e6d5164b6c244/renditions/c4169d72d13dba93fd0174275cb2e51d"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/f0d8a6c4ef1a4bd8a56e6d5164b6c244/renditions/3a1c49e0e0e3fe308395954eee4a8e4c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/67a93be7329ebf9444ba7582fb50e4f4/renditions/2ebf5ebf82c64b12a1254cbb04ba5019"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/f924c7e8f0c7407bad20c80105c7b3c1/revisions/67a93be7329ebf9444ba7582fb50e4f4/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1354,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:56.713Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-02T00:52:29.002-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1933-009",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "McKinley Avenue and Weber House grove, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-02T00:52:29.02-08:00",
                            "ModifyDate": "2025-06-01T14:23:20-07:00"
                        }
                    },
                    "captureDate": "2024-03-02T00:52:29.02-08:00",
                    "importSource": {
                        "originalHeight": 1354,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1933-009.jpg",
                        "fileSize": 478119,
                        "originalWidth": 2000,
                        "sha256": "afa153cfe5ea679b2a31eaad60ebc940982735a3a22b551a9e25112bca48bbaf",
                        "originalDigest": "501919C74738547D7E42791572A69587",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:56.713Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": 4,
                        "created": "2025-06-01T22:22:58Z",
                        "dof": -3,
                        "emphasis": -11,
                        "harmony": 3,
                        "lighting": -27,
                        "repetition": 5,
                        "rot": 0,
                        "score": 62,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "d340c355e8fa42528b3428ad70b2368a",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "3df389ceec704413b6d869bf6ce52c38"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/9f2806e27e6d41cfb0b453024613db49"
                }
            },
            "asset": {
                "id": "9f2806e27e6d41cfb0b453024613db49",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.062989Z",
                "updated": "2026-04-23T02:52:44.780533Z",
                "links": {
                    "self": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49"
                    },
                    "/rels/comments": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/ca867574f1aa4aeeb944d7dcbffb8996/renditions/d1e9fb2df0b4ffee84d82968fc64e620"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/ca867574f1aa4aeeb944d7dcbffb8996/renditions/0445dcafdd1497d8b5127f39c9257b41"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/ca867574f1aa4aeeb944d7dcbffb8996/renditions/d6357300efef2f2cc2404cb1045134e5"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/ca867574f1aa4aeeb944d7dcbffb8996/renditions/8b2e67c6f7eac6394a3e04ee6c1f13cf"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/b89a7108a9391fa0d84072a364af1a45/renditions/2e609de775954e7ea157c5afd4504892"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/9f2806e27e6d41cfb0b453024613db49/revisions/b89a7108a9391fa0d84072a364af1a45/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1799,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.291Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-02T16:14:16.058-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1935-013",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Eighth Street and Weber grove, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-02T16:14:16.58-08:00",
                            "ModifyDate": "2025-06-01T14:23:43-07:00"
                        }
                    },
                    "captureDate": "2024-03-02T16:14:16.58-08:00",
                    "importSource": {
                        "originalHeight": 1799,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1935-013.jpg",
                        "fileSize": 702956,
                        "originalWidth": 2000,
                        "sha256": "5038f07a8586353c4082707ff695abf190c938bd3717eb1c4ad4bb167d20bb3d",
                        "originalDigest": "B13D702654F6EE6732B66629DE4426F4",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.291Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -21,
                        "created": "2025-06-01T22:23:19Z",
                        "dof": -7,
                        "emphasis": -43,
                        "harmony": 8,
                        "lighting": -23,
                        "repetition": 7,
                        "rot": 0,
                        "score": 60,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -45
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "aaf58a7ef9d8496583eed9760afeb948",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "c5549ed4372346d18a68ac7c749c86c5"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/7335e8f7b41149b3b9d4468877d9067f"
                }
            },
            "asset": {
                "id": "7335e8f7b41149b3b9d4468877d9067f",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.723826Z",
                "updated": "2026-04-23T02:52:45.432796Z",
                "links": {
                    "self": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f"
                    },
                    "/rels/comments": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/6f65a7ba87d741fa8b6ca4c092d74c78/renditions/736122ad818179648ab1b63e3bd6f66c"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/6f65a7ba87d741fa8b6ca4c092d74c78/renditions/23c7beb44cda75972b9c9e5d1abe46e8"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/6f65a7ba87d741fa8b6ca4c092d74c78/renditions/047c5cc0a76ab425c5c5643d8edd77e4"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/6f65a7ba87d741fa8b6ca4c092d74c78/renditions/4b2d4121bd03e1e8b281a4603355d8da"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/9a3c28ce6a204e76aa518acba3f7eb6b/renditions/3efa1a9a61c6423b800a2a13b27f23ab"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/7335e8f7b41149b3b9d4468877d9067f/revisions/9a3c28ce6a204e76aa518acba3f7eb6b/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1351,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2026-04-19T23:04:56.074Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-04T19:28:27.061-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-014",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Formwork tower and Chevrolet AK truck, St Francis de Sales Auditorium construction, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-04T19:28:27.61-08:00",
                            "ModifyDate": "2025-06-01T15:13:41-07:00"
                        }
                    },
                    "captureDate": "2024-03-04T19:28:27.61-08:00",
                    "importSource": {
                        "originalHeight": 1351,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-014.jpg",
                        "fileSize": 393809,
                        "originalWidth": 2000,
                        "sha256": "26532a2564ed6cf749a6d335e116dc1e3424b5083b4be4949bc47e367eba9bcc",
                        "originalDigest": "0D1FC8A7C9ED47CF71386489A4A171B4",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:57.936Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 1,
                        "content": -12,
                        "created": "2025-06-01T22:24:47Z",
                        "dof": -6,
                        "emphasis": -21,
                        "harmony": -2,
                        "lighting": -43,
                        "repetition": 5,
                        "rot": -1,
                        "score": 52,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -60
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "c16d1fbaa16843bd929fd517e78dfb97",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "82482bb6bd9a4bdd97c84aa98365113a"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/9171a87e773540e79d10c3cad14f955e"
                }
            },
            "asset": {
                "id": "9171a87e773540e79d10c3cad14f955e",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.935167Z",
                "updated": "2026-04-23T02:52:45.497180Z",
                "links": {
                    "self": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e"
                    },
                    "/rels/comments": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/48380a2b17bd41ecb1cf7fb7a2c709b3/renditions/2a88f394fcd0e937af34dc12d360ff57"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/48380a2b17bd41ecb1cf7fb7a2c709b3/renditions/de82c3c942af7a7af6abcbee064f8c23"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/48380a2b17bd41ecb1cf7fb7a2c709b3/renditions/516472bd29af1c69ed1c0d4507de875b"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/48380a2b17bd41ecb1cf7fb7a2c709b3/renditions/ff4dc56bb7980a9ecbe91452b30d550c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/ea5891652bbb40a0817939d519247abb/renditions/c0e591b2388343a5ab33cfdb10cd329e"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/9171a87e773540e79d10c3cad14f955e/revisions/ea5891652bbb40a0817939d519247abb/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1336,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2026-04-19T23:04:23.123Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T12:48:03.039-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-049",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "St Francis de Sales Auditorium construction, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T12:48:03.39-08:00",
                            "ModifyDate": "2025-06-01T15:14:18-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T12:48:03.39-08:00",
                    "importSource": {
                        "originalHeight": 1336,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-049.jpg",
                        "fileSize": 328811,
                        "originalWidth": 2000,
                        "sha256": "30809bee44cb9ffdeef5792999a155f583b16cd201fbdb317d54c6340a817f51",
                        "originalDigest": "F41EDC0ECF186A072B923049BB7D7E68",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:57.698Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -4,
                        "content": -55,
                        "created": "2025-06-01T22:25:31Z",
                        "dof": -16,
                        "emphasis": -59,
                        "harmony": -13,
                        "lighting": -63,
                        "repetition": 4,
                        "rot": -7,
                        "score": 48,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -69
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "a51bfb1d4b2c40198d7972f1ad927eba",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "1ef101bb104e40c6a2ff40a9f24f9bfa"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/ac1cde1d72c84e7c8badb89fae26493b"
                }
            },
            "asset": {
                "id": "ac1cde1d72c84e7c8badb89fae26493b",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.412520Z",
                "updated": "2026-04-23T02:52:46.211845Z",
                "links": {
                    "self": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b"
                    },
                    "/rels/comments": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/4ade36ed201e43efb780d0abafb90122/renditions/a1525a957b1a113963e45e3d011af79f"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/4ade36ed201e43efb780d0abafb90122/renditions/ada0ccf07107e04b6384701aae1484f8"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/4ade36ed201e43efb780d0abafb90122/renditions/7d763e4e024fb39564b0382b6b5a152e"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/4ade36ed201e43efb780d0abafb90122/renditions/1db636e70c1e2dbcf13eb66d0cd3d3b8"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/35625ce0b8464cde93187ac4c06b69ba/renditions/4ce876d8821246259cb277f9356078a1"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/ac1cde1d72c84e7c8badb89fae26493b/revisions/35625ce0b8464cde93187ac4c06b69ba/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1328,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2026-04-19T23:03:55.087Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T12:50:55.017-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-052",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "St Francis de Sales Auditorium construction, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T12:50:55.17-08:00",
                            "ModifyDate": "2025-06-01T15:14:21-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T12:50:55.17-08:00",
                    "importSource": {
                        "originalHeight": 1328,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-052.jpg",
                        "fileSize": 497947,
                        "originalWidth": 2000,
                        "sha256": "f806c5e895bb442040256e223d2f54f5c1fc88b5001fb0f4c2f7638effa5b855",
                        "originalDigest": "7F3EB55F207139C3B0EDA36825BF9D35",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:55.609Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -32,
                        "created": "2025-06-01T22:25:31Z",
                        "dof": -5,
                        "emphasis": -56,
                        "harmony": 9,
                        "lighting": -24,
                        "repetition": 5,
                        "rot": 0,
                        "score": 60,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -48
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "bde5f48941564c4d89c377731fffb712",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "637a900a97f54de98163270424fee15f"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/43a99f6c8da1484bb73609322cd23bc6"
                }
            },
            "asset": {
                "id": "43a99f6c8da1484bb73609322cd23bc6",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.441703Z",
                "updated": "2026-04-23T02:52:46.461150Z",
                "links": {
                    "self": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6"
                    },
                    "/rels/comments": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4d13dbf951374ff28bd68f18245bc003/renditions/f24151a044195b7b25e6a1bdcee35866"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4d13dbf951374ff28bd68f18245bc003/renditions/8f8f1b014eece123c36070b8f29d79ed"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4d13dbf951374ff28bd68f18245bc003/renditions/6c67c5e01f524e688d8628b9fb23a2c5"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4d13dbf951374ff28bd68f18245bc003/renditions/e58136517ab8df8b7b1c9e6093df909b"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4dd3cd074b0d87bbacb3fc98ac0edbb2/renditions/f1a2e935f39f49408978798036e7ea86"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/43a99f6c8da1484bb73609322cd23bc6/revisions/4dd3cd074b0d87bbacb3fc98ac0edbb2/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1337,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:01.242Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T13:20:56.017-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-133",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Palm Springs High School, Palm Springs, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T13:20:56.17-08:00",
                            "ModifyDate": "2025-06-01T14:30:54-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T13:20:56.17-08:00",
                    "importSource": {
                        "originalHeight": 1337,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-133.jpg",
                        "fileSize": 480409,
                        "originalWidth": 2000,
                        "sha256": "cd412a364851f1718ef2b32fb4b2ab35776d9959af268e58048888eb95b63c51",
                        "originalDigest": "9C2F774F8182EF26B9574C3AD2F2338A",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:01.242Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 9,
                        "content": 47,
                        "created": "2025-06-01T22:26:06Z",
                        "dof": 2,
                        "emphasis": 17,
                        "harmony": 24,
                        "lighting": 8,
                        "repetition": 11,
                        "rot": 5,
                        "score": 68,
                        "symmetry": 5,
                        "version": 1,
                        "vivid": -33
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "e563ee10f35e4abab7b4023cf0ad8cbc",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "7b2781f791674190a2dbc30cd39b1644"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/7bcf93af609c421385b21e2e1033176b"
                }
            },
            "asset": {
                "id": "7bcf93af609c421385b21e2e1033176b",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.627176Z",
                "updated": "2026-04-23T02:52:46.638872Z",
                "links": {
                    "self": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b"
                    },
                    "/rels/comments": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/8a7d86eb5f4b46c992ad0fb01418024f/renditions/5a626550a637570ab5fa176483d6dc21"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/8a7d86eb5f4b46c992ad0fb01418024f/renditions/2199853fcf90f7dfd1f78bdf45978a13"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/8a7d86eb5f4b46c992ad0fb01418024f/renditions/f358669003c522eee1f5c46e27b7dac7"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/8a7d86eb5f4b46c992ad0fb01418024f/renditions/aaa7d55b966a2fe4bbbd67d2ff0531f8"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/6d668d06368c09f5816df112234990d7/renditions/31992595f27c43edb94573ec035fe0dd"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/7bcf93af609c421385b21e2e1033176b/revisions/6d668d06368c09f5816df112234990d7/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1349,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.208Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:12:34.004-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1937-004",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Lugonia Kindergarten, Redlands"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:12:34.40-08:00",
                            "ModifyDate": "2025-06-01T14:27:33-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:12:34.40-08:00",
                    "importSource": {
                        "originalHeight": 1349,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1937-004.jpg",
                        "fileSize": 420283,
                        "originalWidth": 2000,
                        "sha256": "b99ba122ca97cf9ec0302ab15a61be22e555a71dbaa5ff075d053ebb712aea61",
                        "originalDigest": "C10DDACC42F4302C5FA3F88E09749241",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.208Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 4,
                        "content": -7,
                        "created": "2025-06-01T22:29:00Z",
                        "dof": 7,
                        "emphasis": 2,
                        "harmony": 11,
                        "lighting": -20,
                        "repetition": 5,
                        "rot": 2,
                        "score": 66,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -47
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "60564479176748b38b13913b46c027d5",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "18ec7079db63494bab022a73a1e140c6"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/c50e23563cfd454f81eef910e069cf9d"
                }
            },
            "asset": {
                "id": "c50e23563cfd454f81eef910e069cf9d",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.632239Z",
                "updated": "2026-04-23T02:52:46.573688Z",
                "links": {
                    "self": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d"
                    },
                    "/rels/comments": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/c60d1e2ee5644aed9376cdf2e8ae2b5e/renditions/d7235a626e0c5afe0d6fa45c4d9320ef"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/c60d1e2ee5644aed9376cdf2e8ae2b5e/renditions/c8f6da884b45aac48a93877fa8307fe8"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/c60d1e2ee5644aed9376cdf2e8ae2b5e/renditions/ec372a11dca19b196d09fbd4f4619a69"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/c60d1e2ee5644aed9376cdf2e8ae2b5e/renditions/8e83be2b192df1e8dcc25144ef695511"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/0243e8d19f184532ab536bf76b2f0f23/renditions/38213e4de4f248c0a4344f18f7c4644e"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/c50e23563cfd454f81eef910e069cf9d/revisions/0243e8d19f184532ab536bf76b2f0f23/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1330,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2026-03-07T16:34:47.592Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:12:57.085-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1937-001",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Weber House driveway entrance and arbor with 1929 Plymouth Coupe"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:12:57.85-08:00",
                            "ModifyDate": "2025-06-01T14:27:29-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:12:57.85-08:00",
                    "importSource": {
                        "originalHeight": 1330,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1937-001.jpg",
                        "fileSize": 459340,
                        "originalWidth": 2000,
                        "sha256": "7fe3b033b551ed3ab3dbaccf6953530b502c508d9199c68e29eac77dceda0d88",
                        "originalDigest": "5FB0563212829E99676ABC758698AA1C",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.225Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -2,
                        "content": -49,
                        "created": "2025-06-01T22:29:05Z",
                        "dof": -9,
                        "emphasis": -49,
                        "harmony": -7,
                        "lighting": -53,
                        "repetition": 4,
                        "rot": -4,
                        "score": 56,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -68
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "a7beb7f1806a4cc6bd87ec3e636e9a38",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "0138005787cc4c3db5365293c3bbbae1"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/024f91bc58c1486988878c406ff5e85f"
                }
            },
            "asset": {
                "id": "024f91bc58c1486988878c406ff5e85f",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.490666Z",
                "updated": "2026-04-23T02:52:46.635596Z",
                "links": {
                    "self": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f"
                    },
                    "/rels/comments": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/d63ac6c2a5c4418680c8b484e2831256/renditions/910adf6a935901eb54fcb5249f25fe66"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/d63ac6c2a5c4418680c8b484e2831256/renditions/1dbfd06a46d9d1b087bb52d4dd43eedc"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/d63ac6c2a5c4418680c8b484e2831256/renditions/61134f38ef34e8f5054e3fe21cd45e8c"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/d63ac6c2a5c4418680c8b484e2831256/renditions/c14850bd22d6c503215df5978f3e6aac"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/729019e79e13207ce270a2f8b4a2be43/renditions/bcb6e26e34e74334adf5f0f720247b56"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/024f91bc58c1486988878c406ff5e85f/revisions/729019e79e13207ce270a2f8b4a2be43/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1345,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.173Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:15:38.059-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1937-010",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Fremont School, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:15:38.59-08:00",
                            "ModifyDate": "2025-06-01T14:27:39-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:15:38.59-08:00",
                    "importSource": {
                        "originalHeight": 1345,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1937-010.jpg",
                        "fileSize": 512410,
                        "originalWidth": 2000,
                        "sha256": "7dd9e12697011cb40fcf02f3e3330ebd83a83375475f5e45d59278dda28efcaf",
                        "originalDigest": "782E3F8DA5DE04A7A56452E58448AE5D",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.173Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": -13,
                        "created": "2025-06-01T22:29:17Z",
                        "dof": 2,
                        "emphasis": -20,
                        "harmony": 13,
                        "lighting": -12,
                        "repetition": 6,
                        "rot": 3,
                        "score": 66,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -44
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "b532f9cd24604e72a06a5845352b88c4",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "5927c7e291ef4b06b6f4b0a7b26f26f9"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/e512e3c37219497e85893807021257ff"
                }
            },
            "asset": {
                "id": "e512e3c37219497e85893807021257ff",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.376860Z",
                "updated": "2026-04-23T02:52:46.609865Z",
                "links": {
                    "self": {
                        "href": "assets/e512e3c37219497e85893807021257ff"
                    },
                    "/rels/comments": {
                        "href": "assets/e512e3c37219497e85893807021257ff/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/e512e3c37219497e85893807021257ff/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/24003c1a2dcd428dba5c0be8ada90ade/renditions/08bce9645729cc5f332de5519991e4ab"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/24003c1a2dcd428dba5c0be8ada90ade/renditions/c9839c9514aa8b06a4ab4cc811d6c6a7"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/24003c1a2dcd428dba5c0be8ada90ade/renditions/8bcab52ec1816c276bf3e2c301837507"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/24003c1a2dcd428dba5c0be8ada90ade/renditions/eb859a9738aecaed1130d2f734adfc8c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/9b1f6e912845466a2fe40292f72c2dee/renditions/d578b56b44194dd4bf3fa1c47826287b"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/e512e3c37219497e85893807021257ff/revisions/9b1f6e912845466a2fe40292f72c2dee/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1413,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.138Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:18:39.057-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1937-019",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Grant School, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:18:39.57-08:00",
                            "ModifyDate": "2025-06-01T14:27:48-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:18:39.57-08:00",
                    "importSource": {
                        "originalHeight": 1413,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1937-019.jpg",
                        "fileSize": 489424,
                        "originalWidth": 2000,
                        "sha256": "8c614fa665d12c381f5c567a24d7188e3e48d8ec20f707bee546e0b84f52c32a",
                        "originalDigest": "D82C144D09CED39F6E24A2620DA7F012",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.138Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 9,
                        "content": 35,
                        "created": "2025-06-01T22:29:21Z",
                        "dof": 6,
                        "emphasis": 6,
                        "harmony": 24,
                        "lighting": 4,
                        "repetition": 7,
                        "rot": 8,
                        "score": 70,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -33
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "9372fed353884b1f99659973e189407c",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "8ba36b4c049b4246bfffc071ed3090b0"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/7cd9cdf1ca064d8ab8c7c07d1208c345"
                }
            },
            "asset": {
                "id": "7cd9cdf1ca064d8ab8c7c07d1208c345",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.760712Z",
                "updated": "2026-04-23T02:52:47.060862Z",
                "links": {
                    "self": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345"
                    },
                    "/rels/comments": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/3e81f5a45805446c81a7e69929c50093/renditions/50ca123203e1a0cdc7d06a0eeadb76c5"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/3e81f5a45805446c81a7e69929c50093/renditions/5cb4bbd5d24e2771844187e2f8693fdc"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/3e81f5a45805446c81a7e69929c50093/renditions/93db73ac65c444c3abe088776867704e"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/3e81f5a45805446c81a7e69929c50093/renditions/cd68931d4c1e5daa9da7b2047b3d53fc"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/e26e0ce437ed979304532ca3e6e3196d/renditions/3b60af60a72747eba111c6c9f93633bb"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/7cd9cdf1ca064d8ab8c7c07d1208c345/revisions/e26e0ce437ed979304532ca3e6e3196d/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1350,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.245Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:22:17.039-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1935-020",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Grant School, 14th & Brockton, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:22:17.39-08:00",
                            "ModifyDate": "2025-06-01T14:23:54-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:22:17.39-08:00",
                    "importSource": {
                        "originalHeight": 1350,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1935-020.jpg",
                        "fileSize": 582527,
                        "originalWidth": 2000,
                        "sha256": "cc95aef2ffd77c7975129c05cb362829405f1d3d091a5aeee344ece978fe952d",
                        "originalDigest": "A4C6E5BE6BF5E57397B01AB6735CAA90",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.245Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 17,
                        "created": "2025-06-01T22:29:24Z",
                        "dof": 0,
                        "emphasis": -4,
                        "harmony": 13,
                        "lighting": -17,
                        "repetition": 6,
                        "rot": 4,
                        "score": 67,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -46
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "6d99674355354b9a8bc490c862911965",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "064b7ba82edb41afa8c9c85a54c0e272"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/f4b1390382c84d77a77b1fa31bd54e17"
                }
            },
            "asset": {
                "id": "f4b1390382c84d77a77b1fa31bd54e17",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.347699Z",
                "updated": "2026-04-23T02:52:47.071957Z",
                "links": {
                    "self": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17"
                    },
                    "/rels/comments": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/a7f4e60d0d9c43e8a2b01bb62b806cd9/renditions/699e43150487f6833889e91663b8d0ea"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/a7f4e60d0d9c43e8a2b01bb62b806cd9/renditions/bb10af63a3dd7d6a26f8da66f96ffa54"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/a7f4e60d0d9c43e8a2b01bb62b806cd9/renditions/3c45467d70913070a70f6ad77dcd2e5e"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/a7f4e60d0d9c43e8a2b01bb62b806cd9/renditions/a281e6455602a87b87a77b4691419d1c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/56fa8c15132851d22f3b15401552f89f/renditions/693eaf7541d74021b12f437d4b1b74b1"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/f4b1390382c84d77a77b1fa31bd54e17/revisions/56fa8c15132851d22f3b15401552f89f/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1338,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:02.124Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:23:45.025-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1937-022",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Grant School, 14th & Brockton, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:23:45.25-08:00",
                            "ModifyDate": "2025-06-01T14:27:51-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:23:45.25-08:00",
                    "importSource": {
                        "originalHeight": 1338,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1937-022.jpg",
                        "fileSize": 491581,
                        "originalWidth": 2000,
                        "sha256": "a73c1e0a24099f52fa2a282b53f3f630b93cbea683c2d571dc89c5cbc44afb5a",
                        "originalDigest": "5DBEB66E15F84197F95EE1DB2FFE9E59",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:02.124Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 4,
                        "content": 2,
                        "created": "2025-06-01T22:29:28Z",
                        "dof": -3,
                        "emphasis": -6,
                        "harmony": 4,
                        "lighting": -28,
                        "repetition": 6,
                        "rot": 1,
                        "score": 63,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -58
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "7d985e525d984c668b7ce7bbe306608d",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "cf4ee689d3384816bb320bd2fc38d81f"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/706800b0e3c842c3bd081473419782e3"
                }
            },
            "asset": {
                "id": "706800b0e3c842c3bd081473419782e3",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.408510Z",
                "updated": "2026-04-23T02:52:47.238544Z",
                "links": {
                    "self": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3"
                    },
                    "/rels/comments": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/e508444ee7474b18a8278b291cd5c25f/renditions/af1d97674751243dbde0cc18c607a1f5"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/e508444ee7474b18a8278b291cd5c25f/renditions/c63abb3fbd0969b7623fa7c4e0d6f339"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/e508444ee7474b18a8278b291cd5c25f/renditions/2e06b39b83a6821ad24231206a7496fd"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/e508444ee7474b18a8278b291cd5c25f/renditions/0e982f9e8de9d2e21f4c8de5cc563d44"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/6203fc18dd21dae8693516819b1bcc2a/renditions/a7eb1f976dc84fc9b44cc305ab5a3212"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/706800b0e3c842c3bd081473419782e3/revisions/6203fc18dd21dae8693516819b1bcc2a/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1332,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:59.656Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:45:41.075-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1939-081",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Fairmount Park, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:45:41.75-08:00",
                            "ModifyDate": "2025-06-01T15:06:15-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:45:41.75-08:00",
                    "importSource": {
                        "originalHeight": 1332,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1939-081.jpg",
                        "fileSize": 458612,
                        "originalWidth": 2000,
                        "sha256": "11f9ebb6b8df031b5e5c90cb27374c9d0af742dcf0d9ed1f77c960b4b7a65c4c",
                        "originalDigest": "356CFECB15DE7C07973C1331A6C8E35B",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:59.656Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": 4,
                        "created": "2025-06-01T22:30:22Z",
                        "dof": 15,
                        "emphasis": -12,
                        "harmony": 15,
                        "lighting": -7,
                        "repetition": 5,
                        "rot": 3,
                        "score": 69,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -36
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "c485efe303124d148faf51571e7ed365",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "bdfa110c48194e8fad021d5f48b7fe7d"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/f082a6988e48443988a7bf5ea2d2d171"
                }
            },
            "asset": {
                "id": "f082a6988e48443988a7bf5ea2d2d171",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.602174Z",
                "updated": "2026-04-23T02:52:47.273758Z",
                "links": {
                    "self": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171"
                    },
                    "/rels/comments": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/76b38df49edb4aabba73d5aae6cd76b4/renditions/9f6d5a45ce9708697f5b961083f7c85d"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/76b38df49edb4aabba73d5aae6cd76b4/renditions/bd8ac003439e44de21512b167f402897"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/76b38df49edb4aabba73d5aae6cd76b4/renditions/53d165394f35f5a9159a0f50b039c426"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/76b38df49edb4aabba73d5aae6cd76b4/renditions/6daf891b13201e1050e6a333af7f7611"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/ff40c309add7a5104c61a2b3f6723f90/renditions/1fa415f969df4c518120f6a63ac15f07"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/f082a6988e48443988a7bf5ea2d2d171/revisions/ff40c309add7a5104c61a2b3f6723f90/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1347,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:56.362Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:51:48.006-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-330",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "San Bernardino Valley College Auditorium, San Bernardino"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:51:48.60-08:00",
                            "ModifyDate": "2025-06-01T14:33:32-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:51:48.60-08:00",
                    "importSource": {
                        "originalHeight": 1347,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-330.jpg",
                        "fileSize": 339883,
                        "originalWidth": 2000,
                        "sha256": "e46cc1bc37a52ab6c15187e396f59bc4fe07477848e8feacc9aeabfa66942108",
                        "originalDigest": "E52A4B06482FB7355FF54275C33FBEA2",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:56.362Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 12,
                        "content": 55,
                        "created": "2025-06-01T22:30:34Z",
                        "dof": 13,
                        "emphasis": 22,
                        "harmony": 25,
                        "lighting": 7,
                        "repetition": 9,
                        "rot": 10,
                        "score": 75,
                        "symmetry": 6,
                        "version": 1,
                        "vivid": -34
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "bec3f452401447f9918170e82772b917",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "7b6ff3c00a3a4c759d42340f75f20d9e"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/9fdf8c1344cd4015973f4355758b6bee"
                }
            },
            "asset": {
                "id": "9fdf8c1344cd4015973f4355758b6bee",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.507941Z",
                "updated": "2026-04-23T02:52:47.270223Z",
                "links": {
                    "self": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee"
                    },
                    "/rels/comments": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/08fa92025ba3457ca47f5e80ac46fc99/renditions/5fcc785973395b2c954bdee3a25cee85"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/08fa92025ba3457ca47f5e80ac46fc99/renditions/c3701fa5d6df82c1c80b92ffda184d9e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/08fa92025ba3457ca47f5e80ac46fc99/renditions/d8d65a7b95863714a02b466bbb3157b9"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/08fa92025ba3457ca47f5e80ac46fc99/renditions/1ea75d4d819dffd82d1f053e2cf871e5"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/fb2142f368f09efeb2d6d1651bebb2e5/renditions/28a7d5f4cb1146cdb9af04dd5fce8be4"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/9fdf8c1344cd4015973f4355758b6bee/revisions/fb2142f368f09efeb2d6d1651bebb2e5/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 1341,
                        "croppedHeight": 2000,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.353Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T16:52:31.066-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-333",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "San Bernardino Valley College Auditorium, San Bernardino"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T16:52:31.66-08:00",
                            "ModifyDate": "2025-06-01T14:33:35-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T16:52:31.66-08:00",
                    "importSource": {
                        "originalHeight": 2000,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-333.jpg",
                        "fileSize": 375119,
                        "originalWidth": 1341,
                        "sha256": "1761b327a9e48a8127611d75891beeef34893a0b16763c7c8690ea03a562984a",
                        "originalDigest": "537A68D8C381C328C413B35B41C02190",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.353Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -3,
                        "content": -52,
                        "created": "2025-06-01T22:30:35Z",
                        "dof": -13,
                        "emphasis": -48,
                        "harmony": -9,
                        "lighting": -52,
                        "repetition": 6,
                        "rot": -5,
                        "score": 55,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -73
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "4c1affb9f1c54e9592ad914c41e0fc76",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "288b9e05344b4609bba372b5b8f0f92d"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/e936ec0c998d42eda0d23539a627e01e"
                }
            },
            "asset": {
                "id": "e936ec0c998d42eda0d23539a627e01e",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.141369Z",
                "updated": "2026-04-23T02:52:47.397455Z",
                "links": {
                    "self": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e"
                    },
                    "/rels/comments": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/71de1d72c11b4a3589a4083af626594d/renditions/a3691e960bbaf3846d2f67612e497b74"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/71de1d72c11b4a3589a4083af626594d/renditions/d622c1209d99da80c8b531b389003407"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/71de1d72c11b4a3589a4083af626594d/renditions/5e8719a1e5720f1d15a9fbe01c25f340"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/71de1d72c11b4a3589a4083af626594d/renditions/e4690b0b46e902bdf15840088e4a7fc7"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/b5db0e73b93ea66d82325f667888abf0/renditions/b0be33bcbee048dea2eded0c55a5f5ca"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/e936ec0c998d42eda0d23539a627e01e/revisions/b5db0e73b93ea66d82325f667888abf0/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1350,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.246Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T18:04:25.038-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-345",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "East Wing, Riverside General Hospital, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T18:04:25.38-08:00",
                            "ModifyDate": "2025-06-01T14:33:47-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T18:04:25.38-08:00",
                    "importSource": {
                        "originalHeight": 1350,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-345.jpg",
                        "fileSize": 389883,
                        "originalWidth": 2000,
                        "sha256": "6a14a8ded9cd6f0390888ea3b674ffa60d21c2282c47596abbd9d4af634b661a",
                        "originalDigest": "736C06E5A4AC7244684D91DFD09A73C5",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.246Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -21,
                        "created": "2025-06-01T22:30:50Z",
                        "dof": 1,
                        "emphasis": -20,
                        "harmony": 2,
                        "lighting": -29,
                        "repetition": 7,
                        "rot": -2,
                        "score": 63,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -54
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "aafb20fa86544dfeacaacfdc9744a38e",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "42e4ca45cee14f91a62b17daf60405cb"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/388b900c4ec24eca8a8e3bc02c9539c4"
                }
            },
            "asset": {
                "id": "388b900c4ec24eca8a8e3bc02c9539c4",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.146984Z",
                "updated": "2026-04-23T02:52:47.373108Z",
                "links": {
                    "self": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4"
                    },
                    "/rels/comments": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/56c36b6bfdda4200941c05f769c30c12/renditions/e1eb44808161f3aaddfc775999986e61"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/56c36b6bfdda4200941c05f769c30c12/renditions/244d6e6b1bbf23c5540588dcf361bc3e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/56c36b6bfdda4200941c05f769c30c12/renditions/f99681eed15e90bbd9ef376bc427669f"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/56c36b6bfdda4200941c05f769c30c12/renditions/27a0e96f62744dc5687b4ec606595057"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/612607dd6c26942062e303c11584bbaf/renditions/80a70347e7004be2b4018bb62de19129"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/388b900c4ec24eca8a8e3bc02c9539c4/revisions/612607dd6c26942062e303c11584bbaf/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 1369,
                        "croppedHeight": 2000,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.245Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T18:04:37.004-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-346",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "East Wing, Riverside General Hospital, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T18:04:37.04-08:00",
                            "ModifyDate": "2025-06-01T14:33:48-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T18:04:37.04-08:00",
                    "importSource": {
                        "originalHeight": 2000,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-346.jpg",
                        "fileSize": 468282,
                        "originalWidth": 1369,
                        "sha256": "c41295c46bcf86aa07732c220174247e778a76864cbbad3cee95565a156e0ff2",
                        "originalDigest": "039B35C8A060276E10C66B9B54ADC874",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.245Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -12,
                        "created": "2025-06-01T22:30:51Z",
                        "dof": 0,
                        "emphasis": -20,
                        "harmony": 9,
                        "lighting": -23,
                        "repetition": 8,
                        "rot": 0,
                        "score": 65,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -54
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "eacbd051613c4b06b6a9914a69b36770",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "92367a96908c4d9cb810a8dd6bc9cab0"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/075ae4f9475144de8ca4e9b0ad186325"
                }
            },
            "asset": {
                "id": "075ae4f9475144de8ca4e9b0ad186325",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.136681Z",
                "updated": "2026-04-23T02:52:47.127017Z",
                "links": {
                    "self": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325"
                    },
                    "/rels/comments": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/3e9b1249bb834874883c2a107f90c6ae/renditions/025f2b63df4f8763446393d405822a6d"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/3e9b1249bb834874883c2a107f90c6ae/renditions/bc1c7da72a88771f37ab7955addd189c"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/3e9b1249bb834874883c2a107f90c6ae/renditions/8e1ce7e9cf0a3eba24d162c9a263c530"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/3e9b1249bb834874883c2a107f90c6ae/renditions/66094f7e9c64e6bc6a7a2dbf99d69b25"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/c651ed41fbaa18b48730b2efc9e911d5/renditions/1a9b423b549246ada65d345619c5d96f"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/075ae4f9475144de8ca4e9b0ad186325/revisions/c651ed41fbaa18b48730b2efc9e911d5/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1339,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.227Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T18:06:48.023-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-348",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Powerhouse and Laundry addition with Tuberculosis Building in background, Riverside General Hospital, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T18:06:48.23-08:00",
                            "ModifyDate": "2025-06-01T14:33:50-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T18:06:48.23-08:00",
                    "importSource": {
                        "originalHeight": 1339,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-348.jpg",
                        "fileSize": 369061,
                        "originalWidth": 2000,
                        "sha256": "8175d5bac06226b1c6c88dd40aa6a302fe41edfe706ffab495438ab67e666709",
                        "originalDigest": "F84DBAE2B3F4BAA644A5A96E74344E6E",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.227Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": -15,
                        "created": "2025-06-01T22:30:57Z",
                        "dof": -2,
                        "emphasis": -30,
                        "harmony": 7,
                        "lighting": -30,
                        "repetition": 8,
                        "rot": 0,
                        "score": 61,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -61
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "9e9a7e6a6a8c4a749a3813241c78a80a",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "f5fd3a406eac49a5afad3fe12bdc6442"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/6020040334934df2a3e5c2561124545a"
                }
            },
            "asset": {
                "id": "6020040334934df2a3e5c2561124545a",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.959396Z",
                "updated": "2026-04-23T02:52:47.147828Z",
                "links": {
                    "self": {
                        "href": "assets/6020040334934df2a3e5c2561124545a"
                    },
                    "/rels/comments": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/9f18c33103c541f2a4fb5823692d1b2c/renditions/e6ebc8449699d9ce6f086f29a2f6deda"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/9f18c33103c541f2a4fb5823692d1b2c/renditions/25eb703cd9d2f54cf1e0577eb4f418ea"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/9f18c33103c541f2a4fb5823692d1b2c/renditions/8036f47d1da62f60dd742ec60d961b00"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/9f18c33103c541f2a4fb5823692d1b2c/renditions/d78fa6cfb2bd1cb42961f1d044057802"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/30b174fb6d47ec04e8d6238612f696df/renditions/e2fbeea457af4b49b78c9bca7d1d70c9"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/6020040334934df2a3e5c2561124545a/revisions/30b174fb6d47ec04e8d6238612f696df/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1352,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.169Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T18:10:22.003-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-357",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Powerhouse and Laundry addition, Riverside General Hospital, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T18:10:22.30-08:00",
                            "ModifyDate": "2025-06-01T14:34:00-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T18:10:22.30-08:00",
                    "importSource": {
                        "originalHeight": 1352,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-357.jpg",
                        "fileSize": 396297,
                        "originalWidth": 2000,
                        "sha256": "da3e55fcf362184eda0d3c926ee69eaf72fb1ec7a892d51ade97eaa43b9f0c64",
                        "originalDigest": "376BF8E04FC1BF21F493EDE88555368A",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.169Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -31,
                        "created": "2025-06-01T22:31:09Z",
                        "dof": -2,
                        "emphasis": -30,
                        "harmony": 0,
                        "lighting": -37,
                        "repetition": 5,
                        "rot": -1,
                        "score": 59,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -59
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "33436e11f3024b259b36740c769248ff",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "03864724816e4ce2853cdf917a9a7ecb"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/971ede4e5d084d7daebdca92609022aa"
                }
            },
            "asset": {
                "id": "971ede4e5d084d7daebdca92609022aa",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.776074Z",
                "updated": "2026-04-23T02:52:47.227702Z",
                "links": {
                    "self": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa"
                    },
                    "/rels/comments": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/42521daaa56e4434a4ad18c35d8bc4e6/renditions/012df5132864489ec7800c11b4c89890"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/42521daaa56e4434a4ad18c35d8bc4e6/renditions/45f25baf418f708aaf69a0b28c2bc104"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/42521daaa56e4434a4ad18c35d8bc4e6/renditions/f753e990e89ad50753a82463a8edb61e"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/42521daaa56e4434a4ad18c35d8bc4e6/renditions/b64984ceb08332d13da6e3c8c7d9f4fd"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/9eb1c18b2d8979aa406b9701c45cec70/renditions/e37dc38d22e946b28adc1dc910047cae"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/971ede4e5d084d7daebdca92609022aa/revisions/9eb1c18b2d8979aa406b9701c45cec70/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1350,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.092Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-10T18:14:38.067-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-366",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "East Wing, Riverside General Hospital, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-10T18:14:38.67-08:00",
                            "ModifyDate": "2025-06-01T14:34:10-07:00"
                        }
                    },
                    "captureDate": "2024-03-10T18:14:38.67-08:00",
                    "importSource": {
                        "originalHeight": 1350,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-366.jpg",
                        "fileSize": 382059,
                        "originalWidth": 2000,
                        "sha256": "261cad2c7d1c31e0ed0725ef7cefb77ec2ccc5a03e6bb9f565c78fd5c286e25a",
                        "originalDigest": "752CA6E6734D2584CD6F0356E000BEFF",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.092Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": 0,
                        "created": "2025-06-01T22:31:14Z",
                        "dof": 4,
                        "emphasis": -5,
                        "harmony": 11,
                        "lighting": -17,
                        "repetition": 8,
                        "rot": 0,
                        "score": 67,
                        "symmetry": 5,
                        "version": 1,
                        "vivid": -42
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "b2f53d8c7fb2417990d91060f1c8cca0",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "8199d7619eff4f2ab195b0227a85fe49"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/959e99c945124be0b7503a52407a40c8"
                }
            },
            "asset": {
                "id": "959e99c945124be0b7503a52407a40c8",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.988483Z",
                "updated": "2026-04-23T02:52:47.475575Z",
                "links": {
                    "self": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8"
                    },
                    "/rels/comments": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/782a8d5ea60a41cb88519903e1783223/renditions/9d6be67e70bfab2d302231c6664ca922"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/782a8d5ea60a41cb88519903e1783223/renditions/10b22926335cc13c2456125c168652a5"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/782a8d5ea60a41cb88519903e1783223/renditions/269cf60f73a870f177eec09c4bf3d10d"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/782a8d5ea60a41cb88519903e1783223/renditions/00f8f7e865e035ce1acf17fb7ce7d8e4"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/fdee304fce88b331b5a45cf0d18ad9c8/renditions/fd45526c8072459fa102d4a03cc51175"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/959e99c945124be0b7503a52407a40c8/revisions/fdee304fce88b331b5a45cf0d18ad9c8/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1338,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:01.970Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T09:37:20.088-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-008",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": " Jefferson Elementary School Library, Corona"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T09:37:20.88-08:00",
                            "ModifyDate": "2025-06-01T14:28:46-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T09:37:20.88-08:00",
                    "importSource": {
                        "originalHeight": 1338,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-008.jpg",
                        "fileSize": 337837,
                        "originalWidth": 2000,
                        "sha256": "dfc287c90c25a7b5b72faa100276edaa7001d6fb2d8564e64d1f0e4ddd6fbe48",
                        "originalDigest": "36DCADF599E2333A0024093473B4E06A",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:01.970Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -42,
                        "created": "2025-06-01T22:33:27Z",
                        "dof": -9,
                        "emphasis": -51,
                        "harmony": -4,
                        "lighting": -50,
                        "repetition": 5,
                        "rot": -2,
                        "score": 59,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -67
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "a69dcf968d6b42e6a74f51bb2ea06a39",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "858539feddc14168912968c731ebc434"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/d848704296b34db2b4762fdf4754aa23"
                }
            },
            "asset": {
                "id": "d848704296b34db2b4762fdf4754aa23",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.666959Z",
                "updated": "2026-04-23T02:52:47.649573Z",
                "links": {
                    "self": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23"
                    },
                    "/rels/comments": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/6fd7877eaac9428eb3d4fa2eabef22ff/renditions/e17a2ae2183f46c091110e0fb8f4c442"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/6fd7877eaac9428eb3d4fa2eabef22ff/renditions/6eb39277a5bb4d41097005e340546aae"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/6fd7877eaac9428eb3d4fa2eabef22ff/renditions/b8a7e4b75f6ce8c03d89da824687c1be"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/6fd7877eaac9428eb3d4fa2eabef22ff/renditions/a9167ce7184f72b8259dd3a202236c7d"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/a398680dde2392a39b453c9174b3ebed/renditions/7a60ae224c3a44f6999a46fd6c0e9c0c"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/d848704296b34db2b4762fdf4754aa23/revisions/a398680dde2392a39b453c9174b3ebed/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 1340,
                        "croppedHeight": 2000,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:01.928Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T09:39:50.079-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-016",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Jefferson Elementary School Library Wing, Corona"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T09:39:50.79-08:00",
                            "ModifyDate": "2025-06-01T14:28:54-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T09:39:50.79-08:00",
                    "importSource": {
                        "originalHeight": 2000,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-016.jpg",
                        "fileSize": 291143,
                        "originalWidth": 1340,
                        "sha256": "cb78514c6bf8143341a887e1def925fc41737c0fcc48091cfd6b727221390d84",
                        "originalDigest": "25B9D439D88FAAC8DCCFBC16CBBF181B",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:01.928Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -5,
                        "content": -58,
                        "created": "2025-06-01T22:33:36Z",
                        "dof": -11,
                        "emphasis": -63,
                        "harmony": -1,
                        "lighting": -38,
                        "repetition": 6,
                        "rot": -7,
                        "score": 49,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "46761cb0dbdb430e94f789d246cd07fc",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "8a57e2c9c7854dfe94f03ee099dce07d"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/1ffdfb2e22164e11a456315bfaa9124f"
                }
            },
            "asset": {
                "id": "1ffdfb2e22164e11a456315bfaa9124f",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.504197Z",
                "updated": "2026-04-23T02:52:48.056879Z",
                "links": {
                    "self": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f"
                    },
                    "/rels/comments": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/53c070634c284eb899939d4bc4185219/renditions/8a5de0dfa01a9be66f020f655337f95e"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/53c070634c284eb899939d4bc4185219/renditions/4be5344bdfb0f8364458ba11bb30221c"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/53c070634c284eb899939d4bc4185219/renditions/1620ee0e8c43f6b7c84a677d5aefedc7"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/53c070634c284eb899939d4bc4185219/renditions/d1804b6b8649d5d855821491dbbda4fd"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/a06a0c67485d12372fdb8aafff41cd57/renditions/f7a70f0ca0c64b059e20a1f655adc2d8"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/1ffdfb2e22164e11a456315bfaa9124f/revisions/a06a0c67485d12372fdb8aafff41cd57/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1337,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:56.647Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T09:48:18.075-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-030",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Corona Junior High School, Corona"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T09:48:18.75-08:00",
                            "ModifyDate": "2025-06-01T14:29:09-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T09:48:18.75-08:00",
                    "importSource": {
                        "originalHeight": 1337,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-030.jpg",
                        "fileSize": 341061,
                        "originalWidth": 2000,
                        "sha256": "82d224a19e8f7f70f7aaf55222a565ebd80e624ecaee4ae15d05a71b1533502a",
                        "originalDigest": "C0A7C0B32368482942A62A9D610DF4D6",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:56.647Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -1,
                        "content": -46,
                        "created": "2025-06-01T22:33:50Z",
                        "dof": -5,
                        "emphasis": -45,
                        "harmony": -5,
                        "lighting": -41,
                        "repetition": 6,
                        "rot": -2,
                        "score": 62,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -65
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "9ae4c6f917664b9bbd87fe255330ad2a",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "954475419ce3490f99837bed42b960d7"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/1aa7b33717014a62b8105425a7b741d4"
                }
            },
            "asset": {
                "id": "1aa7b33717014a62b8105425a7b741d4",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.307481Z",
                "updated": "2026-04-23T02:52:48.570395Z",
                "links": {
                    "self": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4"
                    },
                    "/rels/comments": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3fbdb4f2fd9a40a394c28990fb07f3a8/renditions/70be36a34a6501eaa2a398d144c40d53"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3fbdb4f2fd9a40a394c28990fb07f3a8/renditions/9a3f63451dcb74c57335a6abea89af5b"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3fbdb4f2fd9a40a394c28990fb07f3a8/renditions/362517e7199ca8b583153363da30169f"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3fbdb4f2fd9a40a394c28990fb07f3a8/renditions/83ef98d3e7e36482cb4b0c9c6e214b1c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3ed161517cf899ce1a259edad8801374/renditions/9346cb25d37b4907840e2de1c45ceadd"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/1aa7b33717014a62b8105425a7b741d4/revisions/3ed161517cf899ce1a259edad8801374/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1321,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:56.644Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T09:48:57.013-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-034",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Corona Junior High School, Corona"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T09:48:57.13-08:00",
                            "ModifyDate": "2025-06-01T14:29:13-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T09:48:57.13-08:00",
                    "importSource": {
                        "originalHeight": 1321,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-034.jpg",
                        "fileSize": 261897,
                        "originalWidth": 2000,
                        "sha256": "a6b7e5070a3c8524cdcd951aa685534871b1eaed3b2d400a2bc26807b32266e1",
                        "originalDigest": "F32EA4DEDB0B969D0F8A52E93919F483",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:56.644Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -3,
                        "content": -28,
                        "created": "2025-06-01T22:34:00Z",
                        "dof": -11,
                        "emphasis": -19,
                        "harmony": -7,
                        "lighting": -41,
                        "repetition": 4,
                        "rot": -6,
                        "score": 52,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -59
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "e6eafa7a1fef405a88edc4f4138e59d8",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "1cfef53be5ca413385fcb6fa3b89ab94"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/4dba271198c3462190271d8453a98a2c"
                }
            },
            "asset": {
                "id": "4dba271198c3462190271d8453a98a2c",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.142336Z",
                "updated": "2026-04-23T02:52:48.645775Z",
                "links": {
                    "self": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c"
                    },
                    "/rels/comments": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/0d646f9ba6d040b6bfbebec6b87813f6/renditions/e28676b80358e60f9e24dfc383dbb384"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/0d646f9ba6d040b6bfbebec6b87813f6/renditions/b06a1290e65f1fa3673e433b18bd4b7e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/0d646f9ba6d040b6bfbebec6b87813f6/renditions/5eb1973260eff36dc319c8917c59c098"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/0d646f9ba6d040b6bfbebec6b87813f6/renditions/273d602fe4a90dca40c957626a4d64ea"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/7454e381f335dede8f1a7ec1e3bf5dd4/renditions/6a98a3de68a043fdaaf464aca21a0935"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/4dba271198c3462190271d8453a98a2c/revisions/7454e381f335dede8f1a7ec1e3bf5dd4/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1347,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:59.027Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T10:11:32.007-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1939-204",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "City Hall, Brawley, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T10:11:32.07-08:00",
                            "ModifyDate": "2025-06-01T15:08:30-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T10:11:32.07-08:00",
                    "importSource": {
                        "originalHeight": 1347,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1939-204.jpg",
                        "fileSize": 487871,
                        "originalWidth": 2000,
                        "sha256": "04ae9bc0c15f88843bd4f9fa0c931708109242d5a859af7a385f99dc74d76d44",
                        "originalDigest": "26E841C288AD6D96AD690CE5A9E80D48",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:59.027Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": 7,
                        "created": "2025-06-01T22:35:00Z",
                        "dof": 5,
                        "emphasis": 0,
                        "harmony": 16,
                        "lighting": -4,
                        "repetition": 7,
                        "rot": 2,
                        "score": 68,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -39
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "81043f99d6fd45329b3d865675d0f686",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "6e9d4da42d3a4104b98a742c8086019b"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/0d3894d1bb3c4af08352fe4f9a8a6eb9"
                }
            },
            "asset": {
                "id": "0d3894d1bb3c4af08352fe4f9a8a6eb9",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.120741Z",
                "updated": "2026-04-23T02:52:48.482218Z",
                "links": {
                    "self": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9"
                    },
                    "/rels/comments": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/7ef65e2da21f44839122de5dc46cc65c/renditions/3e206e02879d37fcb44e04317c97a580"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/7ef65e2da21f44839122de5dc46cc65c/renditions/65687ec87cfbac72a18d293fe43719e7"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/7ef65e2da21f44839122de5dc46cc65c/renditions/ec8aec56a048a9e827055be9d92867cc"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/7ef65e2da21f44839122de5dc46cc65c/renditions/21b97313049ff41e16877216de43baf1"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/e497a79237201d56290666c1a78cad5c/renditions/50670610ec284551aab814462f0a9e9a"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/0d3894d1bb3c4af08352fe4f9a8a6eb9/revisions/e497a79237201d56290666c1a78cad5c/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1343,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:59.007Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T10:12:06.037-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1939-208",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Southern Sierras Power Company Office, Brawley, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T10:12:06.37-08:00",
                            "ModifyDate": "2025-06-01T15:08:35-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T10:12:06.37-08:00",
                    "importSource": {
                        "originalHeight": 1343,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1939-208.jpg",
                        "fileSize": 558952,
                        "originalWidth": 2000,
                        "sha256": "d807db03df5f65ca0eced9330e4e32f4c0295d24612099fe0a5bbe281ed44330",
                        "originalDigest": "DAE4968433A49BC04FB9B4EEF21CD7B9",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:59.007Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -1,
                        "content": -36,
                        "created": "2025-06-01T22:35:04Z",
                        "dof": -4,
                        "emphasis": -43,
                        "harmony": 0,
                        "lighting": -36,
                        "repetition": 6,
                        "rot": -3,
                        "score": 54,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -55
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "4f25246d5bd2480c84b5be2850b0a6d8",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "4697d982c7ff466ba315318fbd4e69e1"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/7b73615c26be4e1f978e5c1aa5ab098d"
                }
            },
            "asset": {
                "id": "7b73615c26be4e1f978e5c1aa5ab098d",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.423236Z",
                "updated": "2026-04-23T02:52:48.715412Z",
                "links": {
                    "self": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d"
                    },
                    "/rels/comments": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/d27c298df4274cb1a487bb86645a2e69/renditions/5bd85197810083ab8cd3f09039c98f66"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/d27c298df4274cb1a487bb86645a2e69/renditions/91622986c98ad2c6350ae5a77fa08b48"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/d27c298df4274cb1a487bb86645a2e69/renditions/6bbeb1ed109b9704fee38ec70ac284aa"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/d27c298df4274cb1a487bb86645a2e69/renditions/834c7a23a774da10254b8ad7119a72d6"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/992d936e45e847104aac02f9980fad00/renditions/a6f382fc5677478e8ab2d979e639f7e1"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/7b73615c26be4e1f978e5c1aa5ab098d/revisions/992d936e45e847104aac02f9980fad00/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1335,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:58.903Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T10:22:15.073-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1940-023",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "St Francis de Sales Convent and Chapel, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T10:22:15.73-08:00",
                            "ModifyDate": "2025-06-01T15:10:00-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T10:22:15.73-08:00",
                    "importSource": {
                        "originalHeight": 1335,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1940-023.jpg",
                        "fileSize": 479889,
                        "originalWidth": 2000,
                        "sha256": "cb4801a15ae57522bf7466959b66d63b9c9f6eafe1b33d6965b01e4a79740912",
                        "originalDigest": "39AEBFF1EA55A1A0B1593F19B214ABB0",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:58.903Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 1,
                        "content": -33,
                        "created": "2025-06-01T22:36:29Z",
                        "dof": 1,
                        "emphasis": -48,
                        "harmony": 9,
                        "lighting": -18,
                        "repetition": 6,
                        "rot": 1,
                        "score": 65,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -48
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "f6af7e8bf58d476189d00a9c04841697",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "c02b23f252b24f74994cabf788e506a9"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/66bd9640f32445138c39a2cb1bb579fc"
                }
            },
            "asset": {
                "id": "66bd9640f32445138c39a2cb1bb579fc",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.278114Z",
                "updated": "2026-04-23T02:52:48.826824Z",
                "links": {
                    "self": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc"
                    },
                    "/rels/comments": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/2130dfefa6704add83032414ab3c3343/renditions/f3a675a52171da22e4b43e937dc79821"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/2130dfefa6704add83032414ab3c3343/renditions/873808e99d27a32fa700cc2636111f0f"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/2130dfefa6704add83032414ab3c3343/renditions/f0013bc75c13293ad0cb37c5ee42a5e1"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/2130dfefa6704add83032414ab3c3343/renditions/845b6c37d943a5821efa3ddf9b5d2244"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/cb267567eca08be492ddd463dfb409be/renditions/9aedc3cf96a447ce84e1976729c3a622"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/66bd9640f32445138c39a2cb1bb579fc/revisions/cb267567eca08be492ddd463dfb409be/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1341,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:58.863Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T10:24:20.065-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1940-030",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "1984 Bonnie Brae Street, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T10:24:20.65-08:00",
                            "ModifyDate": "2025-06-01T15:10:07-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T10:24:20.65-08:00",
                    "importSource": {
                        "originalHeight": 1341,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1940-030.jpg",
                        "fileSize": 727462,
                        "originalWidth": 2000,
                        "sha256": "9f1f38214cc09e73fb0fb19f711bb88da12e8a065e87b386857e1a4856e3dc60",
                        "originalDigest": "A7D2B103DD2AF1E052A86DE06E0027F5",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:58.863Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 14,
                        "created": "2025-06-01T22:35:29Z",
                        "dof": 0,
                        "emphasis": -9,
                        "harmony": 13,
                        "lighting": -18,
                        "repetition": 8,
                        "rot": 2,
                        "score": 64,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -47
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "ea4bb4c40e3b41bdb6cdd4b895faeb60",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "68bf596d2aa6495d8872c435f3bc7c42"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/799477affde54f4a9334b48668128cc1"
                }
            },
            "asset": {
                "id": "799477affde54f4a9334b48668128cc1",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.506495Z",
                "updated": "2026-04-23T02:52:48.978047Z",
                "links": {
                    "self": {
                        "href": "assets/799477affde54f4a9334b48668128cc1"
                    },
                    "/rels/comments": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/e39151139c4448f7817b6c526bb5ca22/renditions/9a5c0f8bb43836d794f6a9aba7e6b2db"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/e39151139c4448f7817b6c526bb5ca22/renditions/df665a3ba21e5da5a4265dc12cd9702e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/e39151139c4448f7817b6c526bb5ca22/renditions/ab58c447a1cd6ec7b0b8bd04bee23df4"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/e39151139c4448f7817b6c526bb5ca22/renditions/7bbff394e9b9b8c417793db5aa84aca8"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/b547c2f5459d6bab0ecc5a70f887b9cf/renditions/bc7968ceff404981a0143ce15de11fd6"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/799477affde54f4a9334b48668128cc1/revisions/b547c2f5459d6bab0ecc5a70f887b9cf/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1367,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:57.518Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T11:10:35.014-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-081",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Blaine Street Federal Housing, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T11:10:35.14-08:00",
                            "ModifyDate": "2025-06-01T15:14:52-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T11:10:35.14-08:00",
                    "importSource": {
                        "originalHeight": 1367,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-081.jpg",
                        "fileSize": 416553,
                        "originalWidth": 2000,
                        "sha256": "5a15e14534cb092f850b0ff6582fc086428ae80f56a3e7e3f73597d26db90b25",
                        "originalDigest": "BCB84535334595948D89CA49F7D0A456",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:57.518Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 1,
                        "content": -21,
                        "created": "2025-06-01T22:35:53Z",
                        "dof": 0,
                        "emphasis": -28,
                        "harmony": 0,
                        "lighting": -31,
                        "repetition": 6,
                        "rot": 0,
                        "score": 58,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -58
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "4d21495df416434aaa2963512232fba9",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "97d2897930ab450eb173d21576b5a15a"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/66766d401a8e4c7184b9b2cc8951fc82"
                }
            },
            "asset": {
                "id": "66766d401a8e4c7184b9b2cc8951fc82",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.455674Z",
                "updated": "2026-04-23T02:52:49.153307Z",
                "links": {
                    "self": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82"
                    },
                    "/rels/comments": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/3e87111afcfd458fa1aa2b1f9163e3e7/renditions/a03dac2a817f6e79d2f35e8196e38964"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/3e87111afcfd458fa1aa2b1f9163e3e7/renditions/bee1169db60126ac903a79b0f7fa5a12"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/3e87111afcfd458fa1aa2b1f9163e3e7/renditions/1bad1b471c3fcc359565bd1364d8473f"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/3e87111afcfd458fa1aa2b1f9163e3e7/renditions/b0fbdaef40e58472088b6c32a8b3d2cd"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/5efec4b42e2e740a771037d740e229c7/renditions/93874c4b02564bef8279dff4c5df48a4"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/66766d401a8e4c7184b9b2cc8951fc82/revisions/5efec4b42e2e740a771037d740e229c7/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1367,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:57.495Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T11:10:52.054-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-083",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Blaine Street Federal Housing, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T11:10:52.54-08:00",
                            "ModifyDate": "2025-06-01T15:14:54-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T11:10:52.54-08:00",
                    "importSource": {
                        "originalHeight": 1367,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-083.jpg",
                        "fileSize": 412573,
                        "originalWidth": 2000,
                        "sha256": "0ed18d2633facb0c2af52df1a047b5736ff1cd1759bb421b02a8376ba45ba2e0",
                        "originalDigest": "718C40BB2E6C1551F51111146E2805EF",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:57.495Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -2,
                        "content": -44,
                        "created": "2025-06-01T22:35:55Z",
                        "dof": -4,
                        "emphasis": -55,
                        "harmony": 3,
                        "lighting": -30,
                        "repetition": 8,
                        "rot": -3,
                        "score": 55,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -51
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "be7617d9f1da42ddb730110b3dcfd224",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "8c702a9ef6764ba7beb1d4bcf0c87860"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/1053076afaa849e784c65ee8dfb0e35a"
                }
            },
            "asset": {
                "id": "1053076afaa849e784c65ee8dfb0e35a",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.476079Z",
                "updated": "2026-04-23T02:52:49.237403Z",
                "links": {
                    "self": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a"
                    },
                    "/rels/comments": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/9dcc4ba611e04e1d81a4f867ce72a664/renditions/1f7d31b24061e085fc621c4540f73496"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/9dcc4ba611e04e1d81a4f867ce72a664/renditions/7acf617b4388ab115eff9a0b8d400773"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/9dcc4ba611e04e1d81a4f867ce72a664/renditions/f51ab18bbdc8939c2b39c3d438abd6df"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/9dcc4ba611e04e1d81a4f867ce72a664/renditions/b5f7df7637aebbb9185b73bd0af18463"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/cbfe1f0166e3d12ae5f0c7907aa6465c/renditions/4147406ebae5434e9aca70148edc339b"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/1053076afaa849e784c65ee8dfb0e35a/revisions/cbfe1f0166e3d12ae5f0c7907aa6465c/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1367,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:57.494Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T11:11:08-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1943-084",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Blaine Street Federal Housing, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T11:11:08.00-08:00",
                            "ModifyDate": "2025-06-01T15:14:55-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T11:11:08.00-08:00",
                    "importSource": {
                        "originalHeight": 1367,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1943-084.jpg",
                        "fileSize": 408437,
                        "originalWidth": 2000,
                        "sha256": "55214f41e9fe69c2f6e47384d676cd01280180e9189e4fe74904c2bc8188f4ec",
                        "originalDigest": "2074490ED07A5A96BBB2123E0634DF1C",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:57.494Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -5,
                        "content": -77,
                        "created": "2025-06-01T22:35:57Z",
                        "dof": -11,
                        "emphasis": -82,
                        "harmony": -9,
                        "lighting": -52,
                        "repetition": 5,
                        "rot": -6,
                        "score": 51,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -68
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "0ad4494704234ba589596e046fd0b7eb",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "1d381cefc95e4c3eb44f5ecb61c62d6d"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/a70838f7752d4104a13f1c6e3a7fb6ff"
                }
            },
            "asset": {
                "id": "a70838f7752d4104a13f1c6e3a7fb6ff",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:06.014650Z",
                "updated": "2026-04-23T02:52:49.282092Z",
                "links": {
                    "self": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff"
                    },
                    "/rels/comments": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/7469fcb5d2ff4ae6945c3066f41d2a6b/renditions/3d94568ff84e5d3a294fede4dbb1186a"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/7469fcb5d2ff4ae6945c3066f41d2a6b/renditions/6cee30361b5b3f9ecc5eb381bee9a2c6"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/7469fcb5d2ff4ae6945c3066f41d2a6b/renditions/8842607c1c39f1610330976f74dc9a6c"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/7469fcb5d2ff4ae6945c3066f41d2a6b/renditions/a547d6274952357b41a5df994bdfcab5"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/43793365783d7b9377481c102c713249/renditions/8d65d98a2abc4480bdf32b332a288187"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/a70838f7752d4104a13f1c6e3a7fb6ff/revisions/43793365783d7b9377481c102c713249/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1336,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.533Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T11:45:57.065-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-260",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Riverside Engine Company #4, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T11:45:57.65-08:00",
                            "ModifyDate": "2025-06-01T14:32:58-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T11:45:57.65-08:00",
                    "importSource": {
                        "originalHeight": 1336,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-260.jpg",
                        "fileSize": 423237,
                        "originalWidth": 2000,
                        "sha256": "d275ac395664cae86d3fdc35772c60ccc3f0fca83eb72f65c105882e1bbb9fed",
                        "originalDigest": "6CD180038D3D5629D90BE1BEC570F494",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.533Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 1,
                        "content": -5,
                        "created": "2025-06-01T22:37:08Z",
                        "dof": 8,
                        "emphasis": -15,
                        "harmony": 13,
                        "lighting": -14,
                        "repetition": 6,
                        "rot": 1,
                        "score": 69,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -41
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "32efdde04c004f67834ed3a1abc0cdbd",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "3210b9fdfb3a484fb2ed24d3a9e951bf"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/e39f8b863cb54f87a74f2612c96369a2"
                }
            },
            "asset": {
                "id": "e39f8b863cb54f87a74f2612c96369a2",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:05.929763Z",
                "updated": "2026-04-23T02:52:49.531274Z",
                "links": {
                    "self": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2"
                    },
                    "/rels/comments": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/2d0e4fb723e045ee943dc59aaaa6fecb/renditions/0cb32ed76c64f350305e59ed4bfbd3d3"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/2d0e4fb723e045ee943dc59aaaa6fecb/renditions/012c5c9a043095707fcd8e80dd8412e3"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/2d0e4fb723e045ee943dc59aaaa6fecb/renditions/0d58e31329bb641dfa9184596e0f1a80"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/2d0e4fb723e045ee943dc59aaaa6fecb/renditions/c4d42d28fa471adf8b0bba0cd2675333"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/1cbdd28b10b66847e5c20811f098361e/renditions/229c4912631d4b2ab43a778a70d70b3d"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/e39f8b863cb54f87a74f2612c96369a2/revisions/1cbdd28b10b66847e5c20811f098361e/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1350,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:20:00.499Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T11:47:55.061-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1938-267",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Riverside Engine Company #4, Riverside"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T11:47:55.61-08:00",
                            "ModifyDate": "2025-06-01T14:33:05-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T11:47:55.61-08:00",
                    "importSource": {
                        "originalHeight": 1350,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1938-267.jpg",
                        "fileSize": 377797,
                        "originalWidth": 2000,
                        "sha256": "6fa9f55ba7f6136fde115d0d2de1e7dbc058be9aefa1221cfb8c025db0dd9e64",
                        "originalDigest": "CB2D958032F72F3DDDD9DF5DDB7D7F5C",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:20:00.499Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -15,
                        "created": "2025-06-01T22:37:13Z",
                        "dof": 4,
                        "emphasis": -22,
                        "harmony": 11,
                        "lighting": -18,
                        "repetition": 6,
                        "rot": 1,
                        "score": 65,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -45
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "456cfc1485534f7e907df7fd9cd62f08",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "df54f3f0bd5b4ff9821c27d5d534c22b"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/d2e0b892512045ffad9de03246f0a7ee"
                }
            },
            "asset": {
                "id": "d2e0b892512045ffad9de03246f0a7ee",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:03.972075Z",
                "updated": "2026-04-23T02:52:49.538775Z",
                "links": {
                    "self": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee"
                    },
                    "/rels/comments": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/53b41d740a30468589fda7af5498835b/renditions/05eaeae37eda75af35a997568074ba73"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/53b41d740a30468589fda7af5498835b/renditions/402e47aa46cb4e6bbd2ff888b0e3e654"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/53b41d740a30468589fda7af5498835b/renditions/95b304630760b41f764f9b9e6dc811d7"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/53b41d740a30468589fda7af5498835b/renditions/b0ac506ffea27a6ca5780d58cdcebdde"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/8d11825f1978f5d77dfddab11cab4729/renditions/8cf50110a15b49f2b636677e0d2b9f05"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/d2e0b892512045ffad9de03246f0a7ee/revisions/8d11825f1978f5d77dfddab11cab4729/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1332,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:55.381Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T17:52:13.097-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1952-002",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Peter N. Weber and dog on McKinley Street at edge of Weber grove, Riverside, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T17:52:13.97-08:00",
                            "ModifyDate": "2025-06-01T15:17:44-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T17:52:13.97-08:00",
                    "importSource": {
                        "originalHeight": 1332,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1952-002.jpg",
                        "fileSize": 372115,
                        "originalWidth": 2000,
                        "sha256": "50cabf0752830c9f34af6781fc6be6857158b5b7f59f3743e10bc6cb300dea90",
                        "originalDigest": "04579DD4CF50B9CAA854448DF8EBA936",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:55.381Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 8,
                        "created": "2025-06-01T22:41:06Z",
                        "dof": 3,
                        "emphasis": -19,
                        "harmony": 17,
                        "lighting": -12,
                        "repetition": 6,
                        "rot": 5,
                        "score": 72,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -43
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "3adf5e88664542ffbf40c1ba317b29a0",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "8bad5cc0576c4faab63673dca58f5902"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/18b1adbdfe43403a9246624af63cae0c"
                }
            },
            "asset": {
                "id": "18b1adbdfe43403a9246624af63cae0c",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.024825Z",
                "updated": "2026-04-23T02:52:49.877139Z",
                "links": {
                    "self": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c"
                    },
                    "/rels/comments": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/df53e73dd7dd4351bca5b850c840b821/renditions/95f34c394d46f78528626acf1506e326"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/df53e73dd7dd4351bca5b850c840b821/renditions/a94a6384411648971ee0a5d4bcbd2df2"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/df53e73dd7dd4351bca5b850c840b821/renditions/cc56416d3e6406d261036f25c9f4473b"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/df53e73dd7dd4351bca5b850c840b821/renditions/b8121685f1abb2b34a2f35680b2cf8f4"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/4dfc755f65855c5dd6850ea26c1362f6/renditions/e3d0ea969ac646b7bea273bd71c5bf5b"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/18b1adbdfe43403a9246624af63cae0c/revisions/4dfc755f65855c5dd6850ea26c1362f6/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1357,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:54.747Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T18:04:12.083-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1950-017",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "First Presbyterian Church, Anaheim, California"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T18:04:12.83-08:00",
                            "ModifyDate": "2025-06-01T15:16:35-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T18:04:12.83-08:00",
                    "importSource": {
                        "originalHeight": 1357,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1950-017.jpg",
                        "fileSize": 444330,
                        "originalWidth": 2000,
                        "sha256": "a84fe7fcee8b17a83900aeefd75d3bb4d0c7c09434f72d19d683a050119c0912",
                        "originalDigest": "F76FB9FE331AD3EF6BC8045716DFEBEF",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:54.747Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 12,
                        "created": "2025-06-01T22:42:00Z",
                        "dof": 14,
                        "emphasis": -12,
                        "harmony": 22,
                        "lighting": 3,
                        "repetition": 7,
                        "rot": 8,
                        "score": 76,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -36
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "36d13f13d516416f83d624553a757bab",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "324f9892c5b84da1aee523d5a076be60"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/a4537de2b5f947c7b2382e461f1fccf3"
                }
            },
            "asset": {
                "id": "a4537de2b5f947c7b2382e461f1fccf3",
                "type": "asset",
                "subtype": "image",
                "created": "2025-06-01T22:20:04.466136Z",
                "updated": "2026-04-23T02:52:49.880528Z",
                "links": {
                    "self": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3"
                    },
                    "/rels/comments": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/db0f9a4a8c0141c9bfff0c07bcb88f44/renditions/8d4f8dba1435358eee90f9fed7172d1d"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/db0f9a4a8c0141c9bfff0c07bcb88f44/renditions/19af5116d92bdb9d77968340dd30f967"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/db0f9a4a8c0141c9bfff0c07bcb88f44/renditions/724372366f39d69a4ae84c8cee3e2bd8"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/db0f9a4a8c0141c9bfff0c07bcb88f44/renditions/b73cef8c83ae80614763519b796d1d46"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/4217cdb5a6423b69a72d71839835e18b/renditions/e1989050e0a5498d84411a1d7fda5797"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/a4537de2b5f947c7b2382e461f1fccf3/revisions/4217cdb5a6423b69a72d71839835e18b/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "croppedWidth": 2000,
                        "croppedHeight": 1353,
                        "device": "Dave’s iMac {57050d77583e2b8199026d41221f9afe9ab0c1ae923e57d837b9c9fb860737e9}",
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "fromDefaults": True,
                        "processingModel": "lightroom",
                        "xmpCameraRaw": {
                            "sha256": "d1edf462323dee105bb20464587ce3cbf54ca827288bc01e1c44f75b0e8ff6a1"
                        }
                    },
                    "userUpdated": "2025-06-01T22:19:55.273Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "photoshop": {
                            "DateCreated": "2024-03-11T18:08:11.019-08:00"
                        },
                        "xmpRights": {
                            "Marked": True,
                            "WebStatement": "oldriverside.org"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1956-007",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user.",
                            "description": "Ridge Cottage Triplex (architect Lloyd Wright), Institute of Mentalphysics, Joshua Tree, Cailfornia"
                        },
                        "xmp": {
                            "CreateDate": "2024-03-11T18:08:11.19-08:00",
                            "ModifyDate": "2025-06-01T15:18:01-07:00"
                        }
                    },
                    "captureDate": "2024-03-11T18:08:11.19-08:00",
                    "importSource": {
                        "originalHeight": 1353,
                        "importTimestamp": "2025-06-01T22:19:54Z",
                        "contentType": "image/jpeg",
                        "fileName": "PJW-PH-California-1956-007.jpg",
                        "fileSize": 408570,
                        "originalWidth": 2000,
                        "sha256": "570deb759161ef7edfa3c2239565f879a1505d388242e0700d17b19de4f6637d",
                        "originalDigest": "942952C6762532928DC92DAC9FA4BCBA",
                        "importedBy": "26373562faa93f6d5bcec06711a88984"
                    },
                    "userCreated": "2025-06-01T22:19:55.273Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -8,
                        "content": -88,
                        "created": "2025-06-01T22:42:20Z",
                        "dof": -13,
                        "emphasis": -54,
                        "harmony": -11,
                        "lighting": -52,
                        "repetition": 5,
                        "rot": -10,
                        "score": 53,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -70
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "aba40535cd884c8da77c0eba13087ba4",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "dd6502908f2b47b2961f1d986cfe6a8c"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/b70806614ccf4439805bd5e34f717109"
                }
            },
            "asset": {
                "id": "b70806614ccf4439805bd5e34f717109",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.715476Z",
                "updated": "2026-04-23T02:52:52.554575Z",
                "links": {
                    "self": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109"
                    },
                    "/rels/comments": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/4f6226e3381844ef83904bbbfd9c5253/renditions/a05d2fe2ac54483015ae531399263cbb"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/4f6226e3381844ef83904bbbfd9c5253/renditions/518d2c04302f71126143fe8551977761"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/4f6226e3381844ef83904bbbfd9c5253/renditions/6497b66e3d137030920bfde91708767e"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/4f6226e3381844ef83904bbbfd9c5253/renditions/2788d1e82e19a3bff02dd77ab3c7a401"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/7b169b25d44b512e7869c48d217cc656/renditions/ea2e8f97e0474689a81cc640494f6bfb"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/b70806614ccf4439805bd5e34f717109/revisions/7b169b25d44b512e7869c48d217cc656/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3689,
                        "fromDefaults": False,
                        "userOrientation": 6,
                        "crsHDREditMode": False,
                        "croppedWidth": 2697,
                        "xmpCameraRaw": {
                            "sha256": "46a69cc9014bac59ef0c49119fd8898fdc5c7db8e2002c7fd46d8a0357087980"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:38:49.572Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "right top"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:50:52.034-07:00",
                            "ModifyDate": "2025-03-28T09:50:52-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:50:52.034-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-016",
                            "description": "Spanish Patio, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:50:52.034-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3895.jpeg",
                        "fileSize": 5195427,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "ce91d65cd993165666a443a4771cd15c828dbbbcf37452d3ee07a439fdc330be",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3895_e87345c7e4504cd59e3bf7a756f9098f.jpeg",
                        "originalDigest": "B2AA0A094860489CE1CACBFFFC4D70E5"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": -4,
                        "created": "2026-04-14T14:38:58Z",
                        "dof": -9,
                        "emphasis": -49,
                        "harmony": 9,
                        "lighting": -23,
                        "repetition": 9,
                        "rot": -1,
                        "score": 56,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -50
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "c3dbfc8f7e914b04a2d5d314c02f5d82",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "b78cb0b4eb3a411ea17d908a0e37ca72"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/a26d65090de44c0a8598a8257fddb9db"
                }
            },
            "asset": {
                "id": "a26d65090de44c0a8598a8257fddb9db",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:02.312758Z",
                "updated": "2026-04-23T02:52:52.420684Z",
                "links": {
                    "self": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db"
                    },
                    "/rels/comments": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/5fb5382fe4fd411eb9cba09dcf8bf8ad/renditions/fa08fdb81248fdaa4439da03df288d4c"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/5fb5382fe4fd411eb9cba09dcf8bf8ad/renditions/4e42026bf16a356bd0227fceb6a49628"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/5fb5382fe4fd411eb9cba09dcf8bf8ad/renditions/11740e555af1a09e35f61975482a6a8c"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/5fb5382fe4fd411eb9cba09dcf8bf8ad/renditions/d471891d83bd02b4a2a06ef9a05d2d79"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/0bcc8f41926750425e4c67956d717fa2/renditions/09a694a75c814f388433944939a9d1f9"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/a26d65090de44c0a8598a8257fddb9db/revisions/0bcc8f41926750425e4c67956d717fa2/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3516,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2703,
                        "xmpCameraRaw": {
                            "sha256": "7bcb1152941fa4ec4078b8ba37f597f1af6abd85a99d1c8384046c246bf3d8e9"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:38:44.287Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:51:07.736-07:00",
                            "ModifyDate": "2025-03-28T09:51:07-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:51:07.736-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-015",
                            "description": "Anton Clock and Carrie Jacobs Bond Suite, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:51:07.736-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3896.jpeg",
                        "fileSize": 4926673,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "caf09674816b169660b0276ca16165bb935750a2c55639257258d808249eeaab",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3896_a2139528a7bd4dfd93dcaf84b436d5d7.jpeg",
                        "originalDigest": "97ABBF91E6965A37614AFF1AA87DAFE6"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -3,
                        "content": -27,
                        "created": "2026-04-14T14:38:56Z",
                        "dof": -15,
                        "emphasis": -44,
                        "harmony": -15,
                        "lighting": -62,
                        "repetition": 4,
                        "rot": -7,
                        "score": 41,
                        "symmetry": 1,
                        "version": 1,
                        "vivid": -63
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "7a2d682f8a2348ac93af8b537cd3c676",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "752d120f5efc4c67a3b58df1c62ceaaf"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/57eb6b66b72348a59d8e3255f6e356a2"
                }
            },
            "asset": {
                "id": "57eb6b66b72348a59d8e3255f6e356a2",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.590534Z",
                "updated": "2026-04-23T02:52:56.744832Z",
                "links": {
                    "self": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2"
                    },
                    "/rels/comments": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/175a08a4599c4802890dd345d3e21d69/renditions/1932e128bb291c5b50e651212b3f3542"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/175a08a4599c4802890dd345d3e21d69/renditions/1db8767a33ac46d60412074f076002a4"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/175a08a4599c4802890dd345d3e21d69/renditions/0619a3d7787fc870144d1eeedba15367"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/175a08a4599c4802890dd345d3e21d69/renditions/877e2638ac8c98ea8169ea0ffd18c070"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/04c9b8d25ddf5a752412a8f6b595b057/renditions/150aa53115a64c60931139aea805829f"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/57eb6b66b72348a59d8e3255f6e356a2/revisions/04c9b8d25ddf5a752412a8f6b595b057/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3288,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2432,
                        "xmpCameraRaw": {
                            "sha256": "354edfd5b76c40c64e34152567c488f26d25b73f6b4ec090c2428cc98ff1b507"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:38:40.586Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:51:17.324-07:00",
                            "ModifyDate": "2025-03-28T09:51:17-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:51:17.324-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-014",
                            "description": "Las Salas de los Escritorios (Authors’ Row) from the Court of the Bells, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:51:17.324-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3897.jpeg",
                        "fileSize": 4657433,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "983cd6822375636469facc463ce69bace27200b6882d03323052de3cda8343a3",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3897_2831298967a546e5a3a53938552f6585.jpeg",
                        "originalDigest": "1B9CDCF4B164F7CE8CB99D8758735E96"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -1,
                        "content": -34,
                        "created": "2026-04-14T14:38:47Z",
                        "dof": -11,
                        "emphasis": -55,
                        "harmony": 1,
                        "lighting": -38,
                        "repetition": 6,
                        "rot": -3,
                        "score": 54,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -58
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "c96eda7be5614effacb22f9f06b847ab",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "dd568551751c4d90915e5c72578c9044"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/a75efdaa960c40f9a66cde69c04a8fd9"
                }
            },
            "asset": {
                "id": "a75efdaa960c40f9a66cde69c04a8fd9",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:02.269064Z",
                "updated": "2026-04-23T02:52:52.609140Z",
                "links": {
                    "self": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9"
                    },
                    "/rels/comments": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d5ce642a0212874b6b2b5d41b75eee3e/renditions/2a1214540c585cd2e9ea29f6f578ae45"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d5ce642a0212874b6b2b5d41b75eee3e/renditions/df091155a25d02427f52510469b3db5c"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d5ce642a0212874b6b2b5d41b75eee3e/renditions/8dc78710d7d5236ffa76dc60f16bfa69"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d5ce642a0212874b6b2b5d41b75eee3e/renditions/642dfaa926b8ac08d5c8b897b0827c8b"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d4a04f574192f41013ae101755fc48b2/renditions/4bb880cb397d44f9b138a95bfdb967d1"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/a75efdaa960c40f9a66cde69c04a8fd9/revisions/d4a04f574192f41013ae101755fc48b2/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3535,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2658,
                        "xmpCameraRaw": {
                            "sha256": "43aa748c43fa749b1b9440a1d06058b46d14c67426610f6d8333275e48cd7e04"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:38:33.617Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:51:44.485-07:00",
                            "ModifyDate": "2025-03-28T09:51:44-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:51:44.485-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-013",
                            "description": "Alhambra Suite and Carmel Dome, Mission Inn, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:51:44.485-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3900.jpeg",
                        "fileSize": 4152293,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "f108d7c0f4e5964fa5448abb4668e1040fb6a4992f13f92b980226ada6617220",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3900_bfdfdd55d6f84def9cbd8027343dba1d.jpeg",
                        "originalDigest": "C230534F24922140E07E9E42AE355710"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 6,
                        "content": 21,
                        "created": "2026-04-14T14:38:41Z",
                        "dof": 0,
                        "emphasis": 8,
                        "harmony": 15,
                        "lighting": -16,
                        "repetition": 6,
                        "rot": 2,
                        "score": 66,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -45
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "80e904782475474f88fc3bf09468e67a",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "c9f3d6d5b87b471097bc6d16732b6b18"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/c57198b4f54d4ebeaa12df61223c3030"
                }
            },
            "asset": {
                "id": "c57198b4f54d4ebeaa12df61223c3030",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.411547Z",
                "updated": "2026-04-23T02:52:55.872632Z",
                "links": {
                    "self": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030"
                    },
                    "/rels/comments": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/a20f87cc9d3f0654989c315508c4a1be/renditions/3976e1eac92c7fbab4a3d23cf24cb83b"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/a20f87cc9d3f0654989c315508c4a1be/renditions/966d2c7c1faf20cc03fbcaec8f1d4b78"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/a20f87cc9d3f0654989c315508c4a1be/renditions/a5b6b278d9d31aa062c9764c11d34fdc"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/a20f87cc9d3f0654989c315508c4a1be/renditions/6852e2acc00f15f31533abf29c0c55ca"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/3f102e9e41d998b41dd57d24c7b6e107/renditions/dfaf3822fa2244848f9a34a17a6775c6"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/c57198b4f54d4ebeaa12df61223c3030/revisions/3f102e9e41d998b41dd57d24c7b6e107/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3448,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2535,
                        "xmpCameraRaw": {
                            "sha256": "33c2e91f9618fde75c35705f500ccf001a3db030bcc2bf072b75a4b911f65061"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:40:13.271Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:51:55.34-07:00",
                            "ModifyDate": "2025-03-28T09:51:55-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:51:55.34-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-012",
                            "description": "Alhambra Suite and Carmel Dome, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:51:55.340-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3901.jpeg",
                        "fileSize": 4476873,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "b140780d957768521de86fcc5dff674598b411d87b0213bb146c12165890777e",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3901_d0cf255db45848dd859107d6570ec41f.jpeg",
                        "originalDigest": "8DABB62D2E48DB5A8A4CABCBB7E73A5C"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 5,
                        "content": 18,
                        "created": "2026-04-14T14:40:20Z",
                        "dof": 0,
                        "emphasis": 25,
                        "harmony": 11,
                        "lighting": -28,
                        "repetition": 4,
                        "rot": 0,
                        "score": 65,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "f5ffa282702b4f839cb367711c5514e9",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "ea163df51ccf4afbb2b1156448cc348f"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/eeeb445fb7d14f129e55968be26da50e"
                }
            },
            "asset": {
                "id": "eeeb445fb7d14f129e55968be26da50e",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.377058Z",
                "updated": "2026-04-23T02:52:52.853118Z",
                "links": {
                    "self": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e"
                    },
                    "/rels/comments": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/db20790ee5ec7a7acde530252c1dda59/renditions/2cc50a2c635bb77c6b5c29e7816ba237"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/db20790ee5ec7a7acde530252c1dda59/renditions/c41432deb0167340fa0d010b61cb76c0"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/db20790ee5ec7a7acde530252c1dda59/renditions/0a0fae4711229f91201ec928ee58c374"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/db20790ee5ec7a7acde530252c1dda59/renditions/bfc7094af5b2b3a24f1e40fd80f11bef"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/b118917f961ea9e495a25d057a206e20/renditions/cf40a3f1e1574d93902d3ef90db7ad90"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/eeeb445fb7d14f129e55968be26da50e/revisions/b118917f961ea9e495a25d057a206e20/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3763,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2561,
                        "xmpCameraRaw": {
                            "sha256": "a2048b863f8b30ae4323f998a59c3910177e96887d062ad503088543a1ccd664"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:41:03.028Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:53:12.826-07:00",
                            "ModifyDate": "2025-03-28T09:53:12-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:53:12.826-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-011",
                            "description": "Spanish Patio, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:53:12.826-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3903.jpeg",
                        "fileSize": 4426757,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "cf3b0cec84802e1ca5f1b13fcdfbe5a39474488f7ab31d27145412d83327934a",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3903_bebf027813d543af9624f056390406fe.jpeg",
                        "originalDigest": "831DA577F45E1E947B5E9BEC93C6E8E7"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -5,
                        "content": -51,
                        "created": "2026-04-14T14:41:09Z",
                        "dof": -6,
                        "emphasis": -57,
                        "harmony": -11,
                        "lighting": -55,
                        "repetition": 2,
                        "rot": -5,
                        "score": 49,
                        "symmetry": 0,
                        "version": 1,
                        "vivid": -64
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "530c521014954063ab28970bfad7da1d",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "37e77f600a314ce2b0aba0429ddb90d3"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/94b94be62a4048faa8895fc252dd8237"
                }
            },
            "asset": {
                "id": "94b94be62a4048faa8895fc252dd8237",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.771276Z",
                "updated": "2026-04-23T02:52:52.976429Z",
                "links": {
                    "self": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237"
                    },
                    "/rels/comments": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/c8a3e1226d21babd4f749b6d6d9f8cf1/renditions/22d42c540f8ff39d7ee83030ccb46da7"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/c8a3e1226d21babd4f749b6d6d9f8cf1/renditions/fb477407f228addc0833c96c15582195"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/c8a3e1226d21babd4f749b6d6d9f8cf1/renditions/cb738f63ef4a832424fefcaa33a4c4f9"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/c8a3e1226d21babd4f749b6d6d9f8cf1/renditions/e7f4acdea296b1c256b1284b16b9dc24"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/3855261fbfab21569797cca0515c1538/renditions/6e1da91258cb46f4bb884f4efdec4195"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/94b94be62a4048faa8895fc252dd8237/revisions/3855261fbfab21569797cca0515c1538/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3784,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2418,
                        "xmpCameraRaw": {
                            "sha256": "fd0b1b7517c5899c966cf82128d09ddd1ee811a7bb34659c11cf4ab8d49e1119"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:42:03.331Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:53:23.603-07:00",
                            "ModifyDate": "2025-03-28T09:53:23-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:53:23.603-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-010",
                            "description": "Old Adobe, Campanario, and Carillon Tower, Mission Inn, Riverside, California ",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:53:23.603-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3904.jpeg",
                        "fileSize": 4339036,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "b95b3114f7ecf2d60ffe4d71833c9d75610176a73f6433c013d00ffc5fe8fe60",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3904_6ea1f9a93bdb4f3f9fc1c05a9aa7100b.jpeg",
                        "originalDigest": "BBA7B30BED720E7ADAA3A73F9F2FDAAB"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -2,
                        "content": -41,
                        "created": "2026-04-14T14:42:10Z",
                        "dof": -12,
                        "emphasis": -57,
                        "harmony": -7,
                        "lighting": -50,
                        "repetition": 5,
                        "rot": -4,
                        "score": 52,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -64
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "4749ea9ce9634a41b04a143224e52b3b",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "cd7a5c44a87341dd9fde9cfa08e6135b"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/e5083780173a4f4eb63f9a46e6e66c0f"
                }
            },
            "asset": {
                "id": "e5083780173a4f4eb63f9a46e6e66c0f",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.449504Z",
                "updated": "2026-04-23T02:52:53.042856Z",
                "links": {
                    "self": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f"
                    },
                    "/rels/comments": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/ac58c368a0cd7faec82a213ca174b6b6/renditions/0cf7f562a5c276bd8b7f6b6ab2af4e1c"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/ac58c368a0cd7faec82a213ca174b6b6/renditions/b5db1011fc5e83917be6a5f66e758cf0"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/ac58c368a0cd7faec82a213ca174b6b6/renditions/c965456f5b5e993ed908e9ae07d01c02"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/ac58c368a0cd7faec82a213ca174b6b6/renditions/b49c76a59866b287010884dd947dc676"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/2014b669468b839478ea1d82044fce55/renditions/1abbc4f7d63a41db9c9266442a0d6751"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/e5083780173a4f4eb63f9a46e6e66c0f/revisions/2014b669468b839478ea1d82044fce55/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3684,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2950,
                        "xmpCameraRaw": {
                            "sha256": "fc5c1f3af96e3fd0affcdefddf279e4d39f5e3ef94d99c2eaaca7240ed3d4131"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:43:14.355Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:53:36.043-07:00",
                            "ModifyDate": "2025-03-28T09:53:36-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:53:36.043-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-009",
                            "description": "Spanish Wing and Frank Miller Suite, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:53:36.043-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3905.jpeg",
                        "fileSize": 4596128,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "6be21da0afb086fe6c62feb62572f70dec02afaf5e4a6461d6bebb66ed059bcd",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3905_89dddfe195094342bb8c76fd878b0912.jpeg",
                        "originalDigest": "99404B89B4D33224E41109193E8CEEC6"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -17,
                        "created": "2026-04-14T14:43:21Z",
                        "dof": -6,
                        "emphasis": -20,
                        "harmony": 1,
                        "lighting": -30,
                        "repetition": 7,
                        "rot": -4,
                        "score": 57,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -51
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "26656c517f514925b0459893679e93dd",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "0b0ddf21db8b48a58c1e4a7ad2aad484"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/7b8d37cb8210416da1c8ec631ad60eb1"
                }
            },
            "asset": {
                "id": "7b8d37cb8210416da1c8ec631ad60eb1",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.401716Z",
                "updated": "2026-04-23T02:52:53.332510Z",
                "links": {
                    "self": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1"
                    },
                    "/rels/comments": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/06a7a6a3089cd9bc8bf65dc43e2a740d/renditions/81f669e8f3088eb4eab66926a0e7f944"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/06a7a6a3089cd9bc8bf65dc43e2a740d/renditions/18e02795d5d53b8d712815b105aed48e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/06a7a6a3089cd9bc8bf65dc43e2a740d/renditions/cfd873f95f541de6a735070bfd4837aa"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/06a7a6a3089cd9bc8bf65dc43e2a740d/renditions/a69ee3c00b034abccde9d81f9a74589a"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/32a450a4b2bc28de6f8dd2beef6c6a75/renditions/9c913e423dae4b139927de3c825d8ab6"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/7b8d37cb8210416da1c8ec631ad60eb1/revisions/32a450a4b2bc28de6f8dd2beef6c6a75/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3662,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2724,
                        "xmpCameraRaw": {
                            "sha256": "cb0c34cf9b1d3181488610ebd49f38138fac9799cdd24afd19d74fe111623a5f"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:44:11.042Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:53:58.282-07:00",
                            "ModifyDate": "2025-03-28T09:53:58-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:53:58.282-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-008",
                            "description": "Carrie Jacobs Bond Suite, Las Salas de los Escritorios (Authors’ Row), Mission Inn, California ",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:53:58.282-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3906.jpeg",
                        "fileSize": 4443673,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "4ec7ca4f086eb1d6894c406232e837bf476a586112060f27362a4e43dbd3eb63",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3906_7c51049f431946b083c45b05b039542c.jpeg",
                        "originalDigest": "E16CCA27F33A0E2AD86566557B75F22B"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -19,
                        "created": "2026-04-14T14:44:17Z",
                        "dof": -10,
                        "emphasis": -29,
                        "harmony": 2,
                        "lighting": -36,
                        "repetition": 5,
                        "rot": -3,
                        "score": 52,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -51
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "dee1ca573ff040789c06eb731c0312ac",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "419132b18d1b4fadb6e3a9ad34074d2c"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/d4d744ce6070457093f6c2d17f5e5c8b"
                }
            },
            "asset": {
                "id": "d4d744ce6070457093f6c2d17f5e5c8b",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.749066Z",
                "updated": "2026-04-23T02:52:53.451813Z",
                "links": {
                    "self": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b"
                    },
                    "/rels/comments": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/3a7940d66c1e368c9a289f6d8462ff6a/renditions/006933d29367be7ace43c99487b17e44"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/3a7940d66c1e368c9a289f6d8462ff6a/renditions/5a579fa0f889a86da029b39b967b6e26"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/3a7940d66c1e368c9a289f6d8462ff6a/renditions/e1e25cd7ec01f3a2e508b547a141200a"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/3a7940d66c1e368c9a289f6d8462ff6a/renditions/3a6f4b6c5ebe41fc8e1965ee49d8c812"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/9b95e656f6c7e672911d4259c686b5e5/renditions/2b3a303c2bdd4ab2924395ab02e0a5fa"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/d4d744ce6070457093f6c2d17f5e5c8b/revisions/9b95e656f6c7e672911d4259c686b5e5/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3809,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2984,
                        "xmpCameraRaw": {
                            "sha256": "d5730bd2aa7f1b3f30f9dcdc4fa5e72ef9993bc3201e5cd99e08ecaadce9a6ff"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:44:57.324Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:54:11.805-07:00",
                            "ModifyDate": "2025-03-28T09:54:11-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:54:11.805-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-007",
                            "description": "Spanish Patio, Mission Inn, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:54:11.805-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3907.jpeg",
                        "fileSize": 4260019,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "d76a5dbe545e218faa69e23d25be1c7cfeaee5ab71c7efbd9732b328b2ffe787",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3907_b2211d27213f434f86e5102876b659ec.jpeg",
                        "originalDigest": "2FB05B2574BA0E08C658B273717B967F"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": 3,
                        "created": "2026-04-14T14:45:04Z",
                        "dof": -4,
                        "emphasis": -12,
                        "harmony": 3,
                        "lighting": -27,
                        "repetition": 6,
                        "rot": 0,
                        "score": 62,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "925fda2a5fdb413aaa8b46520f2f2850",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "1baa3f89b5e640e0937c493a262216b9"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/fc3b072f926b49a5a63da11cbeae9636"
                }
            },
            "asset": {
                "id": "fc3b072f926b49a5a63da11cbeae9636",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.707485Z",
                "updated": "2026-04-23T02:52:55.084625Z",
                "links": {
                    "self": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636"
                    },
                    "/rels/comments": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/69da4b5f80973566fcb0818250b174c2/renditions/87da1022a0ddbb520d4b52152ed30be7"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/69da4b5f80973566fcb0818250b174c2/renditions/47753d34b239818fe5e2d9016561f971"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/69da4b5f80973566fcb0818250b174c2/renditions/3717cc085113ef0a8add69a14d744317"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/69da4b5f80973566fcb0818250b174c2/renditions/6d765206c0f46d4513900b6baceb89ab"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/b199e22c3be1884c5f4fe4f2e1ebfb2b/renditions/7eb856efe6a840829e6117e49e797700"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/fc3b072f926b49a5a63da11cbeae9636/revisions/b199e22c3be1884c5f4fe4f2e1ebfb2b/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3972,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 3084,
                        "xmpCameraRaw": {
                            "sha256": "e37e3587bfb1713dcaf88ef322fc26cfc8b5c303c733952b628a63cc9ce8263f"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:45:39.590Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:54:28.078-07:00",
                            "ModifyDate": "2025-03-28T09:54:28-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:54:28.078-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-006",
                            "description": "East courtyard, Soldiers’ Memorial and Municipal Auditorium Building, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:54:28.078-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3908.jpeg",
                        "fileSize": 5649825,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "fccaf8460c702d8020ce27532254e9c4eb8cd89bed368994eed7aa2ed9bf0052",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3908_9a452921dbf04c389de901e8507a4f00.jpeg",
                        "originalDigest": "B8CBBEFEB72EBAB7846F8ED2F7FDEB89"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -27,
                        "created": "2026-04-14T14:45:48Z",
                        "dof": -7,
                        "emphasis": -57,
                        "harmony": 8,
                        "lighting": -28,
                        "repetition": 7,
                        "rot": 0,
                        "score": 61,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -51
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "0230b2e90a7d49eca81912b0cf4ca5d6",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "e3c0be4ea0f740e5ab2de983a94b166e"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/3ce6ebe189ec4cfbafb2082aa4988f40"
                }
            },
            "asset": {
                "id": "3ce6ebe189ec4cfbafb2082aa4988f40",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:02.296542Z",
                "updated": "2026-04-23T02:52:53.921426Z",
                "links": {
                    "self": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40"
                    },
                    "/rels/comments": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/e30eb96b894dfe70a49952bdbc3a4852/renditions/b872688f2f03f6d4f474dca7022cef3b"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/e30eb96b894dfe70a49952bdbc3a4852/renditions/a26a8862eb188fe808ae457ff1186074"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/e30eb96b894dfe70a49952bdbc3a4852/renditions/0a82ea57020a85b6edd5fb623e76f8a7"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/e30eb96b894dfe70a49952bdbc3a4852/renditions/fb6e3b726a383931c4dffcee71782d76"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/aa86b6623f5b6fb1e8d1be712df3369f/renditions/870e6c6f43234d189f6a6120049eefca"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/3ce6ebe189ec4cfbafb2082aa4988f40/revisions/aa86b6623f5b6fb1e8d1be712df3369f/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3869,
                        "fromDefaults": False,
                        "userOrientation": 6,
                        "crsHDREditMode": False,
                        "croppedWidth": 2781,
                        "xmpCameraRaw": {
                            "sha256": "c069e806d1addc059d696ccad840d9e1bc901f45512e11423cc8323b50c5d620"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:46:38.520Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "right top"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:54:51.862-07:00",
                            "ModifyDate": "2025-03-28T09:54:51-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:54:51.862-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-005",
                            "description": "East steps of Soldiers’ Memorial and Municipal Auditorium Building, Riverside, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:54:51.862-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3909.jpeg",
                        "fileSize": 5433537,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "1615f1efccc50341ac154a894119dfcdf991f69afcc3567f765e1a090621f5d2",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3909_105efa3985bb452ab7412c5973117847.jpeg",
                        "originalDigest": "48B9CB379A90C3B96516B8AA99E48DD9"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -15,
                        "created": "2026-04-14T14:46:45Z",
                        "dof": -4,
                        "emphasis": -45,
                        "harmony": 13,
                        "lighting": -14,
                        "repetition": 7,
                        "rot": 0,
                        "score": 61,
                        "symmetry": 2,
                        "version": 1,
                        "vivid": -38
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "75bd20bb637c40478adde207dd2a5cbc",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "e3d1fb4f762043ae8405242de561e0b6"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/a254c492658c425a9982cbb4952512cf"
                }
            },
            "asset": {
                "id": "a254c492658c425a9982cbb4952512cf",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:02.299055Z",
                "updated": "2026-04-23T02:52:54.302497Z",
                "links": {
                    "self": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf"
                    },
                    "/rels/comments": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/242ba39f5a695cebc5419db73eaa7681/renditions/16871cb890a0fb6caa8b319377fe9cbb"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/242ba39f5a695cebc5419db73eaa7681/renditions/01626d04a404bee1fc7172f1427f7bc4"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/242ba39f5a695cebc5419db73eaa7681/renditions/00a5c8811bca19b723023e28013cafc7"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/242ba39f5a695cebc5419db73eaa7681/renditions/76599ddbf80411ad3975482ef9e4003a"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/2ac0a4b909403fd0873ce00c31c6e384/renditions/b950007d4c94428886fef70606431599"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/a254c492658c425a9982cbb4952512cf/revisions/2ac0a4b909403fd0873ce00c31c6e384/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3886,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2782,
                        "xmpCameraRaw": {
                            "sha256": "8f0146103d48cdbaa4fe5ce4ffe5b50f0151b0dfeba05dc8438f4227c2cbc5ab"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:47:25.167Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:55:10.711-07:00",
                            "ModifyDate": "2025-03-28T09:55:10-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:55:10.711-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-004",
                            "description": "Court of the Bells and Cloister Wing, Mission Inn, California",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:55:10.711-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3910.jpeg",
                        "fileSize": 5006162,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "142dff4fc89e6c5713aa31b41a62d69a91f384f3fd4a3aa5b35a25b2f82d8671",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3910_3b1b7434bb3c4f168ea34d4434456bde.jpeg",
                        "originalDigest": "B70F278879F28975E1E5BFC46813B13B"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 0,
                        "content": -16,
                        "created": "2026-04-14T14:47:33Z",
                        "dof": -4,
                        "emphasis": -41,
                        "harmony": 5,
                        "lighting": -24,
                        "repetition": 8,
                        "rot": -2,
                        "score": 60,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -54
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "37ec6a1e218f4e3196fd0b9737e22907",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "73f0f358b9934762a624ee21f53ca545"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/cd6aeed69fc046b2a3aca577febdb03e"
                }
            },
            "asset": {
                "id": "cd6aeed69fc046b2a3aca577febdb03e",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:06.725365Z",
                "updated": "2026-04-23T02:52:54.044982Z",
                "links": {
                    "self": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e"
                    },
                    "/rels/comments": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/0afdfb0e45b757ebd05d619aa6bed75c/renditions/754eac2a59b6b7e189d58ecc49b4c829"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/0afdfb0e45b757ebd05d619aa6bed75c/renditions/4a6ae1a99bc053e8aa4823f709372433"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/0afdfb0e45b757ebd05d619aa6bed75c/renditions/d313aa364881f8801c6d0bd8b29d4fea"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/0afdfb0e45b757ebd05d619aa6bed75c/renditions/c46d924c000e5d2110ebb3a46b6ca08c"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/5bd4a428e5909d310566c9baf0a8cda1/renditions/cebca33be3a94eebbc210cafbdfcb592"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/cd6aeed69fc046b2a3aca577febdb03e/revisions/5bd4a428e5909d310566c9baf0a8cda1/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3625,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2644,
                        "xmpCameraRaw": {
                            "sha256": "2a4ed31f25262cd925fd6fe2e0dc7bc5a33f7fcfbcf9e68aebd2e8a91d917271"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:48:20.776Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:55:24.021-07:00",
                            "ModifyDate": "2025-03-28T09:55:24-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:55:24.021-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-003",
                            "description": "Carillon Tower and Spanish Courtyard, Mission Inn, Riverside, California ",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:55:24.021-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3911.jpeg",
                        "fileSize": 4809337,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "50504454b749ee2a290ea842ddd6c7f13b68b5bfc4c10e646b343f38cbea3222",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3911_08375d00b6da412b8e16cf66fec12b0b.jpeg",
                        "originalDigest": "FC1E9180504079221BD6FE1C9F74C8A1"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 3,
                        "content": 1,
                        "created": "2026-04-14T14:48:28Z",
                        "dof": -7,
                        "emphasis": -37,
                        "harmony": 9,
                        "lighting": -18,
                        "repetition": 11,
                        "rot": 0,
                        "score": 59,
                        "symmetry": 4,
                        "version": 1,
                        "vivid": -49
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "c1c307a381344846bf316105eea2e413",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "484737b5e9d94a64adbb77e22ce70edc"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/873b2ab6550f40a9a976896995894c1e"
                }
            },
            "asset": {
                "id": "873b2ab6550f40a9a976896995894c1e",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.437962Z",
                "updated": "2026-04-23T02:52:54.506163Z",
                "links": {
                    "self": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e"
                    },
                    "/rels/comments": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/f372a5f1ae8a83914a7226f2869fea77/renditions/902e83a73fba8faa0ad10c79490219b9"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/f372a5f1ae8a83914a7226f2869fea77/renditions/71f3c67124de2e40af63c2f338d9f46e"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/f372a5f1ae8a83914a7226f2869fea77/renditions/b3cd69c0bab3f6b8bfc8ba1f1fa09dca"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/f372a5f1ae8a83914a7226f2869fea77/renditions/6bcb74870c71903123b01c614b8ab998"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/9975b9368c9e73ef21d105e8fe28a719/renditions/bbf947912a534b479b2a6a9f9d268ee3"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/873b2ab6550f40a9a976896995894c1e/revisions/9975b9368c9e73ef21d105e8fe28a719/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3884,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2859,
                        "xmpCameraRaw": {
                            "sha256": "0640a47546eeb0b3fd8ff1bd3ccf4c1fa122a10b45885b57637bf94885dc6247"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:49:33.704Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:55:41.39-07:00",
                            "ModifyDate": "2025-03-28T09:55:41-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:55:41.39-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-002",
                            "description": "Las Salas de Los Escritorios (Authors’ Row), Mission Inn, Riverside, California ",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:55:41.390-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3912.jpeg",
                        "fileSize": 5163323,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "9c04e009f02da9b1d3f49735c8ca232d486f714db8450fa14930aecfff6f0d32",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3912_04412f19938a4f2d851d8145997de806.jpeg",
                        "originalDigest": "0633EA5518EFE958498884F03012B534"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": -2,
                        "content": -34,
                        "created": "2026-04-14T14:49:43Z",
                        "dof": -4,
                        "emphasis": -39,
                        "harmony": -2,
                        "lighting": -33,
                        "repetition": 8,
                        "rot": -4,
                        "score": 56,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        },
        {
            "id": "8807cda3ad844620a8895540b91bba99",
            "type": "album_asset",
            "created": "0000-00-00T00:00:00",
            "updated": "0000-00-00T00:00:00",
            "revision_ids": [
                "c2a85c05df5e428d92d662b0bd030462"
            ],
            "links": {
                "self": {
                    "href": "albums/e5e6ad020f7f4c34963ceebb91d95d12/assets/83ea6a41caa74436a32c3b9b4bd3eafc"
                }
            },
            "asset": {
                "id": "83ea6a41caa74436a32c3b9b4bd3eafc",
                "type": "asset",
                "subtype": "image",
                "created": "2026-04-13T16:36:10.416176Z",
                "updated": "2026-04-23T02:52:54.646254Z",
                "links": {
                    "self": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc"
                    },
                    "/rels/comments": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/comments",
                        "count": 0
                    },
                    "/rels/favorites": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/favorites",
                        "count": 0
                    },
                    "/rels/rendition_type/2048": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/88e38b73b168e132bdff7deafdd961ec/renditions/35a4c9386d376f2db3df35fd0c9ab99c"
                    },
                    "/rels/rendition_type/1280": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/88e38b73b168e132bdff7deafdd961ec/renditions/62447142f463d21da268a5fb49f5b610"
                    },
                    "/rels/rendition_type/640": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/88e38b73b168e132bdff7deafdd961ec/renditions/27e5694bfeb106ee822b518e093f482b"
                    },
                    "/rels/rendition_type/thumbnail2x": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/88e38b73b168e132bdff7deafdd961ec/renditions/8eac6fca137f9a3220feaa29fa5e4abc"
                    },
                    "/rels/rendition_type/fullsize": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/e350bfe0f0d2087acfbe33c3f4e80a50/renditions/8bfd05e57eac4dee816fa23f24591137"
                    },
                    "/rels/rendition_generate/fullsize": {
                        "href": "assets/83ea6a41caa74436a32c3b9b4bd3eafc/revisions/e350bfe0f0d2087acfbe33c3f4e80a50/renditions/{rendition_id}?rendition_type=fullsize",
                        "templated": True
                    }
                },
                "payload": {
                    "develop": {
                        "processingModel": "lightroom",
                        "croppedHeight": 3643,
                        "fromDefaults": False,
                        "userOrientation": 1,
                        "crsHDREditMode": False,
                        "croppedWidth": 2877,
                        "xmpCameraRaw": {
                            "sha256": "77de7cd2ce98124e8ff24edd627d56b3040bb6eeb025e8baf09f47d108a847cd"
                        },
                        "device": "iPhone {952db76491c358b7e9ae301c57c6402c23590a315b3e8f3d149433b0759a8512}"
                    },
                    "userUpdated": "2026-04-14T14:50:22.502Z",
                    "xmp": {
                        "tiff": {
                            "Orientation": "top left"
                        },
                        "xmp": {
                            "CreateDate": "2025-03-28T09:56:01.116-07:00",
                            "ModifyDate": "2025-03-28T09:56:01-07:00"
                        },
                        "photoshop": {
                            "DateCreated": "2025-03-28T09:56:01.116-07:00"
                        },
                        "dc": {
                            "title": "PJW-PH-California-1928-001",
                            "description": "Cloister Wing, Mission Inn, Riverside CA",
                            "rights": "Copyrighted. Rights are owned by Old Riverside Foundation. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."
                        }
                    },
                    "captureDate": "2025-03-28T09:56:01.116-07:00",
                    "importSource": {
                        "originalHeight": 5712,
                        "importTimestamp": "2026-04-13T16:35:56.764Z",
                        "contentType": "image/jpeg",
                        "fileName": "IMG_3913.jpeg",
                        "fileSize": 6348845,
                        "importedBy": "26373562faa93f6d5bcec06711a88984",
                        "originalWidth": 4284,
                        "sha256": "07a2c87f52b8fe3b170e07070b27f3f4cab4169f7a925815aa94573188656ca6",
                        "localAssetId": "file:///private/var/mobile/Containers/Shared/AppGroup/2BFB17AB-D42F-45EF-93AA-127C40885CBA/ShareExtension/IMG_3913_7ad35790f5a2477a95ac9a5d2ab77c47.jpeg",
                        "originalDigest": "F1A48D03C31F63BCF325FC02B73E5409"
                    },
                    "userCreated": "2026-04-13T16:35:56.764Z",
                    "aesthetics": {
                        "application": "ias",
                        "balancing": 2,
                        "content": -7,
                        "created": "2026-04-14T14:50:31Z",
                        "dof": -5,
                        "emphasis": -33,
                        "harmony": 9,
                        "lighting": -23,
                        "repetition": 8,
                        "rot": 0,
                        "score": 62,
                        "symmetry": 3,
                        "version": 1,
                        "vivid": -52
                    }
                }
            },
            "payload": {
                "userCreated": "2026-04-22T00:31:30.243Z",
                "userUpdated": "2026-04-22T00:31:30.243Z"
            }
        }
    ]
}

