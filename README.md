# MSOS searcher

A half-hearted attempt at finding (or rather searching) a MSOS (Magic Square of Squares)
in the spirit of the Parker Square.

## Running

I recommend running it with [pypy](pypy.org) for [obvious reasons](https://speed.pypy.org/)
if not even going ahead and porting it to C++.

```bash
pypy search_square.py
```

Fiddle around with N and the number of parallel workers as you please.
On my machine I got to around N=2000.

## Documentation

The code is the documentation.

## License

This code is licensed under [WTFPL](http://www.wtfpl.net/).