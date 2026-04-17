# Registrations INDEX — Template

**How to use this template**: copy this file to `docs/eureka/registrations/INDEX.md` in your project repo when you start using `eureka:hypothesis-first`. The skill will maintain it thereafter.

---

# Registrations INDEX

**Purpose**: machine-readable index of all hypothesis registrations and their lifecycle states. Maintained by `eureka:hypothesis-first`. See `docs/references/registration-lifecycle.md` for the conventions this index follows.

**When to read**: when you need to know which registration is authoritative for a given study, or when auditing the registration chain for reproducibility.

**When to update**: every time a registration is created, amended, or superseded by `eureka:hypothesis-first`. The skill regenerates the affected rows.

Last updated: (not yet populated — this is a template)

---

## Registration chain

| Registration ID | Status | Lineage | Created |
|---|---|---|---|
| (none yet) | | | |

## Active registrations summary

(None yet — this INDEX is seeded empty. As your project registers hypotheses via `eureka:hypothesis-first`, rows will be added here.)

---

## How the lineage column works

- **Original registration**: blank lineage column
- **Supersession**: `supersedes: <prev-id>` — this registration replaces an earlier one
- **Amendment**: `parent: <parent-id>` — this file amends an earlier registration without replacing it
- **Chained supersession**: v3 might have `supersedes: v2` while v2 has `supersedes: v1`

## Example entries

(Illustrative only — delete when your project has real entries.)

```
| 2026-04-17-topic-v1 | superseded-by: 2026-05-01-topic-v2 | — | 2026-04-17 |
| 2026-05-01-topic-v2 | amended-by: 2026-05-15-topic-amendment-001 | supersedes: 2026-04-17-topic-v1 | 2026-05-01 |
| 2026-05-15-topic-amendment-001 | active (amendment) | parent: 2026-05-01-topic-v2 | 2026-05-15 |
```

In this example, the authoritative current registration for "topic" is **v2** (plus amendment-001). v1 is superseded and should not be read as authoritative.
