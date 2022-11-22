# Things left for Later 

- SFMTA: Only calculate ridership for lines that have 2022 data. Some lines were cancelled due to covid and cause failing later on when trying to match route id with GTFS data. 

- SFMTA: More than two shape_ids matched to many routes. Currently going to take the longest in each direction, and drop the rest. Investigate if something better can be done. 

- SFMTA: Investigate why routes are sometimes double added to the routes intersecting stop. How could route intersect stop twice. Is it stopping there in both directions?

- General: We replace each stop with its parent station in the simplification step? Is this okay for reversing it?