# Patrol Field Effort

This guide walks you through configuring and running the Patrol Field Effort workflow, which analyzes ranger patrol activity within a study area and produces a dashboard summarizing field effort across three spatial metrics, sourced from EarthRanger.

---

## Overview

The workflow delivers, for a single combined analysis (there is no per-group breakdown):

- **Days since last patrol visit** map — a 5-class grid showing how recently rangers passed through each cell
- **Dwell time (hours)** map — a 5-class grid showing total time rangers spent inside each cell
- **Linear time density** map — a 5-class grid showing patrol route coverage as a percentile across the grid
- Three **stat cards** — total patrols, total distance (km), and spatial patrol coverage (%)
- An **operational days table** — distance, duration, and distinct patrol days per ranger
- An **interactive widget dashboard** combining all of the above

---

## Prerequisites

- Access to an **EarthRanger** instance with **completed** (`done`) patrols recorded within the analysis period
- An area-of-interest feature layer available via EarthRanger's spatial features (used as the study area boundary and grid clip extent)

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste this repository's URL into the **Github Link** field, then click **Add Template**:

```
https://github.com/wildlife-dynamics/patrol-field-effort.git
```

Once added, it appears in the **Workflow Templates** list. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

### Step 2 — Configure the EarthRanger Connection

Navigate to **Data Sources**, click **Connect**, and select **EarthRanger**. Fill in the connection details (URL, username, password) and save. This connection is used both to fetch patrol observations and to select the area-of-interest feature layer.

### Step 3 — Configure the Workflow Form

The configuration form has several sections on a single page:

**Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. site or reporting period) |

**Connect to EarthRanger**

Select the data source configured in Step 2.

**Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start of the analysis period |
| Until | End of the analysis period — also the reference date for "days since last visit" |

**Groupers**

This workflow fixes groupers to an empty list (`partial: groupers: []`) — every metric and the summary table are computed for the whole dataset as a single view. There is no per-group breakdown option in this workflow.

**Area of Interest**

Select the EarthRanger spatial feature(s) that define the study area boundary. This same geometry is used to clip the analysis grid and as the map extent.

**Grid Cell Size** *(Advanced Configuration)*

The grid is always built at a **custom cell size** — the underlying auto-scale/custom toggle is hidden and locked to "Customize" for this workflow. Only the **Grid Cell Size** field (metres) is exposed, defaulting to **1000 m**.

**Base Map Layers**

Configure the background tile layer(s) used by all three maps (URL, opacity, max zoom).

### Step 4 — Run

Once all sections are filled in, click **Submit**.

---

## Running the Workflow

Once submitted, the runner will:

1. Fetch completed (`status: done`) patrol observations from EarthRanger for the configured time range (`raise_on_empty: true` — the run fails rather than producing an empty dashboard if no patrols match).
2. Convert the observations into patrol trajectories.
3. Validate that the selected area-of-interest geometry is polygonal, reproject it to a metric CRS (EPSG:3857), and save it as the study area boundary.
4. Build an analysis grid over the study area (default 1000 m cells) and clip it to the AOI boundary.
5. Reproject the patrol trajectories to EPSG:3857 and spatially join them against the grid to determine which trajectory segments intersect which cells.
6. Compute **days since last visit** per cell (latest patrol end time relative to the "Until" date), flag visited cells, and classify into 5 natural-breaks bins (Red–Yellow–Green palette; unvisited cells are grey).
7. Compute **dwell time** per cell (total hours rangers spent inside each cell), using the same flagging and 5-bin classification scheme.
8. Compute **linear time density** per cell (route coverage expressed as a percentile), adding back cells with zero coverage so every grid cell is represented, then apply the same classification scheme.
9. Standardize patrol column names, extract the patrol date, and build an **operational days table** grouped by ranger (subject ID and name) — total distance (km), duration (hrs), and distinct patrol days.
10. Compute the three summary stats: total distinct patrols, total patrol distance (km), and patrol coverage — the percentage of the study area with at least one recorded visit.
11. Determine an appropriate zoom/center from the study area extent, and composite an unfilled study-area boundary layer under each of the three metric maps.
12. Assemble the dashboard: 3 stat cards, 3 interactive maps, and 1 sortable/filterable table.
13. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

### Field Effort Maps

| File | Description |
|---|---|
| `days_since_patrol_visit.gpkg` | Grid with days-since-visit stats |
| `days_since_patrol_visit_map.html` | Interactive days-since-visit map |
| `time_spent_per_cell.gpkg` | Grid with dwell time (hours) per cell |
| `time_spent_per_grid_map.html` | Interactive dwell time map |
| `patrols_linear_time_density.gpkg` | Grid with linear time density percentiles |
| `ltd_patrols_map.html` | Interactive linear time density map |

### Boundary & Raw Data

| File | Description |
|---|---|
| `er_spatial_file.gpkg` | Study area boundary |
| `patrol_observations.gpkg` | Raw patrol observation points |
| `patrol_trajectories.gpkg` | Patrol trajectory lines |

### Summary Table

| File | Description |
|---|---|
| `patrol_operational_days.csv` | Operational days, distance, and duration per ranger |

---

## Inputs

| Parameter | Description |
|---|---|
| EarthRanger connection | Source system for patrol data and the area-of-interest layer |
| Time range | Start and end dates for the analysis period |
| Area of interest | Spatial feature(s) defining the study area |
| Grid cell size | Cell size in metres (default 1000 m) |
| Base maps | Background tile layers for the maps |
