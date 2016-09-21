## TinCanPython Project Website

### API Doc Generation

To automatically generate documentation, at the root of the repository run,

    sphinx-apidoc -f -o ./docs/source/ tincan/

Then from the `docs/` directory run,

    make html

The docs will be output to `docs/build/html/`.

If you would like to change the names of each section, you can do so by modifying `docs/source/tincan.rst`.

### Local Site Development

With Bundler (http://bundler.io - a Ruby project) installed, the site can be rendered locally using Jekyll with:

    bundle exec jekyll serve --baseurl='/TinCanPython'
