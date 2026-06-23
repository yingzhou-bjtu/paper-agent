# draw.io Cookbook

Recipes for emitting draw.io–pastable content. Two output modes:

1. **mxGraph XML** (preferred): every snippet below is a **complete `<mxfile>` document** so it pastes as-is. User opens a blank diagram → *Extras → Edit Diagram…* → selects-all → pastes → *OK*.
2. **Structured NL description** (fallback): use when the figure has **> 30 nodes OR the XML exceeds ~150 lines**. User recreates by dropping nodes per the explicit list.

All `<mxCell value="…">` content that contains HTML tags (`<b>`, `<br/>`, `<font>`) is **entity-escaped** (`&lt;b&gt;`, `&lt;br/&gt;`) — draw.io renders the HTML when `html=1` is in the style. Unescaped angle brackets break the XML parser.

---

## Recipe 1 — System architecture (block diagram)

Coordinates are on a 240×120 grid; bump `x` by 240 per column, `y` by 140 per row. Palette roles follow [style-conventions.md](style-conventions.md): Data = blue, Model = green, Loss = orange.

```xml
<mxfile host="app.diagrams.net">
  <diagram name="architecture" id="arch">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="M1" value="&lt;b&gt;Data Loader&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40"  y="40"  width="160" height="64" as="geometry"/>
        </mxCell>
        <mxCell id="M2" value="&lt;b&gt;Encoder&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="280" y="40"  width="160" height="64" as="geometry"/>
        </mxCell>
        <mxCell id="M3" value="&lt;b&gt;Decoder&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="520" y="40"  width="160" height="64" as="geometry"/>
        </mxCell>
        <mxCell id="M4" value="&lt;b&gt;Loss Head&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="760" y="40"  width="160" height="64" as="geometry"/>
        </mxCell>

        <mxCell id="e1" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="M1" target="M2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e2" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="M2" target="M3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e3" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="M3" target="M4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

To add a secondary-language label (bilingual), extend the `value`:
`value="&lt;b&gt;Encoder&lt;/b&gt;&lt;br/&gt;&lt;font size=&#39;10&#39;&gt;编码器&lt;/font&gt;"` (note: single quotes inside attributes escape as `&#39;`).

### Style palette (paper-safe, aligned with [style-conventions.md](style-conventions.md))

| Role | Fill | Stroke |
|---|---|---|
| Data / I/O | `#dae8fc` | `#6c8ebf` |
| Preprocessing | `#fff2cc` | `#d6b656` |
| Model / Compute | `#d5e8d4` | `#82b366` |
| Loss / Objective | `#ffe6cc` | `#d79b00` |
| External system | `#f8cecc` | `#b85450` |
| Meta / Grouping | `#f5f5f5` | `#666666` |

---

## Recipe 2 — Module dependency graph

```xml
<mxfile host="app.diagrams.net">
  <diagram name="deps" id="deps">
    <mxGraphModel dx="1200" dy="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- One module node per import target: -->
        <mxCell id="N1" value="utils" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#444;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="100" height="40" as="geometry"/>
        </mxCell>
        <!-- ...repeat per module... -->

        <!-- One dashed open-arrow edge per import: -->
        <mxCell id="E1" style="endArrow=open;dashed=1;html=1;" edge="1" parent="1" source="N1" target="N2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <!-- ...repeat per import... -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

After pasting, run *Arrange → Layout → Vertical Tree* (or *Vertical Flow*) for an auto-layout.

NL fallback form: list `module_A --imports--> module_B`, one per line.

---

## Recipe 3 — Data pipeline (swimlane)

```xml
<mxfile host="app.diagrams.net">
  <diagram name="pipeline" id="pipe">
    <mxGraphModel dx="1200" dy="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="lane1" value="CPU (data)" style="shape=swimlane;horizontal=0;startSize=24;fillColor=#f5f5f5;strokeColor=#666;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="720" height="120" as="geometry"/>
        </mxCell>
        <mxCell id="lane2" value="GPU (model)" style="shape=swimlane;horizontal=0;startSize=24;fillColor=#eef7ea;strokeColor=#666;" vertex="1" parent="1">
          <mxGeometry x="40" y="180" width="720" height="120" as="geometry"/>
        </mxCell>

        <!-- Stages go inside lanes (parent="lane1" / parent="lane2"); coords then become lane-relative. -->
        <mxCell id="S1" value="Raw" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="lane1">
          <mxGeometry x="40" y="40" width="120" height="48" as="geometry"/>
        </mxCell>
        <mxCell id="S2" value="Tokenize" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="lane1">
          <mxGeometry x="200" y="40" width="120" height="48" as="geometry"/>
        </mxCell>
        <mxCell id="S3" value="Model" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="lane2">
          <mxGeometry x="40" y="40" width="120" height="48" as="geometry"/>
        </mxCell>

        <mxCell id="E1" style="endArrow=classic;html=1;" edge="1" parent="1" source="S1" target="S2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="E2" style="endArrow=classic;html=1;" edge="1" parent="1" source="S2" target="S3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## Recipe 4 — Algorithm flowchart (training / inference loop)

Standard flowchart shapes:

- Terminator (start/end): `rounded=1;fillColor=#000000;fontColor=#ffffff;` pill.
- Process (step): `rounded=1;` rectangle.
- Decision (if/while): `rhombus;` diamond.
- I/O: `shape=parallelogram;perimeter=parallelogramPerimeter;`.
- Loop edge: `endArrow=classic;curved=1;` with a label like `epoch++`.

Edge labels belong on the edge `value` attribute. Keep decision labels to ≤ 2 words. Same `<mxfile>/<diagram>/<mxGraphModel>/<root>` wrapping as Recipe 1 applies.

---

## Recipe 5 — Attention / confusion-matrix heatmap

draw.io does not render color-mapped matrices cleanly. **Switch to TikZ** — see [tikz-cookbook.md](tikz-cookbook.md) Recipe 6. In the draw.io output, emit only a placeholder rectangle with a note: *"Replace with TikZ heatmap — tikz-cookbook.md Recipe 6."*

---

## NL fallback format (trigger: > 30 nodes OR > 150 XML lines)

```
NODES:
  N1  [rect,   role=data]   label="Data Loader"   at (col=1, row=1)
  N2  [rect,   role=model]  label="Encoder"        at (col=2, row=1)
  ...
EDGES:
  N1 -> N2   solid classic arrow, label=""
  N2 -> N3   solid classic arrow, label="h_t"
  ...
LAYOUT:
  column spacing 240 px, row spacing 140 px
  canvas 1169 × 826 (A4 landscape)
```

`role=data|model|loss|preprocess|external|meta` drives fill/stroke via [style-conventions.md](style-conventions.md).

---

## Paste instructions (emit verbatim to user)

1. Open [app.diagrams.net](https://app.diagrams.net) (or Desktop draw.io).
2. *File → New → Blank diagram → Create* (needed — the *Edit Diagram* menu is disabled on the welcome screen).
3. *Extras → Edit Diagram…*. If you don't see "Extras", your tab hasn't loaded a diagram yet — go back to step 2.
4. Select **all existing XML** in the dialog, replace with the snippet above, *OK*.
5. *File → Save as `<figure-name>.drawio`*; export to PDF or SVG via *File → Export as…*.

Alternative: save the snippet locally as `<figure-name>.drawio` and *File → Open → Open From → Device*.
