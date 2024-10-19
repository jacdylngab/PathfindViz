# List of cities 
cities = [
    ("vancouver", 49.246292, -123.116226),
    ("seattle", 47.608013, -122.335167),
    ("portland", 45.512794, -122.679565), 
    ("sanfrancisco", 37.773972, -122.431297),  
    ("losangeles", 34.052235, -118.243683),
    ("calgary", 51.049999, -114.066666),
    ("montreal", 45.508888, -73.561668),
    ("pittsburgh", 40.440624, -79.995888), 
    ("miami", 25.761681, -80.191788),
    ("newyork", 40.730610, -73.935242),
    ("boston", 42.361145, -71.057083),
    ("lasvegas", 36.188110, -115.176468),
    ("chicago", 41.881832, -87.623177), 
    ("saultstemarie", 46.533333, -84.349998),
    ("toronto", 43.651070, -79.347015), 
    ("duluth", 46.786671, -92.100487),
    ("omaha", 41.257160, -95.995102),
    ("kansascity", 39.099724, -94.578331),
    ("oklahomacity", 35.481918, -97.508469), 
    ("phoenix", 33.448376, -112.074036),
    ("elpaso", 31.772543, -106.460953),
    ("santafe", 35.691544, -105.944183), 
    ("denver", 39.742043, -104.991531),
    ("dallas", 32.779167, -96.808891),
    ("houston", 29.749907, -95.358421), 
    ("neworleans", 29.951065, -90.071533),
    ("littlerock", 34.746483, -92.289597),
    ("winnipeg", 49.895077, -97.138451),
    ("helena", 46.595806, -112.027031),
    ("saltlakecity", 40.758701, -111.876183),  
    ("washington", 38.889805, -77.009056), 
    ("raleigh", 35.787743, -78.644257),
    ("charleston", 32.776566, -79.930923),
    ("atlanta", 33.753746, -84.386330),
    ("nashville", 36.174465, -86.767960), 
    ("saintlouis", 38.627003, -90.199402)
]

# List of connections/edges 
connections = [
    ("vancouver", "calgary", 100),
    ("vancouver", "seattle", 45),

    ("seattle", "portland", 44),
    ("seattle", "calgary", 118),
    ("seattle", "helena", 189),
    ("seattle", "vancouver", 45),

    ("portland", "seattle", 44),
    ("portland", "sanfrancisco", 151),
    ("portland", "saltlakecity", 175),

    ("sanfrancisco", "losangeles", 100),
    ("sanfrancisco", "portland", 151),
    ("sanfrancisco", "saltlakecity", 156),

    ("losangeles", "sanfrancisco", 100),
    ("losangeles", "lasvegas", 66),
    ("losangeles", "phoenix", 109),
    ("losangeles", "elpaso", 191),

    ("calgary", "vancouver", 100),
    ("calgary", "seattle", 118),
    ("calgary", "helena", 130),
    ("calgary", "winnipeg", 180),

    ("montreal", "boston", 69),
    ("montreal", "newyork", 66),
    ("montreal", "toronto", 115),
    ("montreal", "saultstemarie", 193),

    ("pittsburgh", "toronto", 80),
    ("pittsburgh", "chicago", 81),
    ("pittsburgh", "newyork", 69),
    ("pittsburgh", "washington", 85),

    ("miami", "charleston", 80),
    ("miami", "atlanta", 116),
    ("miami", "neworleans", 151),

    ("newyork", "boston", 74),
    ("newyork", "montreal", 66),
    ("newyork", "washington", 76),
    ("newyork", "pittsburgh", 69),

    ("boston", "newyork", 74),
    ("boston", "montreal", 69),

    ("lasvegas", "saltlakecity", 89),
    ("lasvegas", "losangeles", 66),

    ("chicago", "pittsburgh", 81),
    ("chicago", "saintlouis", 104),
    ("chicago", "omaha", 142),
    ("chicago", "duluth", 157),

    ("saultstemarie", "toronto", 90),
    ("saultstemarie", "montreal", 193),
    ("saultstemarie", "duluth", 110),
    ("saultstemarie", "winnipeg", 156),

    ("toronto", "montreal", 115),
    ("toronto", "saultstemarie", 90),
    ("toronto", "pittsburgh", 80),

    ("duluth", "winnipeg", 103),
    ("duluth","helena", 150),
    ("duluth","omaha",74),
    ("duluth","saultstemarie",110),
    ("duluth","chicago",157),

    ("omaha","duluth",74),
    ("omaha","helena",174),
    ("omaha","denver",130),
    ("omaha","chicago",142),

    ("kansascity","denver",135),
    ("kansascity","oklahomacity",61),
    ("kansascity","saintlouis",68),

    ("oklahomacity","santafe",121),
    ("oklahomacity","kansascity",61),
    ("oklahomacity","littlerock",72),

    ("phoenix", "losangeles", 109),
    ("phoenix", "santafe", 85),
    ("phoenix", "denver", 128),

    ("elpaso", "losangeles", 191),
    ("elpaso", "santafe", 65),
    ("elpaso", "dallas", 140),

    ("santafe","phoenix", 85),
    ("santafe","elpaso", 65),
    ("santafe","oklahomacity", 121),
    ("santafe","denver", 70),

    ("denver","saltlakecity", 101),
    ("denver","phoenix",128),
    ("denver","santafe",70),
    ("denver","helena",126),
    ("denver","omaha",130),
    ("denver","kansascity",135),

    ("dallas", "elpaso", 140),
    ("dallas", "houston", 46),
    ("dallas", "littlerock", 74),

    ("houston", "dallas", 46),
    ("houston", "neworleans", 80),

    ("neworleans", "houston", 80),
    ("neworleans", "littlerock", 100),
    ("neworleans", "atlanta", 120),
    ("neworleans", "miami", 151),

    ("littlerock", "oklahomacity", 72),
    ("littlerock", "saintlouis", 60),
    ("littlerock", "nashville", 94),
    ("littlerock", "neworleans", 100),
    ("littlerock", "dallas", 74),

    ("winnipeg", "calgary", 180),
    ("winnipeg", "helena", 137),
    ("winnipeg", "duluth", 103),
    ("winnipeg", "saultstemarie", 156),

    ("helena", "calgary", 130),
    ("helena", "seattle", 189),
    ("helena", "saltlakecity", 116),
    ("helena", "denver", 126),
    ("helena", "omaha", 174),
    ("helena", "duluth", 150),
    ("helena", "winnipeg", 137),

    ("saltlakecity", "helena", 116),
    ("saltlakecity", "portland", 175),
    ("saltlakecity", "sanfrancisco", 156),
    ("saltlakecity", "lasvegas", 89),
    ("saltlakecity", "denver", 101),

    ("washington", "newyork", 76),
    ("washington", "pittsburgh", 85),
    ("washington", "raleigh", 47),

    ("raleigh", "washington", 47),
    ("raleigh", "nashville", 128),
    ("raleigh", "atlanta", 96),
    ("raleigh", "charleston", 95),

    ("charleston", "raleigh", 95),
    ("charleston", "atlanta", 63),
    ("charleston", "miami", 80),

    ("atlanta", "raleigh", 96),
    ("atlanta", "charleston", 63),
    ("atlanta", "miami", 116),
    ("atlanta", "neworleans", 120),
    ("atlanta", "nashville", 67),

    ("nashville", "saintlouis", 85),
    ("nashville", "littlerock", 94),
    ("nashville", "atlanta", 67),
    ("nashville", "raleigh", 128),

    ("saintlouis", "chicago", 104),
    ("saintlouis", "kansascity", 68),
    ("saintlouis", "littlerock", 60),
    ("saintlouis", "nashville", 85)
]
