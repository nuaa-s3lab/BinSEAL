# DATA Segment infector

## Usage

``` bash
make
./bin/infector <infected-file> <output-file>
```

* Locate the data segment
  * Increase p_filesz to account for the new code and .bss
  * Increase p_memsz to account for the new code
* For each phdr who's segment is after the insertion (text segment)
  * increase p_offset to reflect the new position after insertion
* For each shdr who's section resides after the insertion
  * Increase sh_offset to account for the new code
  * Increase sh_addr to account for the new code
* Physically insert the new code into the file

## References

[UNIX VIRUSES](https://www.win.tue.nl/~aeb/linux/hh/virus/unix-viruses.txt)

Ryan O'Neill: Learning Linux Binary Analysis, Page 104-105
