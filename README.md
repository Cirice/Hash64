### Hash64

A class for reading content of an ES index into a Pandas DataFrame (written  in  Python 3)

#### Introduction

Nilsima (a locality sensetive hashing function) in Python 3. For more info please see: [Nilsima](https://en.wikipedia.org/wiki/Nilsimsa_Hash).

#### Prerequisites

 No requirements needed, for an example on how to run the code, have a look at  `main.py`.

#### API and usage

```
from src.string_to_hash import Hash64

if __name__ == "__main__":

    hash_generator = Hash64()
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy")))
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy / ")))


```

For more info use `help(Hash64)`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the `CHANGELOG.MD`.

