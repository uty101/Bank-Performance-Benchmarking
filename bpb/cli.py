"""Command line entry point. The commands are built in Section 6 of PLAN.md."""

USAGE = """usage: bpb <command> [args]

commands:
  build               rebuild every output from raw files
  trace <lineage_id>  print the chain behind a figure
  bank <bank_id>      build one bank profile
"""


def main(argv: list[str] | None = None) -> int:
    print(USAGE, end="")
    return 0
