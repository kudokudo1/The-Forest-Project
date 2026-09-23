from pathlib import Path
import copy
import yaml

from cache import CacheCoordinator, CacheKey


class CapabilityResolutionError(RuntimeError):
    """Forest capability resolution failed."""

    def __init__(
        self,
        message,
        unresolved=None,
    ):
        super().__init__(message)

        self.unresolved = (
            copy.deepcopy(
                unresolved
            )
            if unresolved
            is not None
            else []
        )


class ForestCapabilityResolver:
    """Resolve Forest capabilities through a runtime adapter.

    This layer is deliberately runtime-neutral at the
    canonical level. Forest capability identity comes from
    registry.yaml and Workshop definitions. Runtime-specific
    names come only from adapters/<runtime>.yaml.
    """

    def __init__(
        self,
        forest_root=None,
        cache_coordinator=None,
    ):
        if forest_root is None:
            forest_root = (
                Path(__file__)
                .resolve()
                .parents[1]
            )

        self.forest = Path(
            forest_root
        )

        self.registry_file = (
            self.forest
            / "capabilities"
            / "registry.yaml"
        )

        self.workshop_dir = (
            self.forest
            / "workshops"
        )

        self.adapter_dir = (
            self.forest
            / "adapters"
        )

        self._cache_coordinator = (
            cache_coordinator
            if cache_coordinator is not None
            else CacheCoordinator()
        )

    @staticmethod
    def _load_yaml(path):
        with Path(path).open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = yaml.safe_load(
                handle
            )

        if not isinstance(
            data,
            dict,
        ):
            raise CapabilityResolutionError(
                f"Expected YAML mapping: {path}"
            )

        return data

    @staticmethod
    def _unique(items):
        seen = set()
        result = []

        for item in items:
            item = str(
                item
            ).strip()

            if not item:
                continue

            if item in seen:
                continue

            seen.add(item)
            result.append(item)

        return result

    @staticmethod
    def _selection_list(
        value,
        label,
    ):
        if value is None:
            return []

        if not isinstance(
            value,
            list,
        ):
            raise CapabilityResolutionError(
                f"{label} must be a list."
            )

        return ForestCapabilityResolver._unique(
            value
        )

    def _manifest_cache_identity(
        self,
        path,
    ):
        """Return stable Forest-relative manifest identity."""

        path = Path(path).resolve()

        try:
            relative = path.relative_to(
                self.forest.resolve()
            )

        except ValueError as exc:
            raise CapabilityResolutionError(
                "Resolver manifest is outside "
                "the Forest root: "
                f"{path}"
            ) from exc

        return relative.as_posix()

    @staticmethod
    def _manifest_dependencies(
        path,
    ):
        """Return cheap file-state dependencies."""

        stat = Path(path).stat()

        return {
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }

    def _load_manifest_yaml(
        self,
        path,
    ):
        """Load resolver manifest through Forest cache."""

        path = Path(path)

        # Stat is deliberately cheaper than rereading
        # and reparsing the entire YAML document.
        #
        # If stat itself fails, delegate to the original
        # loader so its existing failure behavior remains.
        try:
            dependencies = (
                self._manifest_dependencies(
                    path
                )
            )

        except OSError:
            return self._load_yaml(
                path
            )

        identity = (
            self._manifest_cache_identity(
                path
            )
        )

        cache_key = CacheKey(
            namespace="forest",
            cache_type="parsed-yaml",
            identity=(
                identity,
            ),
        )

        cached_entry = (
            self._cache_coordinator.get(
                cache_key,
                dependencies=dependencies,
            )
        )

        if cached_entry is not None:
            # Never hand callers the coordinator's
            # authoritative cached object directly.
            return copy.deepcopy(
                cached_entry.value
            )

        parsed = self._load_yaml(
            path
        )

        try:
            after_read = (
                self._manifest_dependencies(
                    path
                )
            )

        except OSError:
            # The source disappeared or became
            # inaccessible after parsing. Re-enter
            # the original loader so we fail according
            # to the actual current source state.
            return self._load_yaml(
                path
            )

        # A manifest changed while we were reading it.
        # Re-read once against the new file state.
        if after_read != dependencies:
            parsed = self._load_yaml(
                path
            )

            try:
                final_dependencies = (
                    self._manifest_dependencies(
                        path
                    )
                )

            except OSError:
                return self._load_yaml(
                    path
                )

            if (
                final_dependencies
                != after_read
            ):
                raise CapabilityResolutionError(
                    "Resolver manifest changed "
                    "repeatedly while being read: "
                    f"{path}"
                )

            after_read = final_dependencies

        self._cache_coordinator.put(
            cache_key,
            copy.deepcopy(
                parsed
            ),
            dependencies=after_read,
            display_name=(
                "Parsed YAML: "
                f"{identity}"
            ),
            metadata={
                "path": identity,
                "format": "yaml",
            },
        )

        # Return another copy so later caller mutation
        # cannot alter the stored cache entry.
        return copy.deepcopy(
            parsed
        )

    def resolve(
        self,
        workshop_id,
        general=None,
        ready=None,
        adapter_name=None,
        require_resolved=True,
    ):
        """Resolve one desired Forest working set.

        No runtime state or Forest state is modified.
        """

        workshop_id = str(
            workshop_id
        ).strip()

        adapter_name = str(
            adapter_name
        ).strip()

        if not workshop_id:
            raise CapabilityResolutionError(
                "Workshop ID cannot be empty."
            )

        if not adapter_name:
            raise CapabilityResolutionError(
                "Adapter name cannot be empty."
            )

        general = self._selection_list(
            general,
            "general",
        )

        ready = self._selection_list(
            ready,
            "ready",
        )

        registry = self._load_manifest_yaml(
            self.registry_file
        )

        workshop_file = (
            self.workshop_dir
            / f"{workshop_id}.yaml"
        )

        if not workshop_file.exists():
            raise CapabilityResolutionError(
                "Unknown Workshop: "
                f"{workshop_id}"
            )

        workshop = self._load_manifest_yaml(
            workshop_file
        )

        adapter_file = (
            self.adapter_dir
            / f"{adapter_name}.yaml"
        )

        if not adapter_file.exists():
            raise CapabilityResolutionError(
                "Unknown runtime adapter mapping: "
                f"{adapter_name}"
            )

        adapter = self._load_manifest_yaml(
            adapter_file
        )

        declared_runtime = adapter.get(
            "runtime"
        )

        if (
            declared_runtime is not None
            and str(declared_runtime)
            != adapter_name
        ):
            raise CapabilityResolutionError(
                "Adapter file runtime mismatch: "
                f"requested {adapter_name!r}, "
                f"file declares "
                f"{declared_runtime!r}."
            )

        capabilities = registry.get(
            "capabilities"
        )

        if not isinstance(
            capabilities,
            dict,
        ):
            raise CapabilityResolutionError(
                "Capability registry is missing "
                "the capabilities mapping."
            )

        general_ready = set(
            self._unique(
                registry.get(
                    "general_ready",
                    [],
                )
            )
        )

        workshop_ready = set(
            self._unique(
                workshop.get(
                    "ready",
                    [],
                )
            )
        )

        invalid_general = [
            name
            for name in general
            if name
            not in general_ready
        ]

        if invalid_general:
            raise CapabilityResolutionError(
                "Capabilities are not in the "
                "General Ready rack: "
                + ", ".join(
                    invalid_general
                )
            )

        invalid_ready = [
            name
            for name in ready
            if name
            not in workshop_ready
        ]

        if invalid_ready:
            raise CapabilityResolutionError(
                "Capabilities are not Ready "
                f"in Workshop {workshop_id!r}: "
                + ", ".join(
                    invalid_ready
                )
            )

        core = self._unique(
            workshop.get(
                "core",
                [],
            )
        )

        active_ids = self._unique(
            core
            + general
            + ready
        )

        sources = []

        for name in active_ids:
            if name in core:
                source = "core"

            elif name in general:
                source = "general"

            else:
                source = "ready"

            sources.append(
                {
                    "canonical_id":
                        name,

                    "source":
                        source,
                }
            )

        tool_map = adapter.get(
            "capabilities",
            {},
        )

        skill_map = adapter.get(
            "skills",
            {},
        )

        unresolved_map = adapter.get(
            "unresolved",
            {},
        )

        if not isinstance(
            tool_map,
            dict,
        ):
            tool_map = {}

        if not isinstance(
            skill_map,
            dict,
        ):
            skill_map = {}

        if not isinstance(
            unresolved_map,
            dict,
        ):
            unresolved_map = {}

        runtime_toolsets = []
        runtime_skills = []
        skill_bindings = []
        unresolved = []

        for name in active_ids:
            definition = capabilities.get(
                name
            )

            if not isinstance(
                definition,
                dict,
            ):
                unresolved.append(
                    {
                        "canonical_id":
                            name,

                        "reason":
                            "not defined in capability registry",
                    }
                )

                continue

            kind = definition.get(
                "kind"
            )

            # ------------------------------------------
            # RUNTIME TRANSPORT
            #
            # Canonical Forest kind and runtime transport
            # are intentionally separate concepts.
            #
            # Examples:
            #
            #   memory
            #     Forest kind: context
            #     Hermes transport: toolset
            #
            #   debugging
            #     Forest kind: skill
            #     Hermes transport: Skill
            #
            # The canonical registry describes what a
            # capability IS. The runtime adapter describes
            # HOW that runtime exposes it.
            # ------------------------------------------

            mapping_problem = None

            if kind == "skill":
                mapping = skill_map.get(
                    name
                )

                if isinstance(
                    mapping,
                    dict,
                ):
                    target = mapping.get(
                        "target"
                    )

                    if (
                        isinstance(
                            target,
                            str,
                        )
                        and target.strip()
                    ):
                        target = target.strip()

                        runtime_skills.append(
                            target
                        )

                        skill_bindings.append(
                            {
                                "canonical_id":
                                    name,

                                "runtime_id":
                                    target,

                                "adapter":
                                    adapter_name,
                            }
                        )

                        continue

                    mapping_problem = (
                        f"{adapter_name} Skill mapping "
                        "has no valid target"
                    )

            else:
                # Non-Skill Forest capabilities may be
                # represented by a runtime toolset even
                # when their canonical kind is something
                # semantic such as "context".
                mapping = tool_map.get(
                    name
                )

                if isinstance(
                    mapping,
                    dict,
                ):
                    runtime_type = mapping.get(
                        "type",
                        "toolset",
                    )

                    if not isinstance(
                        runtime_type,
                        str,
                    ):
                        runtime_type = str(
                            runtime_type
                        )

                    runtime_type = (
                        runtime_type
                        .strip()
                        .lower()
                    )

                    target = mapping.get(
                        "target"
                    )

                    if runtime_type != "toolset":
                        mapping_problem = (
                            f"{adapter_name} capability "
                            f"mapping uses unsupported "
                            f"runtime type "
                            f"{runtime_type!r}"
                        )

                    elif not (
                        isinstance(
                            target,
                            str,
                        )
                        and target.strip()
                    ):
                        mapping_problem = (
                            f"{adapter_name} toolset "
                            "mapping has no valid target"
                        )

                    else:
                        runtime_toolsets.append(
                            target.strip()
                        )

                        continue

            # ------------------------------------------
            # UNRESOLVED
            # ------------------------------------------

            unresolved_definition = (
                unresolved_map.get(
                    name
                )
            )

            if isinstance(
                unresolved_definition,
                dict,
            ):
                reason = (
                    unresolved_definition.get(
                        "reason"
                    )
                    or ""
                )

                reason = " ".join(
                    str(reason).split()
                )

                if not reason:
                    reason = (
                        "adapter marks capability "
                        "as unresolved"
                    )

            elif mapping_problem:
                reason = mapping_problem

            elif kind == "skill":
                reason = (
                    f"no {adapter_name} "
                    "Skill mapping"
                )

            else:
                reason = (
                    f"no verified {adapter_name} "
                    "runtime mapping for Forest "
                    f"capability kind {kind!r}"
                )

            unresolved.append(
                {
                    "canonical_id":
                        name,

                    "kind":
                        kind,

                    "reason":
                        reason,
                }
            )

        runtime_toolsets = (
            self._unique(
                runtime_toolsets
            )
        )

        runtime_skills = (
            self._unique(
                runtime_skills
            )
        )

        result = {
            "schema_version":
                1,

            "tree":
                registry.get(
                    "tree"
                ),

            "workshop": {
                "id":
                    workshop_id,

                "name":
                    workshop.get(
                        "name",
                        workshop_id,
                    ),

                "core":
                    core,

                "ready":
                    self._unique(
                        workshop.get(
                            "ready",
                            [],
                        )
                    ),
            },

            "selection": {
                "general":
                    general,

                "ready":
                    ready,
            },

            "canonical_active_ids":
                active_ids,

            "canonical_sources":
                sources,

            "runtime": {
                "adapter":
                    adapter_name,

                "toolsets":
                    runtime_toolsets,

                "skills":
                    runtime_skills,

                "skill_bindings":
                    skill_bindings,
            },

            "unresolved":
                unresolved,

            "fully_resolved":
                not unresolved,
        }

        if (
            require_resolved
            and unresolved
        ):
            details = "; ".join(
                (
                    f"{item['canonical_id']}: "
                    f"{item['reason']}"
                )
                for item in unresolved
            )

            raise CapabilityResolutionError(
                "Capability resolution "
                "is incomplete: "
                + details,
                unresolved=unresolved,
            )

        return result
