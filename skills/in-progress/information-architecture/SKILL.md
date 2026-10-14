---
name: information-architecture
description: Organize product content into destinations, labels and navigation. Use when mapping information architecture, a sitemap or findability from an agreed product brief, or restructuring an existing information hierarchy.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Information architecture

Decide where the scoped information belongs and how a person finds it. The output is an information map with a content-to-destination trace. Task transitions belong to user-flow; screen composition belongs to wireframe.

## 1. Establish the boundary

Read the supplied PM decisions, vocabulary, content inventory and existing navigation. Reuse their locators and revision identifiers instead of rewriting the brief. Capture the audience, retrieval tasks, scope and fixed decisions in a few lines.

If an input is absent, distinguish a missing document from a missing decision. A small request may already contain enough information. Ask only about a gap that changes the structure, while mapping the settled portion. Keep unresolved ownership, permissions or product scope visible rather than inventing a policy.

Done when the map has a bounded set of information and retrieval tasks, with assumptions separated from supplied decisions.

## 2. Map objects to destinations

Identify content types, their relationships, and the attributes people use to recognize or narrow them. Separate an object from its list, detail view, category and filter: these do not automatically need separate pages.

Give each destination a stable ID, a user-facing label, its content and the task it supports. Map each scoped content type to a destination or an explicit exclusion. Reuse established vocabulary; record ambiguous labels with the competing meanings.

For an existing product, retain the current structure wherever it serves the task. Propose a change only with a specific findability problem, affected task and resulting destination. Keeping the structure is a valid result. Keep taxonomy changes distinct from visual navigation treatments.

Done when the scoped content has a home and the purpose of every proposed destination is identifiable.

## 3. Connect discovery and return paths

Show the relevant entry points and relationships: global or local navigation, contextual links, search, filters and direct entry where the product supports them. Give the same object a stable destination even when several paths reach it. Distinguish hidden content from content a role may not access.

State what stays reachable when navigation changes at narrow widths. Define the information priority and entry paths here; leave the menu component and layout to wireframe.

Walk each retrieval task from its entry point to its target and back to an appropriate context. Record an unreachable target, ambiguous choice or unresolved access rule. These are author walkthroughs, not user research. Existing card-sort or tree-test evidence can inform the map; proposing those studies does not mean they happened.

Done when each scoped retrieval task has a traceable route or a named unresolved dependency.

## 4. Deliver the map

Save Markdown in the project's existing design location. A small map may be a section of an existing document. Include:

- Source locators, scope, assumptions and decision status.
- Destinations: ID, label, content, supporting task and access condition if relevant.
- Navigation relationships and content coverage, as a table or diagram.
- Walkthrough results, proposed changes and remaining decisions.

Mark the map ready for downstream drafting when its structural decisions are usable. Mark it approved only when the user's decisions support that status. If a blocking decision remains, hand over the settled portion and identify the exact dependency.

The next role can consume the destination IDs without another PM interview. Continue into task transitions or screens only when that work is included in the user's request.
