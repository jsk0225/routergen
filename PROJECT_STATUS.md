# RouterGen Project Status

**Project stage:** Pre-alpha
**Development line:** v0.2
**Current phase:** v0.2-A, Read-Only Architecture
**Current milestone:** v0.2-A2, Topology/Schema and Semantic-Validation Framework (next)
**Last completed milestone:** v0.2-A1, Project and Bootstrap, **COMPLETE**
**Last updated:** 2026-11-25
**Network changes permitted in v0.2-A:** No

---

## 1. Status Summary

RouterGen is a safety-first topology compiler for creating reproducible Linux and WSL2 router environments from declarative topology definitions.

The v0.2 development line is in **v0.2-A**, establishing the complete read-only pipeline before any network mutation functionality is allowed.

```text
Topology
  |
  v
Schema Validation
  |
  v
Host Discovery
  |
  v
Resolution
  |
  v
Semantic Validation
  |
  v
Deterministic Planning
  |
  v
STOP
```

The entire v0.2-A phase must make **zero network configuration changes**.

### Current position

v0.2-A1 was implemented on `feature/v0.2-a1-bootstrap`, tested in GitHub Codespaces and on the physical WSL2 test laptop, and verified with 7/7 automated tests and passing read-only diagnostics in each environment. Its verification evidence was committed on the feature branch as `88523a9`.

**Pull Request #1 was merged into `main`** at commit `547bb56b770a804c02a950a02fc763d992b4b054`. Both Codespaces and the WSL2 test laptop subsequently synchronized to this exact commit, had clean working trees, and passed post-merge regression tests and diagnostics. **A1 is COMPLETE.**

Next development milestone: **v0.2-A2**, topology/schema and semantic-validation framework. The A1 closure documentation update itself must be reviewed and committed separately; it does not change the already verified A1 code baseline.

---

## 2. Current State at a Glance

| Area | Status | Notes |
|---|---|---|
| Project purpose | Defined | Safety-first topology compiler for Linux router environments |
| v0.2 data model | Frozen for v0.2-A | Host, router, interface, bridge, SVI, transport, optional FRR intent |
| JSON Schema architecture | Defined | Structural validation belongs in JSON Schema |
| Semantic-validation architecture | Defined | Cross-object and host-dependent validation outside JSON Schema |
| Host-discovery architecture | Defined | Structured `ip -j` / `bridge -j` data preferred |
| Configuration precedence | Frozen | CLI > prompt > profile > topology default > RouterGen default |
| Read-only planning architecture | Defined | Deterministic, non-mutating plans |
| A1 implementation | **COMPLETE** | PR #1 merged; Codespaces and WSL2 each 7/7 PASS on merged `main` |
| A2 implementation | Not started | Next development milestone |
| Network apply | Not implemented | Explicitly outside v0.2-A |
| Reconciliation | Design defined | Not implemented |
| Post-apply validation | Planned | Later lifecycle |
| FRR lifecycle | Design defined | Must follow successful network-underlay validation |
| Production readiness | No | Project remains pre-alpha |

---

## 3. Historical Prototype Baseline

Before the current GitHub-based RouterGen implementation, the earlier `wsl2-router-netgen` prototype achieved:

```text
12 PASS
0 FAIL
```

This is **historical prototype evidence**, not the current GitHub RouterGen test suite. The current RouterGen implementation has its own automated baseline established during v0.2-A1. Any prototype behavior carried into the current codebase should receive current RouterGen tests.

---

## 4. Current GitHub Test Baseline

**Authoritative branch:** `main`
**Merged A1 commit:** `547bb56b770a804c02a950a02fc763d992b4b054`

A1 history:

```text
a9a3204 feat: add RouterGen v0.2-A1 bootstrap foundation
f5972dc build: add reproducible development bootstrap
88523a9 docs: record v0.2-A1 verification status
547bb56 Merge pull request #1 from jsk0225/feature/v0.2-a1-bootstrap
```

**Post-merge automated baseline, each environment:**

```text
7 PASS
0 FAIL
```

The current suite covers package version, CLI parser construction, CLI baseline execution, successful environment-diagnostic evaluation, missing-required-command failure, non-Linux failure, and read-only safety reporting.

---

## 5. v0.2-A Milestones

| Milestone | Description | Status |
|---|---|---|
| A1 | Project/bootstrap | **COMPLETE: merged and cross-environment verified** |
| A2 | Topology/schema + semantic-validation framework | Not started; next |
| A3 | Structured host discovery | Planned |
| A4 | Resolution, profiles, prompts, and precedence | Planned |
| A5 | Deterministic read-only planning | Planned |

---

# 6. Completed Milestone: v0.2-A1

## 6.1 Objective

Establish a clean, reproducible RouterGen development and execution environment without modifying host networking.

## 6.2 Implemented

- Python package structure under `src/routergen` and `pyproject.toml` packaging.
- Editable development installation, dedicated RouterGen `.venv`, and development dependencies.
- RouterGen CLI entry point: `routergen --help`, `routergen --version`, `routergen diagnose`.
- Linux and WSL detection; virtual-environment reporting.
- Required external-command discovery: `ip`, `bridge`, `sysctl`, `ss`.
- Automated pytest framework and explicit read-only safety reporting.
- Reproducible development bootstrap; fresh `.venv` creation and repeat/idempotent bootstrap verified.

The diagnostic reports:

```text
FINAL_RESULT=PASS|FAIL
NETWORK_CHANGES_PERMITTED=NO
```

A1 does not contain network apply functionality.

## 6.3 Reproducible Bootstrap

Script: `scripts/bootstrap-dev.sh`

```text
Check Python >= 3.10
  |
  v
Create/reuse .venv
  |
  v
Install RouterGen + development dependencies
  |
  v
Run automated tests
  |
  v
Run read-only environment diagnostics
```

Run:

```bash
./scripts/bootstrap-dev.sh
```

The caller's shell need not have the RouterGen virtual environment activated.

## 6.4 Codespaces Verification

**Post-merge verification:** branch `main`, commit `547bb56b770a804c02a950a02fc763d992b4b054`; clean working tree; local `HEAD` matched `origin/main`.

```text
Platform: GitHub Codespaces / Linux
Python: 3.14.2
RouterGen: 0.2.0.dev0
Virtual environment: /workspaces/routergen/.venv
WSL: no
ip PASS
bridge PASS
sysctl PASS
ss PASS
Tests: 7 PASS / 0 FAIL
FINAL_RESULT=PASS
NETWORK_CHANGES_PERMITTED=NO
```

Fresh virtual-environment creation and repeat/idempotent bootstrap were verified during A1 development. Generated `.venv`, Python-cache, pytest-cache, and package-build artifacts remain excluded from Git.

## 6.5 WSL2 Test-Laptop Verification

**Post-merge verification:** branch `main`, commit `547bb56b770a804c02a950a02fc763d992b4b054`; clean working tree; local `HEAD` matched `origin/main`.

```text
Checkout: /mnt/c/Project/routergen
Platform: Linux / WSL2
Kernel: 6.18.58.1-microsoft-standard-WSL2
Python: 3.12.3
RouterGen: 0.2.0.dev0
Virtual environment: /mnt/c/Project/routergen/.venv
WSL: yes
ip PASS
bridge PASS
sysctl PASS
ss PASS
Tests: 7 PASS / 0 FAIL
FINAL_RESULT=PASS
NETWORK_CHANGES_PERMITTED=NO
```

The RouterGen environment is separate from the existing OSPF Alt project environment. No OSPF Alt namespace, FRR pathspace, route, bridge, VLAN, interface, or other network configuration was intentionally modified by A1 verification.

## 6.6 A1 Acceptance Criteria

- [x] RouterGen installs into its own `.venv`, separate from OSPF Alt.
- [x] Editable install and CLI startup work.
- [x] `routergen --help`, `routergen --version`, and `routergen diagnose` work.
- [x] Linux and WSL detection work where applicable.
- [x] Required external commands are detected.
- [x] Missing-command and non-Linux failure behavior are covered by tests.
- [x] Fresh and repeated bootstrap verified.
- [x] Automated tests pass in Codespaces and on the WSL2 laptop.
- [x] Diagnostics explicitly prohibit network changes.
- [x] A1 performs no intentional network configuration changes.
- [x] A1 verification evidence committed to `PROJECT_STATUS.md` on feature branch (`88523a9`).
- [x] A1 Pull Request #1 reviewed and merged into `main`.
- [x] Codespaces `main` synchronized after merge.
- [x] WSL2 test checkout synchronized with merged `main`.
- [x] Post-merge tests and diagnostics passed in both environments at identical commit `547bb56`.

**A1 status: COMPLETE.** This post-merge closure record is a subsequent documentation update, not part of the original merge commit.

---

# 7. v0.2 Architecture Invariants

Detailed architecture: `docs/architecture/architecture.md`. `PROJECT_STATUS.md` records implementation status rather than duplicating the architecture specification.

- Logical topology is separate from discovered host state.
- Host discovery occurs before host-dependent resolution.
- Missing configured host interfaces are never silently substituted.
- Each attachment represents one logical Layer-2 segment and uses a dedicated bridge.
- Separate point-to-point VLANs must not be merged through a shared bridge.
- Router-interface addressing and host-SVI addressing are independent; each supports `none`, `static`, or `dhcp`.
- VLAN `parent_role` resolves to an actually detected host device.
- Configuration-source precedence is deterministic and resolved values retain provenance.
- Read-only planning is separate from apply; identical normalized inputs produce deterministic plans.
- Reconciliation preserves unchanged resources and distinguishes RouterGen-owned from externally managed resources.
- Network-underlay validation must pass before FRR lifecycle operations.
- Each logical router must use an independent FRR pathspace.

Any change to these invariants requires an explicit architecture decision.

---

# 8. Configuration Precedence

Frozen v0.2 precedence:

```text
CLI override
  >
interactive answer
  >
saved host/router profile
  >
topology JSON default
  >
RouterGen default
```

The future resolver must retain provenance of each resolved value.

---

# 9. Validation Model

RouterGen separates validation into three layers.

## 9.1 Schema Validation

JSON Schema handles structural constraints: required objects/fields, types, enumerations, permitted addressing modes, permitted transport types, identifier formatting, and expressible value ranges.

## 9.2 Semantic Validation

Semantic validation handles router identity and namespace uniqueness; FRR pathspace uniqueness; valid object references; interface uniqueness; bridge ownership; VLAN consistency; addressing conflicts; transport-specific rules; host-role resolution; generated-name collisions; and prevention of unintended Layer-2 merging.

## 9.3 Operational Validation

Later lifecycle stages validate actual namespace existence, interface creation, link state, bridge membership, VLAN state, addressing, routes, policy rules, connectivity, and FRR/routing-protocol state.

---

# 10. v0.2-A Hard Gate

RouterGen must not begin v0.2-B apply lifecycle until this pipeline is proven:

```text
Logical topology
 +
Actual host discovery
 +
Optional saved profile
 +
CLI overrides / user selections
 |
 v
Fully resolved router
 |
 v
Schema validation PASS
 |
 v
Semantic validation PASS
 |
 v
Deterministic plan
 |
 v
ZERO NETWORK CHANGES
```

- [ ] Topology structurally valid.
- [ ] Topology semantically valid.
- [ ] Required host devices actually detected.
- [ ] Every required host role resolved.
- [ ] Every selected router interface fully resolved.
- [ ] Every attachment mapped to the correct dedicated Layer-2 bridge.
- [ ] Every non-staged transport fully resolved.
- [ ] Addressing intent unambiguous.
- [ ] Provenance of resolved values retained.
- [ ] Identical normalized inputs produce the same plan.
- [ ] Plan ordering deterministic.
- [ ] No network or routing state changed.
- [ ] Consolidated verification evidence produced.

Passing this gate allows work on v0.2-B to begin; it does not make RouterGen production ready.

---

# 11. Remaining v0.2-A Work

## A2: Topology/schema + semantic validation

Planned: v0.2 topology model, JSON Schema, topology loader, normalized internal representation, schema-validation reporting, semantic-validation framework, initial semantic rule set.

## A3: Structured Host Discovery

Read-only sources planned:

```bash
ip -j link show
ip -j addr show
ip -j route show
ip -j rule show
bridge -j link show
bridge -j vlan show
```

## A4: Resolution

Planned: saved host/router profiles, interactive selection, non-interactive operation, CLI overrides, precedence processing, role-to-device mapping, provenance, unresolved-value reporting, and fully resolved router representation.

## A5: Deterministic Planning

The planning layer describes proposed changes without executing them. Example **plan records only**:

```text
CREATE namespace r1
CREATE bridge br-r1-mgmt
CREATE veth pair
MOVE router peer into namespace r1
ATTACH host peer to bridge br-r1-mgmt
CREATE VLAN transport
ASSIGN router address
LEAVE bridge SVI unnumbered
```

These records are data, not authorization to execute networking commands during v0.2-A.

---

# 12. Out of Scope for v0.2-A

Network apply; namespace creation/deletion; bridge creation/deletion; veth or VLAN creation; address, route, or policy-rule modification; forwarding or firewall/nftables changes; persistence configuration; FRR configuration generation or startup/shutdown; OSPF or BGP configuration; destructive reconciliation; rollback execution; multi-host orchestration; remote deployment; and production appliance packaging.

Architecture documentation may discuss these capabilities, but they must not be presented as implemented.

---

# 13. Known Limitations

- RouterGen remains pre-alpha. Only A1 of v0.2-A has been implemented and merged.
- The current automated GitHub RouterGen suite contains seven tests.
- A2 topology/schema, A3 host discovery, A4 resolution, and A5 planning have not been implemented.
- Network apply is intentionally unavailable.
- DHCP behavior has not been implemented or operationally validated.
- Host-routed transport has not been operationally implemented.
- External-bridge lifecycle/ownership handling has not been implemented.
- FRR intent is architectural; FRR lifecycle management is not implemented.
- Multi-host orchestration, rollback/recovery, and restart persistence are not implemented.
- Production security and privilege-separation review is incomplete.

Host-interface observations from a particular machine are discovered host state, not permanent RouterGen limitations.

---

# 14. Safety Rules

- Never silently replace a missing configured interface.
- Never treat an example topology as approved for the current host.
- Never execute apply behavior from a read-only command.
- Never merge independent Layer-2 segments merely because they share a transport device.
- Never infer host-SVI addressing from router-interface addressing, or vice versa.
- Never begin FRR lifecycle operations before successful underlay validation.
- Never reuse an FRR pathspace between different logical routers.
- Never delete resources RouterGen does not own.
- Never describe design-defined capability as implemented or implementation as lab-verified without evidence.
- Never weaken tests merely to make new implementation work.
- Never execute a plan merely because planning succeeded.
- Never substitute a detected interface for a missing configured device without explicit resolution.
- Never perform network mutation during v0.2-A.

---

# 15. Stability Definitions

**Design Defined:** Architecture and intended behavior documented.

**Implemented:** Capability exists in code.

**Deterministically Tested:** Automated tests demonstrate repeatable behavior without live network changes.

**Lab Verified:** Capability exercised in intended controlled environment with recorded passing evidence.

**Stable:** Additionally requires documented behavior and failure behavior, regression coverage, appropriate integration/lab verification, lifecycle consideration, and no known critical safety defect.

**Production Ready:** Additionally requires security review, privilege/ownership controls, recovery, rollback, supported install/upgrade, operational documentation, monitoring, and explicit support policy.

No RouterGen capability is currently production ready.

---

# 16. Evidence Policy

Milestone evidence should establish RouterGen version, Git commit, topology/schema version where applicable, environment, Python version, tests, safety result, failure stage where applicable, whether mutation was permitted, and whether mutation occurred.

Preferred consolidated result markers:

```text
FINAL_RESULT=PASS
FAILURE_STAGE=NONE
NETWORK_CHANGES_PERMITTED=NO
NETWORK_CHANGES_DETECTED=NO
```

**Evidence distinction:** The A1 diagnostic explicitly reported `FINAL_RESULT=PASS` and `NETWORK_CHANGES_PERMITTED=NO`. The other markers above are **future preferred wrapper markers**, not claims that the A1 diagnostic emitted them. A future verification wrapper should consolidate evidence into one result file where practical.

---

# 17. Branch and Change Discipline

`main` is authoritative. A1's `feature/v0.2-a1-bootstrap` was merged through PR #1. Future milestone branches are planned, not asserted to exist:

```text
main
  +-- feature/v0.2-a1-bootstrap (merged via PR #1)
  +-- feature/v0.2-a2-schema (planned)
  +-- feature/v0.2-a3-discovery (planned)
  +-- feature/v0.2-a4-resolution (planned)
  +-- feature/v0.2-a5-planning (planned)
```

Recommended commit prefixes: `feat:`, `fix:`, `test:`, `docs:`, `build:`, `refactor:`.

Before merging each new milestone:

- [ ] Current and milestone-specific tests pass.
- [ ] Applicable safety gates pass.
- [ ] Lab verification completed where required.
- [ ] Documentation describes actual behavior, not planned behavior as implemented.
- [ ] `PROJECT_STATUS.md` updated.
- [ ] Pull Request reviewed.

This checklist is for **future milestones**; it does not reopen completed A1 gates.

---

# 18. Decision Summary

| Decision | Status | Rationale |
|---|---|---|
| Declarative topology JSON | Accepted | Separates portable intent from host implementation |
| Discover host before resolution | Accepted | Prevents hard-coded interface assumptions |
| Dedicated bridge per logical L2 segment | Accepted | Preserves Layer-2 isolation |
| Router and host-SVI addressing remain independent | Accepted | Supports numbered and unnumbered designs |
| Explicit configuration precedence | Accepted | Makes resolution predictable |
| Missing configured devices are rejected | Accepted | Prevents unsafe silent substitution |
| Plan before apply | Accepted | Creates safety/review boundary |
| Reconcile only relevant changed resources | Accepted | Avoids unnecessary disruption |
| FRR lifecycle follows underlay validation | Accepted | Prevents daemons starting on invalid networking |
| One FRR pathspace per router | Accepted | Isolates logical routers |
| Semantic validation outside JSON Schema | Accepted | Supports cross-object and host-dependent rules |

Detailed architecture decisions belong in `docs/architecture/` and may later be promoted to ADR files.

---

# 19. Next Action

**A1 implementation and verification are complete.** The remaining administrative action is to commit and review this post-merge status-documentation update without rewriting A1's historical merge.

Recommended repository workflow:

1. In **Codespaces**, start from clean, up-to-date `main` at `547bb56` and create a documentation branch.
2. Replace `PROJECT_STATUS.md` with this updated file; review the diff and run `git diff --check` and the seven tests.
3. Commit and push the documentation branch; review and merge its Pull Request.
4. Synchronize both Codespaces and WSL2 `main` again to the new documentation commit.
5. Begin **v0.2-A2** on its own feature branch, with zero network changes.

---

# 20. Completion Record

## Historical `wsl2-router-netgen` baseline

```text
Status: VERIFIED HISTORICAL PROTOTYPE
Tests: 12 PASS / 0 FAIL
Scope: Earlier validation/read-only planning prototype
Relationship to current suite: Historical evidence, not current GitHub tests
```

## v0.2-A1

```text
Status: COMPLETE
Pull Request: #1, MERGED
Authoritative merged main commit:
547bb56b770a804c02a950a02fc763d992b4b054

Feature branch: feature/v0.2-a1-bootstrap
Implementation commits: a9a3204, f5972dc
Feature status evidence commit: 88523a9

Codespaces:
Branch: main
Commit: 547bb56
Git working tree: CLEAN
Python: 3.14.2
RouterGen: 0.2.0.dev0
Tests: 7 PASS / 0 FAIL
Diagnostic: PASS
WSL: no

WSL2 test laptop:
Checkout: /mnt/c/Project/routergen
Branch: main
Commit: 547bb56
Git working tree: CLEAN
Python: 3.12.3
RouterGen: 0.2.0.dev0
Tests: 7 PASS / 0 FAIL
Diagnostic: PASS
WSL: yes

Both environments synchronized to the same main commit: YES
NETWORK_CHANGES_PERMITTED=NO
```

## v0.2-A2

```text
Status: NOT STARTED
Network changes permitted: No
```

## v0.2-A3

```text
Status: PLANNED
Network changes permitted: No
```

## v0.2-A4

```text
Status: PLANNED
Network changes permitted: No
```

## v0.2-A5

```text
Status: PLANNED
Network changes permitted: No
```
