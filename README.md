# geodata - WIP

I wanted to explore working with geospatial data and learning how to work with this field's specialized datatypes. This is a small data ingestion service to extract data from a GeoTIFF, process it, then load it into a PostgreSQL database. 

The data source I've used is the "H12482: NOS Hydrographic Survey, Eastern Long Island Sound, 2013-04-20" from data.gov.

## Setup
Be sure you have a ```database.ini``` with the correct info to initialize the database. It should look something like this:
```
[postgresql]
host=localhost
database=geodata
user=postgres
password=postgres
```

The service uses PostgreSQL, so be sure you have PostgreSQL and PostGIS installed so the geographic objects are supported in the database.

The ```dataset``` directory should contain the ```H12482.tiff``` image to be processed. I plan to remove the hardcoded image and make this a parameter at a later date to try with other images.

## Running The Code
To run, simply run ```python3 geodata_ingestion.py```. This script will read the raw GeoTIFF data, examine the grid point image coordinates, translate them to geographic coordinates (EPSG:32618), and retrieve the depth data from each point. Then, it will create an instance of the GeodataDB, create a table with the name of the survey, and load the data into the database.

### Note:
As there are easily over a million data points to process, this will take a fairly long time to run (on my machine it takes about 20-30 minutes). I will continue to optimize in the future.

## Future Goals
Other features I plan to add:

    - Creating a 3D model of the ocean floor from the depth and coordinate data
    - Multithreaded geometry processing
    - Support for multiple images
    - Comparison tools
