# Artwork sources

The cover combines `folio-art.png`, a generated material study, with exact editable text in `cover-layout.html`. The two explanatory diagrams have editable SVG editions in the parent directory and separate narrow-screen editions.

To regenerate the HTML and SVG sources, run from the repository root:

```sh
python assets/readme/source/build_artwork.py
```

This build uses only the Python standard library. Open `cover-layout.html` through a local file server and export its 1800 × 800 scene to `../cover.png`. Export desktop diagrams at 1440 × 660 and narrow-screen diagrams at 720 × 1040. Use a browser with the fonts specified in the sources; inspect the result after exporting.

The root README embeds flattened PNG exports so the generated paper material does not depend on a remote image or on SVG raster-image loading. Keep the PNG exports synchronized after editing their sources. The matching material prompt is recorded in `art-direction.txt`.
