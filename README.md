
# froot

Exports your favorite website to your E-reader.


## Examples

To export Innerworth module from Zerodha varsity:

```sh
./froot.py -z https://zerodha.com/varsity/module/innerworth/ -c table.innerworth -a section.chapter-body -o innerworth.epub
```

To export Nithin Kamath's blog:

```sh
./froot.py -z https://nithinkamath.me/blog -c div.posts -i div.post -a div.content -o musings.epub --author "Nithin Kamath" --title "Musings" --page-end 31
```

To export Paul Graham's blog:

```sh
./froot.py -z https://paulgraham.com/articles.html -c table "table:nth-of-type(2)" -a table table -o pg.epub
```
