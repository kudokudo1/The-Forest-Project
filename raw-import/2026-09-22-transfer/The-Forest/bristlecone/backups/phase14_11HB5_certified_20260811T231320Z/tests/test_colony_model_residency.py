import unittest
from dataclasses import FrozenInstanceError

from runtime.model_residency import (
    MODEL_RESIDENCY_SCHEMA_VERSION,
    ModelResidencyError,
    SharedModelResidency,
    residency_supports_session_identity,
)
from runtime.session_identity import (
    RuntimeSessionIdentity,
)


class SharedModelResidencyTests(unittest.TestCase):

    def setUp(self):
        self.residency = SharedModelResidency(
            residency_id="resident-small-1",
            binding_id="binding-0001",
            adapter="hermes",
        )

    def test_same_residency_supports_different_contexts(self):
        context_a = RuntimeSessionIdentity(
            execution_context_id="ctx-A",
            binding_id="binding-0001",
        )

        context_b = RuntimeSessionIdentity(
            execution_context_id="ctx-B",
            binding_id="binding-0001",
        )

        self.assertNotEqual(
            context_a.execution_context_id,
            context_b.execution_context_id,
        )

        self.assertTrue(
            residency_supports_session_identity(
                self.residency,
                context_a,
            )
        )

        self.assertTrue(
            residency_supports_session_identity(
                self.residency,
                context_b,
            )
        )

    def test_different_binding_is_not_supported(self):
        other = RuntimeSessionIdentity(
            execution_context_id="ctx-A",
            binding_id="binding-0002",
        )

        self.assertFalse(
            residency_supports_session_identity(
                self.residency,
                other,
            )
        )

    def test_residency_contains_no_session_or_context_identity(self):
        fields = set(
            SharedModelResidency.__dataclass_fields__
        )

        forbidden = {
            "tree_id",
            "execution_context_id",
            "task_id",
            "session_id",
            "previous_session_id",
            "lineage_role",
            "operational_role",
            "reasoning_mode",
            "permissions",
            "kv",
            "context",
        }

        self.assertTrue(
            forbidden.isdisjoint(fields)
        )

    def test_residency_is_frozen(self):
        with self.assertRaises(
            FrozenInstanceError
        ):
            self.residency.binding_id = "binding-0002"

    def test_required_fields_fail_closed(self):
        with self.assertRaises(
            ModelResidencyError
        ):
            SharedModelResidency(
                residency_id="",
                binding_id="binding-0001",
                adapter="hermes",
            )

        with self.assertRaises(
            ModelResidencyError
        ):
            SharedModelResidency(
                residency_id="resident-1",
                binding_id="",
                adapter="hermes",
            )

        with self.assertRaises(
            ModelResidencyError
        ):
            SharedModelResidency(
                residency_id="resident-1",
                binding_id="binding-0001",
                adapter="",
            )

    def test_schema_version_is_exact(self):
        self.assertEqual(
            self.residency.schema_version,
            MODEL_RESIDENCY_SCHEMA_VERSION,
        )

        with self.assertRaises(
            ModelResidencyError
        ):
            SharedModelResidency(
                residency_id="resident-1",
                binding_id="binding-0001",
                adapter="hermes",
                schema_version=2,
            )

    def test_compatibility_requires_typed_session_identity(self):
        with self.assertRaises(
            ModelResidencyError
        ):
            residency_supports_session_identity(
                self.residency,
                {
                    "execution_context_id": "ctx-A",
                    "binding_id": "binding-0001",
                },
            )


if __name__ == "__main__":
    unittest.main()
