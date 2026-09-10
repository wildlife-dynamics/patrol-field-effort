"""
Generate the Patrol Field Effort Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: patrol_field_effort_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "patrol_field_effort_technical_guide.pdf"

# ── Colour palette (same as sibling workflow technical guides) ──────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)   # table cell paragraph


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "Patrol Field Effort — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Patrol Field Effort — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Patrol Field Effort", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Patrol Field Effort Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>Patrol Field Effort</b> workflow analyses ranger patrol activity within "
            "a user-selected study area, sourced live from <b>EarthRanger</b>. It converts "
            "completed patrols into trajectories, overlays them onto an analysis grid, and "
            "computes three complementary spatial field-effort metrics per grid cell: days "
            "since last visit, dwell time, and linear time density."
        ),
        p(
            "The workflow produces three interactive maps, three scalar summary widgets, "
            "and one sortable operational-days table, all assembled into a single "
            "dashboard. There is no per-group breakdown &mdash; groupers are fixed to an "
            "empty list, so every output covers the whole dataset as one combined view."
        ),
        note(
            "All three field-effort metrics are computed over the <b>same</b> analysis "
            "grid, so the three maps are directly comparable cell-for-cell."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "Patrol data is fetched from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. <code>get_patrol_observations</code> queries "
            "completed patrols only (<code>status: [\"done\"]</code>), with "
            "<code>include_patrol_details: true</code>, "
            "<code>patrols_overlap_daterange: true</code>, a sub-page size of 150, and "
            "<code>raise_on_empty: true</code> &mdash; the run fails rather than producing "
            "an empty dashboard if no patrols match the configured time range."
        ),

        sp(4), h2("2.2 Groupers"),
        p(
            "<code>set_groupers</code> is called with <code>partial: groupers: []</code>, "
            "fixing the grouping strategy to an empty list. Unlike sibling patrol workflows "
            "that expose a user-selectable grouper field, this workflow always computes a "
            "single combined view &mdash; there is no per-group map or table variant."
        ),

        sp(6), h2("2.3 Area of Interest"),
        p(
            "The study area boundary is fetched live from EarthRanger via "
            "<code>get_spatial_features</code> (no bundled or Dropbox-downloaded boundary "
            "file). The selected geometry is validated as polygonal "
            "(<code>assert_polygon_types</code>) and reprojected to a metric CRS "
            "(EPSG:3857) before being used as both the map extent and the grid clip "
            "boundary. It is persisted as <code>er_spatial_file.gpkg</code>."
        ),

        sp(4), h2("2.4 Analysis Grid &amp; Cell Size"),
        p(
            "The grid cell size field normally lets a user choose between an "
            "auto-scaled grid and a custom cell size. This workflow overrides the RJSF "
            "schema (<code>rjsf-overrides</code> in <code>spec.yaml</code>) to only accept "
            "the <b>custom</b> cell-size schema, hides the auto/custom toggle in the form, "
            "and defaults the cell size to <b>1000 m</b>. The grid is built with "
            "<code>create_meshgrid</code> (<code>intersecting_only: true</code>) and then "
            "clipped to the study area with an intersection overlay "
            "(<code>keep_geom_type: true</code>, <code>make_valid: true</code>)."
        ),

        sp(6), h2("2.5 Base Map Tile Layers"),
        p(
            "Background tile layer(s) for all three maps are configured via "
            "<code>set_base_maps_pydeck</code> and are fully user-editable (URL, opacity, "
            "max zoom) &mdash; there are no workflow-level defaults hardcoded in "
            "<code>spec.yaml</code> beyond the task's own schema defaults."
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Patrol Observations → Trajectories"),
        p(
            "<code>relocations_to_trajectory</code> converts the fetched patrol "
            "observations into trajectory segments, adding <code>segment_start</code>, "
            "<code>segment_end</code>, and <code>dist_meters</code>. Trajectories are "
            "reprojected to EPSG:3857 (<code>reproject_trajs</code>) for all metric "
            "calculations, then re-reprojected to EPSG:4326 (WGS84) wherever a result is "
            "rendered on an interactive map. Raw observations and trajectories are "
            "persisted as <code>patrol_observations.gpkg</code> and "
            "<code>patrol_trajectories.gpkg</code>."
        ),

        sp(4), h2("3.2 Column Standardisation &amp; Patrol Date"),
        p(
            "<code>map_columns</code> renames raw EarthRanger <code>extra__*</code> fields "
            "to plain names used throughout the workflow:"
        ),
        make_table(
            [
                [c("Original column"),          c("Renamed to")],
                [c("extra__patrol_type__value"), c("patrol_type")],
                [c("extra__patrol_serial_number"), c("patrol_serial_number")],
                [c("extra__patrol_status"),      c("patrol_status")],
                [c("extra__patrol_subject"),     c("patrol_subject")],
                [c("extra__subject_id"),         c("subject_id")],
                [c("extra__patrol_id"),          c("patrol_id")],
                [c("extra__patrol_title"),       c("name")],
            ],
            [7.5*cm, 9*cm],
        ),
        sp(4),
        p(
            "<code>decompose_datetime</code> then extracts the calendar date component "
            "from <code>segment_start</code> (as <code>segment_start_date</code>), used "
            "later to count distinct patrol days per ranger."
        ),

        sp(4), h2("3.3 Grid Overlay"),
        p(
            "Trajectories are reduced to <code>segment_start</code>, <code>segment_end</code>, "
            "and <code>geometry</code>, then spatially joined against the clipped analysis "
            "grid with <code>spatial_join</code> (<code>how: inner</code>, "
            "<code>predicate: intersects</code>). Every downstream metric is computed from "
            "this joined table, grouped back to the grid's <code>index</code> column."
        ),
    ]

    # ── 4. Field Effort Metrics ───────────────────────────────────────────────
    story += [
        sp(4), h1("4. Field Effort Metrics — Methodology"), hr(),

        h2("4.1 Days Since Last Visit"),
        p(
            "<code>summarize_df</code> aggregates the joined trajectory/grid table by "
            "<code>index</code>, taking <code>max(segment_end)</code> as "
            "<code>last_visited</code> and <code>min(segment_start)</code> as "
            "<code>first_visited</code> per cell. <code>add_time_since_visit</code> then "
            "computes <code>days_since_visit</code> as the elapsed time between "
            "<code>last_visited</code> and the end of the configured time range. Cells "
            "with no patrol coverage have a null value, flagged via "
            "<code>add_non_null_flag</code> (column <code>visited</code>)."
        ),

        sp(4), h2("4.2 Dwell Time (Hours)"),
        p(
            "<code>compute_dwell_time</code> takes the reprojected patrol trajectories "
            "and the gridded study area and computes <code>hours_in_cell</code> &mdash; "
            "total time rangers spent with a fix inside each grid cell. Cells with zero "
            "recorded dwell time are again flagged via <code>add_non_null_flag</code>."
        ),

        sp(4), h2("4.3 Linear Time Density"),
        p(
            "<code>calculate_linear_time_density</code> computes route-coverage density "
            "as a <code>percentile</code> value per cell that intersects a patrol "
            "trajectory (<code>percentiles: null</code> &mdash; uses the task's default "
            "percentile scheme). Cells with <b>no</b> trajectory coverage are not returned "
            "by this task, so they are recovered separately: a <code>difference</code> "
            "overlay between the full clipped grid and the covered cells yields the "
            "uncovered cells, which are then concatenated back onto the result "
            "(<code>concat_dataframes</code>, ensuring the <code>percentile</code>, "
            "<code>density</code>, and <code>area_sqkm</code> columns exist on both sides) "
            "so every grid cell appears in the final output."
        ),
    ]

    # ── 5. Classification & Styling ───────────────────────────────────────────
    story += [
        sp(4), h1("5. Classification &amp; Styling"), hr(),
        p(
            "All three metrics (<code>days_since_visit</code>, <code>hours_in_cell</code>, "
            "<code>percentile</code>) go through the identical classification pipeline:"
        ),
        make_table(
            [
                [c("Step"),           c("Task"),               c("Configuration")],
                [c("Bin"),            c("add_visit_bins"),      c("5 classes, natural-breaks (Jenks) scheme, absolute value")],
                [c("No-data label"),  c("add_visit_bins"),      c("\"Unvisited\" for cells not flagged as visited")],
                [c("Colour"),         c("add_bin_colors"),      c("RdYlGn palette across the 5 bins")],
                [c("No-data colour"), c("add_bin_colors"),      c("#808080 (grey) for \"Unvisited\" cells")],
            ],
            [3.2*cm, 4.3*cm, 8.5*cm],
        ),
        sp(4),
        p(
            "Each metric's hex colours are decategorised to strings and converted to RGBA "
            "(<code>add_rgba_from_hex</code>) before being used as a deck.gl fill colour. "
            "Bin legend order is fixed with <code>order_bin_categories</code> so the legend "
            "always reads from the lowest to the highest bin, ending in \"Unvisited\"."
        ),
    ]

    # ── 6. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Map Outputs — Methodology"), hr(),
        p(
            "All three maps share the same GeoJSON polygon layer style: filled, stroked "
            "in black at 0.25 px width, 55&#37; fill opacity, fill colour driven by each "
            "cell's RGBA colour. A single unfilled study-area boundary layer (0&#37; fill "
            "opacity, full line opacity) is composited underneath every map for spatial "
            "context. Map zoom and centre are computed once from the study area's extent "
            "and reused across all three maps (max zoom 15 for extent-fitting, 10 for the "
            "rendered map)."
        ),
        make_table(
            [
                [c("Map"),                       c("Value column"), c("Legend title")],
                [c("Days Since Patrol Visit"),   c("days_since_visit"), c("Time Since Visit (Days)")],
                [c("Time Spent Per Grid Cell"),  c("hours_in_cell"),    c("Time Spent (Hours)")],
                [c("Patrol Linear Time Density"),c("percentile"),       c("Time Spent")],
            ],
            [5.5*cm, 4*cm, 6.5*cm],
        ),
        sp(4),
        p(
            "Each map is rendered with <code>draw_map</code> (legend placement: "
            "bottom-right) and persisted as an interactive HTML file "
            "(<code>days_since_patrol_visit_map.html</code>, "
            "<code>time_spent_per_grid_map.html</code>, and "
            "<code>ltd_patrols_map.html</code> respectively)."
        ),
    ]

    # ── 7. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Summary Metrics"), hr(),

        h2("7.1 Scalar Dashboard Widgets"),
        make_table(
            [
                [c("Widget title"),        c("Source"),                              c("Aggregator / Unit")],
                [c("Total Patrols"),       c("subject_id"),                          c("nunique &middot; count")],
                [c("Total Patrol Distance"), c("dist_meters"),                       c("sum &middot; converted m &rarr; km")],
                [c("Patrol Coverage"),     c("compute_patrol_effort_fraction"),      c("fraction of grid with &ge;1 visit &middot; %")],
            ],
            [4.5*cm, 5*cm, 6.5*cm],
        ),

        sp(6), h2("7.2 Operational Days Table"),
        p(
            "<code>summarize_df</code> groups the renamed, date-decomposed trajectory "
            "table by <code>subject_id</code> and <code>patrol_subject</code>:"
        ),
        make_table(
            [
                [c("Output column"), c("Source column"),        c("Aggregator"), c("Unit")],
                [c("distance_km"),   c("dist_meters"),           c("sum"),        c("km (1 dp)")],
                [c("duration_hrs"),  c("timespan_seconds"),      c("sum"),        c("h (1 dp)")],
                [c("patrol_days"),   c("segment_start_date"),    c("nunique"),    c("count")],
            ],
            [4*cm, 4.5*cm, 3.5*cm, 4*cm],
        ),
        sp(4),
        p(
            "Column headers are relabelled for display (Subject ID, Patrol Subject, "
            "Distance (km), Duration (hrs), Patrol Days) and rendered as a sortable, "
            "filterable HTML table (<code>draw_table</code>), persisted with the "
            "<code>patrol_summary_table</code> filename suffix."
        ),
    ]

    # ── 8. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("8. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the final dashboard from seven "
            "widgets, in order:"
        ),
        make_table(
            [
                [c("#"), c("Widget"),                       c("Type")],
                [c("1"), c("Total Patrols"),                c("Single value")],
                [c("2"), c("Total Patrol Distance"),        c("Single value")],
                [c("3"), c("Patrol Coverage"),              c("Single value")],
                [c("4"), c("Days Since Patrol Visit"),      c("Map")],
                [c("5"), c("Time Spent Per Grid Cell (Hours)"), c("Map")],
                [c("6"), c("Patrol Linear Time Density"),   c("Map")],
                [c("7"), c("Patrol Summary"),                c("Table")],
            ],
            [1.5*cm, 8*cm, 6.5*cm],
        ),
    ]

    # ── 9. Output Files ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Output Files"), hr(),
        p("All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                [c("File"),                              c("Format"),    c("Content")],
                [c("er_spatial_file.gpkg"),               c("GeoPackage"), c("Study area boundary (EPSG:3857)")],
                [c("patrol_observations.gpkg"),           c("GeoPackage"), c("Raw patrol observation points")],
                [c("patrol_trajectories.gpkg"),           c("GeoPackage"), c("Patrol trajectory lines")],
                [c("days_since_patrol_visit.gpkg"),       c("GeoPackage"), c("Grid with days-since-visit stats")],
                [c("days_since_patrol_visit_map.html"),   c("HTML"),       c("Interactive days-since-visit map")],
                [c("time_spent_per_cell.gpkg"),           c("GeoPackage"), c("Grid with dwell time (hours) per cell")],
                [c("time_spent_per_grid_map.html"),       c("HTML"),       c("Interactive dwell time map")],
                [c("patrols_linear_time_density.gpkg"),   c("GeoPackage"), c("Grid with linear time density percentiles")],
                [c("ltd_patrols_map.html"),               c("HTML"),       c("Interactive linear time density map")],
                [c("patrol_operational_days.csv"),        c("CSV"),        c("Operational days per ranger")],
            ],
            [5.5*cm, 2.7*cm, 8.3*cm],
        ),
    ]

    # ── 10. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("10. Workflow Execution Logic"), hr(),

        h2("10.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> &mdash; skips a task (and its dependants) when any "
            "input DataFrame is empty."
        ),
        bullet(
            "<b>any_dependency_skipped</b> &mdash; propagates skips downstream "
            "automatically."
        ),
        p(
            "Unlike some sibling workflows, patrol widget tasks here do "
            "<b>not</b> override this with <code>skipif: [never]</code> &mdash; combined "
            "with <code>raise_on_empty: true</code> on the patrol fetch, an empty result "
            "set surfaces as a hard failure rather than a partially-empty dashboard."
        ),

        sp(4), h2("10.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),           c("Tasks")],
                [c("Setup"),           c("ER connection, time range, groupers (fixed empty), base maps, area of interest")],
                [c("Ingest"),          c("Fetch completed patrol observations &rarr; build trajectories")],
                [c("Study area"),      c("Validate polygon &rarr; reproject to EPSG:3857 &rarr; persist")],
                [c("Grid"),            c("Create meshgrid (custom cell size) &rarr; clip to study area &rarr; reset index")],
                [c("Join"),            c("Reproject trajectories &rarr; select columns &rarr; spatial join onto grid")],
                [c("Days since visit"),c("Summarise last/first visit &rarr; time-since-visit &rarr; merge &rarr; flag &rarr; bin &rarr; colour &rarr; map")],
                [c("Dwell time"),      c("Compute dwell time &rarr; merge &rarr; flag &rarr; bin &rarr; colour &rarr; map")],
                [c("Linear time density"), c("Calculate LTD &rarr; recover unvisited cells (difference + concat) &rarr; flag &rarr; bin &rarr; colour &rarr; map")],
                [c("Summary"),         c("Rename columns &rarr; extract date &rarr; operational days table &rarr; scalar widgets")],
                [c("Dashboard"),       c("gather_dashboard combines all 7 widgets")],
            ],
            [4.2*cm, 12.3*cm],
        ),
    ]

    # ── 11. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("11. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                          c("Version"),               c("Role")],
                [c("ecoscope-platform"),                 c("&gt;=2.18.0"),           c("Consolidated core task library and workflow engine")],
                [c("ecoscope-workflows-ext-custom"),     c("0.1.0rc14.*"),           c("Utility tasks (persistence, maps, layers)")],
                [c("ecoscope-workflows-ext-ste"),        c("0.0.0rc1.*"),            c("Spatial operations tasks (view state, layer combination)")],
                [c("ecoscope-workflows-ext-mep"),        c("1.0.3.*"),               c("Domain tasks (visit bins, dwell time, colour bins, patrol effort fraction)")],
                [c("pydeck"),                            c("0.9.2"),                 c("Deck.gl map rendering")],
                [c("opentelemetry-sdk"),                 c("&gt;=1.20.0, &lt;2.0.0"), c("Observability/tracing")],
            ],
            [6*cm, 4.3*cm, 6.2*cm],
        ),
        sp(4),
        p(
            "Packages are distributed via the <code>repo.prefix.dev</code> conda channels "
            "(<code>ecoscope-workflows</code> and <code>ecoscope-workflows-custom</code>) "
            "and pinned to compatible version ranges in <code>spec.yaml</code>. The runtime "
            "environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
