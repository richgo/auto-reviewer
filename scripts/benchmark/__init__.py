"""
Benchmark harness for code review skills.

Modules:
- runner: SWE-bench-style benchmark execution
- reporter: Markdown report generation
"""

__all__ = ["BenchmarkRunner", "BenchmarkReporter"]


def __getattr__(name):
    if name == "BenchmarkRunner":
        from .runner import BenchmarkRunner

        return BenchmarkRunner
    if name == "BenchmarkReporter":
        from .reporter import BenchmarkReporter

        return BenchmarkReporter
    raise AttributeError(name)
