# pycon-redux.com

Redux of learnings and talks from PyCon 2022 and onward:
https://pycon-redux.com/

## Website

The website is hosted via [GitHub Pages](https://pages.github.com/).
It was made with the static site generator [Hugo](https://gohugo.io/),
and the theme is [Geekdoc](https://themes.gohugo.io/themes/hugo-geekdoc/)
([GitHub repo](https://github.com/thegeeklab/hugo-geekdoc)).

To download a pre-release of this theme, please follow the
[Geekdocs pre-release download instructions here][1].
Also, check the [Hugo GitHub Actions workflow](.github/workflows/hugo.yaml)
for what to set `$GEEKDOC_VERSION`.

```shell
mkdir -p themes/hugo-geekdoc/
curl -L https://github.com/thegeeklab/hugo-geekdoc/releases/download/v${GEEKDOC_VERSION}/hugo-geekdoc.tar.gz | \
    tar -xz -C themes/hugo-geekdoc/ --strip-components=1
```

## Style

Markdown content in this website are written using [semantic linefeeds][2].

[1]: https://geekdocs.de/usage/getting-started/#option-1-download-pre-build-release-bundle
[2]: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
