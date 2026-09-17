European Gridded Seasonal Precipitation Reconstructions
-----------------------------------------------------------------------
               World Data Center for Paleoclimatology, Boulder
                                  and
                     NOAA Paleoclimatology Program
-----------------------------------------------------------------------
NOTE: PLEASE CITE CONTRIBUTORS WHEN USING THIS DATA!!!!!


NAME OF DATA SET: European Gridded Seasonal Precipitation Reconstructions
LAST UPDATE: 6/2007 (Original receipt by WDC Paleo)
CONTRIBUTOR: Andreas Pauling, University of Bern.
IGBP PAGES/WDCA CONTRIBUTION SERIES NUMBER: 2007-054

SUGGESTED DATA CITATION: Pauling, A., et al. 2007.
European Gridded Seasonal Precipitation Reconstructions.
IGBP PAGES/World Data Center for Paleoclimatology 
Data Contribution Series # 2007-054.
NOAA/NCDC Paleoclimatology Program, Boulder CO, USA.


ORIGINAL REFERENCE: 
Pauling, A., J. Luterbacher, C. Casty, and H. Wanner. 2006.
Five hundred years of gridded high-resolution precipitation 
reconstructions over Europe and the connection to large-scale circulation. 
Climate Dynamics, Vol. 26, No. 4, pp. 387-405, March 2006. 

ABSTRACT: 
We present seasonal precipitation reconstructions for European land 
areas (30°W to 40° E/30-71°N; given on a 0.5° x 0.5° resolved grid) 
covering the period 1500-1900 together with gridded reanalysis from 
1901 to 2000 (Mitchell and Jones 2005). Principal component regression 
techniques were applied to develop this dataset.  A large variety of 
long instrumental precipitation series, precipitation indices based 
on documentary evidence and natural proxies (tree-ring chronologies, 
ice cores, corals and a speleothem) that are sensitive to precipitation 
signals were used as predictors. Transfer functions were derived over 
the 1901-1983 calibration period and applied to 1500-1900 in order to 
reconstruct the large-scale precipitation fields over Europe. 
The performance (quality estimation based on unresolved variance 
within the calibration period) of the reconstructions varies over 
centuries, seasons and space. Highest reconstructive skill was found 
for winter over central Europe and the Iberian Peninsula. Precipitation 
variability over the last half millennium reveals both large interannual 
and decadal fluctuations. Applying running correlations, we found major 
non-stationarities in the relation between large-scale circulation and 
regional precipitation. For several periods during the last 500 years, 
we identified key atmospheric modes for southern Spain/northern Morocco
and central Europe as representations of two precipitation regimes. 
Using scaled composite analysis, we show that precipitation extremes 
over central Europe and southern Spain are linked to distinct pressure 
patterns.  Due to its high spatial and temporal resolution, this
dataset allows detailed studies of regional precipitation variability 
for all seasons, impact studies on different time and space scales, 
comparisons with high-resolution climate models as well as analysis 
of connections with regional temperature reconstructions.


GEOGRAPHIC REGION: Europe
PERIOD OF RECORD: 1500-2000 AD

FUNDING SOURCES: This work is part of the EU-project SOAP  
(simulations, observations and palaeoclimate, 
data: climate variability over the last 500 years), 
the Swiss part being funded by the Staatssekretariat fur Bildung 
und Forschung (SBF) under contract 01.0560. Publication of this work 
was also supported by the Marchese Francesco Medici del Vascello foundation. 
Jurg Luterbacher is supported by the Swiss National Science foundation
through its National Center of Competence in Research in Climate
program, project PALVAREX. Carlo Casty is funded by the
European Commission under the Fifth Framework Programme
Contract Nr. EVR1-2002-000413, project PACLIVA.


DESCRIPTION: 
European Gridded Seasonal Precipitation Reconstructions

The data available here are: 

1)
prec-pauling-wi.txt.gz (Winter fine-resolution 0.5° grids, 8MB) 
prec-pauling-sp.txt.gz (Spring fine-resolution 0.5° grids, 8MB) 
prec-pauling-su.txt.gz (Summer fine-resolution 0.5° grids, 8MB) 
prec-pauling-au.txt.gz (Autumn fine-resolution 0.5° grids, 8MB) 
These files have been compressed with gzip.
 
All these files cover the area 30.25N-70.75N / 29.75W-39.75E 
(all coordinates given here denote the centre of each box),
Grid lon x lat = 140 x 82. Non-land grid boxes are indicated by 
values set to NA. Data run from 1500 to 2000. Data from 1901-2000 
are observational estimates from the Mitchell and Jones (2005) dataset. 
Data prior to 1901 are reconstructed values 
(see data set reference for details: Pauling et al. (2006)).

The files are ASCII plain text, with the following format:

line 1: year season (13=winter, 14=spring, 15=summer, 16=autumn)
line 2: top row of grid (70.75N, 29.75W-39.75E)
line 3: 2nd row of grid (70.25N, 29.75W-39.75E)
etc.
line 83: 82nd row of grid (30.25N , 29.75W-39.75E)

The following 83 lines describe the grid for the second year and so on.



2) 
Mean of the European precipitation reconstructions for winter 
(File precmean-pauling-wi.txt), spring (precmean-pauling-sp.txt), 
summer (precmean-pauling-su.txt) and autumn (precmean-pauling-au.txt).

For these spatial averages uncertainties are provided as labeled in the file. 
All data are reconstructed values.



