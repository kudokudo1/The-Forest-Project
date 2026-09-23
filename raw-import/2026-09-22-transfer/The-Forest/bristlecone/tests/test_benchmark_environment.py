"""Phase 14.11L.0 passive environment tests."""

import unittest

from benchmarks.environment import (
    parse_llama_server_pids,
    parse_mem_available_kib,
    parse_ollama_resident_models,
    parse_systemctl_properties,
)


class BenchmarkEnvironmentTests(
    unittest.TestCase
):

    def test_mem_available(
        self,
    ):
        self.assertEqual(
            parse_mem_available_kib(
                "MemTotal: 1000 kB\n"
                "MemAvailable: 750 kB\n"
            ),
            750,
        )

    def test_systemctl_properties(
        self,
    ):
        value = (
            parse_systemctl_properties(
                "ActiveState=active\n"
                "SubState=running\n"
                "MainPID=941\n"
            )
        )

        self.assertEqual(
            value,
            {
                "ActiveState": "active",
                "SubState": "running",
                "MainPID": "941",
            },
        )

    def test_empty_ollama_ps(
        self,
    ):
        value = (
            parse_ollama_resident_models(
                "NAME    ID    SIZE    "
                "PROCESSOR    CONTEXT    UNTIL\n"
            )
        )

        self.assertEqual(
            value,
            (),
        )

    def test_resident_ollama_models(
        self,
    ):
        value = (
            parse_ollama_resident_models(
                "NAME ID SIZE PROCESSOR CONTEXT UNTIL\n"
                "model-a abc 1GB 100%CPU 4096 5m\n"
                "model-b def 2GB 100%CPU 8192 5m\n"
            )
        )

        self.assertEqual(
            value,
            (
                "model-a",
                "model-b",
            ),
        )

    def test_llama_server_pids(
        self,
    ):
        value = (
            parse_llama_server_pids(
                "101 python something.py\n"
                "202 /usr/bin/llama-server --port 1234\n"
                "303 another-process\n"
            )
        )

        self.assertEqual(
            value,
            (202,),
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
