This dataset contains Uniform Crime Reporting (UCR) data for 68 major U.S. police departments from 1975 to 2015, compiled by The Marshall Project.

Each row represents one department in one year.

Columns:
- ORI: Unique agency identifier code
- department_name: Name of the police department/city
- year: Year of the record (1975–2015)
- total_pop: Estimated population of the jurisdiction
- homs_sum: Total number of homicides
- rape_sum: Total number of rapes
- rob_sum: Total number of robberies
- agg_ass_sum: Total number of aggravated assaults
- violent_crime: Total number of violent crimes reported
- months_reported: Number of months reported (12 = full year)
- violent_per_100k: Violent crime rate per 100,000 residents
- homs_per_100k: Homicide rate per 100,000 residents
- rape_per_100k: Rape rate per 100,000 residents
- rob_per_100k: Robbery rate per 100,000 residents
- agg_ass_per_100k: Aggravated assault rate per 100,000 residents
- source: Data source for that record
- url: URL reference for that record

Notes:
- The "per 100k" columns are the most useful for comparisons between cities of different sizes.
- There is a row with department_name "National" which represents a national aggregate/average.
- Some city names include state abbreviations (e.g., "Nashville, Tenn.") while major cities do not (e.g., "Chicago").
- violent_crime = homs_total + rape_total + rob_total + agg_ass_total
