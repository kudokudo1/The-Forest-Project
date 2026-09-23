"""Phase 14.11H.B5 — Colony identifier doctrine certification.

This test is intentionally structural.

It protects the separation between:

tree_id
    durable Tree / Colony identity

execution_context_id
    individual Ortet or Ramet execution context

lineage_role
    Ortet / Ramet origin relationship

operational_role
    current operational responsibility

binding_id
    model/runtime binding identity

session_id
    live runtime session identity

residency_id
    shared immutable model-weight residency identity

It does not inspect or certify transitional H.5 Reasoning state.
"""

import inspect
import unittest
from dataclasses import fields

from colony.identity import ColonyExecutionContext
from runtime.model_residency import SharedModelResidency
from runtime.session_identity import RuntimeSessionIdentity
from runtime.session_store import (
    get_runtime_session_binding,
    set_runtime_session_binding,
)


def field_names(dataclass_type):
    return {
        field.name
        for field in fields(dataclass_type)
    }


class ColonyIdentifierDoctrineTests(unittest.TestCase):
    def test_colony_context_owns_colony_semantics_only(self):
        names = field_names(
            ColonyExecutionContext
        )

        required = {
            "tree_id",
            "execution_context_id",
            "lineage_role",
            "operational_role",
        }

        forbidden = {
            "binding_id",
            "session_id",
            "previous_session_id",
            "residency_id",
            "task_id",
            "reasoning",
            "reasoning_mode",
            "permissions",
            "kv",
        }

        self.assertTrue(
            required.issubset(names)
        )

        self.assertTrue(
            forbidden.isdisjoint(names)
        )

    def test_runtime_session_identity_is_context_plus_binding(self):
        names = field_names(
            RuntimeSessionIdentity
        )

        self.assertTrue(
            {
                "execution_context_id",
                "binding_id",
            }.issubset(names)
        )

        self.assertTrue(
            {
                "tree_id",
                "lineage_role",
                "operational_role",
                "session_id",
                "previous_session_id",
                "residency_id",
                "task_id",
                "reasoning",
                "reasoning_mode",
                "permissions",
                "kv",
            }.isdisjoint(names)
        )

    def test_residency_identity_is_not_context_or_session_identity(self):
        names = field_names(
            SharedModelResidency
        )

        self.assertTrue(
            {
                "binding_id",
                "residency_id",
            }.issubset(names)
        )

        self.assertTrue(
            {
                "tree_id",
                "execution_context_id",
                "lineage_role",
                "operational_role",
                "session_id",
                "previous_session_id",
                "task_id",
                "reasoning",
                "reasoning_mode",
                "permissions",
                "kv",
                "context",
            }.isdisjoint(names)
        )

    def test_colony_roles_do_not_leak_into_runtime_identity(self):
        runtime_names = field_names(
            RuntimeSessionIdentity
        )

        residency_names = field_names(
            SharedModelResidency
        )

        roles = {
            "lineage_role",
            "operational_role",
        }

        self.assertTrue(
            roles.isdisjoint(
                runtime_names
            )
        )

        self.assertTrue(
            roles.isdisjoint(
                residency_names
            )
        )

    def test_session_lookup_requires_context_and_binding(self):
        parameters = inspect.signature(
            get_runtime_session_binding
        ).parameters

        self.assertIn(
            "execution_context_id",
            parameters,
        )

        self.assertIn(
            "binding_id",
            parameters,
        )

    def test_session_write_requires_context_and_binding(self):
        parameters = inspect.signature(
            set_runtime_session_binding
        ).parameters

        self.assertIn(
            "execution_context_id",
            parameters,
        )

        self.assertIn(
            "binding_id",
            parameters,
        )

        self.assertIn(
            "session_id",
            parameters,
        )

    def test_no_identity_object_collapses_all_layers(self):
        colony = field_names(
            ColonyExecutionContext
        )

        runtime = field_names(
            RuntimeSessionIdentity
        )

        residency = field_names(
            SharedModelResidency
        )

        # Tree identity belongs to Colony semantics.
        self.assertIn(
            "tree_id",
            colony,
        )
        self.assertNotIn(
            "tree_id",
            runtime,
        )
        self.assertNotIn(
            "tree_id",
            residency,
        )

        # Binding belongs to runtime/residency semantics,
        # not Colony semantic identity.
        self.assertNotIn(
            "binding_id",
            colony,
        )
        self.assertIn(
            "binding_id",
            runtime,
        )
        self.assertIn(
            "binding_id",
            residency,
        )

        # Execution context participates in Colony identity
        # and runtime-session identity, but never residency.
        self.assertIn(
            "execution_context_id",
            colony,
        )
        self.assertIn(
            "execution_context_id",
            runtime,
        )
        self.assertNotIn(
            "execution_context_id",
            residency,
        )

        # Residency identity belongs only to shared weights.
        self.assertNotIn(
            "residency_id",
            colony,
        )
        self.assertNotIn(
            "residency_id",
            runtime,
        )
        self.assertIn(
            "residency_id",
            residency,
        )


if __name__ == "__main__":
    unittest.main()
