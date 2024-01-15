import psycopg2
from psycopg2 import sql
import pandas as pd
import requests


t_host = "localhost" # either "localhost", a domain name, or an IP address.
t_port = "5435" # default postgres port
t_dbname = "postgres"
t_user = "postgres"
t_pw = "postgres"

input_data = None

with psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(t_host, t_port, t_dbname, t_user, t_pw)) as conn:
    
    query = '''SELECT id, geom, siren, siret, statutdiffusionetablissement, libellevoieetablissement, libellecommuneetablissement, 
                        NULLIF(denominationusuelleetablissement, '[ND]') as denominationusuelleetablissement,
                        NULLIF(enseigne1etablissement, '[ND]') as enseigne1etablissement,
                        NULLIF(enseigne2etablissement, '[ND]') as enseigne2etablissement,
                        NULLIF(enseigne3etablissement, '[ND]') as enseigne3etablissement,
                        ST_X(ST_GeomFromEWKT(geom)) as geom_x,
                        ST_Y(ST_GeomFromEWKT(geom)) as geom_y
                       FROM siren.siren_archis;'''
    input_data = pd.read_sql_query(query, conn)
    
for data in input_data:

    json_post_data = {
                        "includedTypes": ["restaurant"],
                        "maxResultCount": 3,
                        "locationRestriction": {
                            "circle": {
                            "center": {
                                "latitude": input_data.geom_x,
                                "longitude": input_data.geom_y},
                            "radius": 500.0
                            }
                        }
                    }


curl -X POST -d  \
-H 'Content-Type: application/json' -H "X-Goog-Api-Key: YOUR_GOOGLE_API_TOKEN" \
-H "X-Goog-FieldMask: places.displayName" \
https://places.googleapis.com/v1/places:searchNearby
