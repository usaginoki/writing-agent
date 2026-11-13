"""Format conversion via pandoc (pypandoc-binary bundles it). Run inside the uv env.

  convert.py to-md <in.docx|in.tex|...> <out.md>      import for editing
  convert.py to-docx <in.md> <out.docx> [--ref <original.docx>]
      export; --ref reuses the original's styles so the revised docx looks like the original.
The original docx is never overwritten: the writer exports <name>.revised.docx next to it.
"""

import sys

import pypandoc


def main() -> None:
    cmd, src, dst, *rest = sys.argv[1:]
    if cmd == "to-md":
        pypandoc.convert_file(src, "gfm", outputfile=dst, extra_args=["--wrap=none"])
    elif cmd == "to-docx":
        extra = ["--reference-doc", rest[1]] if rest[:1] == ["--ref"] else []
        pypandoc.convert_file(src, "docx", outputfile=dst, extra_args=extra)
    else:
        sys.exit(__doc__)
    print(dst)


if __name__ == "__main__":
    main()
