# The Sparkdown specification

## Must be backwards-compatible with Markdown.
A nebulous standard of its own, but we can try.

## Modern web-aware
HTML generated from Sparkdown must have context-aware classes for CSS and IDs for flexible styling. Fonts can be inferred from the Sparkdown. Interactions through CSS or JavaScript are implied by semantics. Template the skeleton, then use `includes` for individual page content.
  
## Socially responsible
That is, social media is its own thing.
- Validation of social media handles
- Optional embed of Tweets, etc
`T@username` becomes `<a href="//twitter.com/username" class="twitter-handle">@username</a>`
`F@username` becomes `<a href="//facebook.com/username" class="facebook-handle">username on Facebook<a>`

## Rich media
Embedding audio, video is easy and context-aware.

- Video-embed is identical to image embed. Specify source of non-OC to get API for embed.
- Embed audio: `"[//path/to/audio]"`
- Interview block-quote with original audio: `"<Quotation text>[//path/to/audio] - Person who said it"`

## Interactive data and visualization
The modern world is the data world. There should be no barrier to presenting raw data, so basic visualizations should be generated automatically. Source data structure types (CSV, JSON, etc) should be inferred automatically. The embedded SVG must be fully marked-up with classes and IDs.

- Bar charts: `||[//path/to/data/file](libraryToUse.js)||`
- Pie charts: `oo[//path/to/data/file](d3.js)oo`
- Scatter plots: `....[//path/to/data/file](libraryToUse.js){facets, for, interaction}....`
- Custom include: @@[path/to/html]@@
