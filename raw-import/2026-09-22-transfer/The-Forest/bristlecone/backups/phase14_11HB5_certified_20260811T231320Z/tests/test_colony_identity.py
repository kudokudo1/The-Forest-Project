import unittest
from dataclasses import FrozenInstanceError

from colony import (
    COLONY_IDENTITY_SCHEMA_VERSION,
    ColonyExecutionContext,
    ColonyIdentityError,
)


class ColonyExecutionContextTests(unittest.TestCase):

    def test_ortet_does_not_imply_main(self):
        context = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-a",
            lineage_role="ortet",
            operational_role="worker",
        )

        self.assertEqual(
            context.lineage_role,
            "ortet",
        )
        self.assertEqual(
            context.operational_role,
            "worker",
        )

    def test_ramet_may_be_main(self):
        context = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-b",
            lineage_role="ramet",
            operational_role="main",
        )

        self.assertEqual(
            context.lineage_role,
            "ramet",
        )
        self.assertEqual(
            context.operational_role,
            "main",
        )

    def test_same_tree_can_have_distinct_contexts(self):
        ortet = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-a",
            lineage_role="ortet",
            operational_role="worker",
        )

        ramet = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-b",
            lineage_role="ramet",
            operational_role="main",
        )

        self.assertEqual(
            ortet.tree_id,
            ramet.tree_id,
        )
        self.assertNotEqual(
            ortet.execution_context_id,
            ramet.execution_context_id,
        )

    def test_runtime_identity_fields_are_excluded(self):
        fields = set(
            ColonyExecutionContext.__dataclass_fields__
        )

        forbidden = {
            "binding_id",
            "session_id",
            "adapter",
            "model_form",
            "reasoning_mode",
            "permissions",
        }

        self.assertTrue(
            forbidden.isdisjoint(fields)
        )

    def test_identity_is_frozen(self):
        context = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-a",
            lineage_role="ortet",
            operational_role="main",
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            context.tree_id = "tree-b"

    def test_whitespace_is_normalized(self):
        context = ColonyExecutionContext(
            tree_id=" tree-a ",
            execution_context_id=" ctx-a ",
            lineage_role=" RAMET ",
            operational_role=" main ",
        )

        self.assertEqual(
            context.tree_id,
            "tree-a",
        )
        self.assertEqual(
            context.execution_context_id,
            "ctx-a",
        )
        self.assertEqual(
            context.lineage_role,
            "ramet",
        )
        self.assertEqual(
            context.operational_role,
            "main",
        )

    def test_invalid_lineage_role_fails_closed(self):
        with self.assertRaises(
            ColonyIdentityError
        ):
            ColonyExecutionContext(
                tree_id="tree-a",
                execution_context_id="ctx-a",
                lineage_role="main",
                operational_role="main",
            )

    def test_empty_required_identity_fails_closed(self):
        with self.assertRaises(
            ColonyIdentityError
        ):
            ColonyExecutionContext(
                tree_id="",
                execution_context_id="ctx-a",
                lineage_role="ortet",
                operational_role="main",
            )

        with self.assertRaises(
            ColonyIdentityError
        ):
            ColonyExecutionContext(
                tree_id="tree-a",
                execution_context_id="",
                lineage_role="ortet",
                operational_role="main",
            )

    def test_schema_version_is_exact(self):
        context = ColonyExecutionContext(
            tree_id="tree-a",
            execution_context_id="ctx-a",
            lineage_role="ortet",
            operational_role="main",
        )

        self.assertEqual(
            context.schema_version,
            COLONY_IDENTITY_SCHEMA_VERSION,
        )

        with self.assertRaises(
            ColonyIdentityError
        ):
            ColonyExecutionContext(
                tree_id="tree-a",
                execution_context_id="ctx-a",
                lineage_role="ortet",
                operational_role="main",
                schema_version=2,
            )


if __name__ == "__main__":
    unittest.main()
