# draw.io Cookbook

## Output Modes

1. Prefer complete `<mxfile>` XML for figures with 30 nodes or fewer and about 150 XML lines or fewer.
2. Use structured natural-language fallback for larger graphs.

All HTML in `value="..."` must be entity escaped, e.g. `&lt;b&gt;Encoder&lt;/b&gt;`.

## Minimal System Architecture XML

```xml
<mxfile host="app.diagrams.net">
  <diagram name="architecture" id="arch">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="M1" value="&lt;b&gt;Data Loader&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="160" height="64" as="geometry"/>
        </mxCell>
        <mxCell id="M2" value="&lt;b&gt;Encoder&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="280" y="40" width="160" height="64" as="geometry"/>
        </mxCell>
        <mxCell id="E1" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="M1" target="M2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Fallback Format

```text
NODES:
  N1 [rect, role=data] label="Data Loader" at (col=1, row=1)
  N2 [rect, role=model] label="Encoder" at (col=2, row=1)
EDGES:
  N1 -> N2 solid classic arrow, label=""
LAYOUT:
  column spacing 240 px, row spacing 140 px
```

## Paste Instructions

1. Open app.diagrams.net or draw.io Desktop.
2. Create a blank diagram.
3. Use `Extras -> Edit Diagram...`.
4. Replace all existing XML with the snippet and click OK.
5. Save as `.drawio`; export to PDF or SVG for paper inclusion.
