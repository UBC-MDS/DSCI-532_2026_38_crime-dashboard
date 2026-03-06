# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [0.2.1] - 2026-03-05

### Changed

- Aligned chart titles with card headers for consistency across all visualizations
- Converted City Comparison bar chart from vertical to horizontal orientation to prevent x-axis labels from being cut off

### Fixed

- Synchronized color schemes between Trend Over Time line chart and City Comparison bar chart so the same city uses the same color in both visualizations

## [0.2.0] - 2026-02-28

### Added

- Implemented components in dashboard (issues #23-26)
- Created GIF demo and contributors section for README.md ([#27](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/27#issue-3985219934))
- Implemented reactivity structure ([#28](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/28#issue-3985222765))
- Created reactivity diagram ([#29](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/29#issue-3985225748))
- Preview and stable builds deployed (issues #30-31)
- Created component inventory in specifications ([#36](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/36#issue-3985246750))

### Changed

- Updated job stories in specifications ([#37](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/37#issue-3985248141))

### Fixed

N/A

### Known Issues

N/A

### Reflection

The Crime Dashboard successfully implements the majority of the core functionality outlined in our milestone 1 proposal. User stories 1, 3, and 4 are now fully implemented with dashboard components that allow for long-term and inter-city analysis of crime trends. Said components include an interactive map displaying local crime statistics and line plot for long-term trends, with both being filterable by location and time span. User Story 2 is not yet implemented, with comparisons across violent crime subcategories (homicide, robbery, rape, and aggravated assault) still needing to be integrated.

The current composition of the dashboard includes all components of the M1 sketch and M2 specification, only deviating with some marginal layout changes. As it stands at the end of Milestone 2, there are no notable deviations from visualization best practices, nor are there any known issues.

Overall, the dashboard holds strong alignment with user needs, providing nearly every capability we sought to include. However, it is still limited in categorical crime comparisons which will be implemented in future iterations.

## [0.1.0] - 2026-02-14

### Added

- Initial repository, app skeleton setup ([#5](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/5#issue-3929168391))
- Established a dashboard proposal ([#6](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/6#issue-3929170365))
- Sketched a prospective dashboard ([#7](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/7#issue-3929171826))
- Selected a dataset, perfomed eda ([#8](https://github.com/UBC-MDS/DSCI-532_2026_38_crime-dashboard/issues/8#issue-3929173743))
