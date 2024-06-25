 Project concept
## About
### Title
Toronto renovation hot spots
### Description
Creating a map of Toronto showing neighbourhoods with the most home renovations per resident.

## Planned concept
### Data flow
Extract live data from [the Toronto Open Data portal](https://open.toronto.ca/): Recent building permit data ([active](https://open.toronto.ca/dataset/building-permits-active-permits/) and [cleared](https://open.toronto.ca/dataset/building-permits-cleared-permits/)), [address data](https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/), and [neighbourhood profiles data](https://open.toronto.ca/dataset/neighbourhood-profiles/). Transform the data: 
1. geolocate building permit addresses into address points
2. attach neighbourhood data to address points by geofencing
3. attach 2011, 2016, and 2021 neighbourhood data to understand change in neighbourhood statistics, where possible
4. calculate a neighbourhood score of permit costs if applicable and number of permits as a function of neighbourhood population
### Visualization
Create a clorpleth (geo heat map) with [OSM and Leaflet](https://leafletjs.com/examples/choropleth/)). Plot data onto a map: colour ramp based on the neighbourhood renovation score, where each shape is the neighbourhood. Hovering over each shape should provide neighbourhood statistics in a popup.

## Code
### Language
Python

## Current work
### 2024-06-25
Built initial exploratory transformation pipelines and analysis. Using these as a base, I will create data pipelines to deliver the transformations for the heatmap and clustermap analytics I created.

## License
Copyright 2024 Nikko Torres, under the [CC BY-NC License](https://creativecommons.org/licenses/by-nc/4.0/)
