#!/usr/bin/env python

#  Copyright (c) 2025 Carnegie Mellon University and Contributors.
#  - see Contributors.md for a full list of Contributors
#  - see ContributionInstructions.md for information on how you can Contribute to this project
#  Vultron Multiparty Coordinated Vulnerability Disclosure Protocol Prototype is
#  licensed under a MIT (SEI)-style license, please see LICENSE.md distributed
#  with this Software or contact permission@sei.cmu.edu for full terms.
#  Created, in part, with funding and support from the United States Government
#  (see Acknowledgments file). This program may include and/or can make use of
#  certain third party source code, object code, documentation and other files
#  (“Third Party Software”). See LICENSE.md for more details.
#  Carnegie Mellon®, CERT® and CERT Coordination Center® are registered in the
#  U.S. Patent and Trademark Office by Carnegie Mellon University

import json
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL


def ttl_to_json_and_rules(ttl_paths):
    g = Graph()

    # --- Load all TTL files into one merged graph ---
    for path in ttl_paths:
        g.parse(path, format="turtle")

    classes = {}
    properties = {}
    rules = []

    # --- Classes ---
    for cls in g.subjects(RDF.type, OWL.Class):
        cls_str = str(cls)
        classes.setdefault(cls_str, {"subClassOf": [], "equivalentTo": []})

        for parent in g.objects(cls, RDFS.subClassOf):
            classes[cls_str]["subClassOf"].append(str(parent))
            rules.append(f"If X is a {cls_str} then X is also a {parent}.")

        for eq in g.objects(cls, OWL.equivalentClass):
            classes[cls_str]["equivalentTo"].append(str(eq))
            rules.append(
                f"{cls_str} and {str(eq)} contain exactly the same individuals."
            )

    # --- Object Properties ---
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        p = str(prop)
        properties.setdefault(p, {"domain": [], "range": [], "type": "object"})

        for domain in g.objects(prop, RDFS.domain):
            properties[p]["domain"].append(str(domain))
            rules.append(
                f"Domain of {p} is {domain}: if (X {p} Y) then X is a {domain}."
            )

        for rng in g.objects(prop, RDFS.range):
            properties[p]["range"].append(str(rng))
            rules.append(
                f"Range of {p} is {rng}: if (X {p} Y) then Y is a {rng}."
            )

    # --- Datatype Properties ---
    for prop in g.subjects(RDF.type, OWL.DatatypeProperty):
        p = str(prop)
        properties.setdefault(
            p, {"domain": [], "range": [], "type": "datatype"}
        )

        for domain in g.objects(prop, RDFS.domain):
            properties[p]["domain"].append(str(domain))
            rules.append(
                f"Domain of {p} is {domain}: if (X {p} V) then X is a {domain}."
            )

        for rng in g.objects(prop, RDFS.range):
            properties[p]["range"].append(str(rng))
            rules.append(f"Value of {p} must be of datatype {rng}.")

    # --- All remaining triples (fallback facts) ---
    for s, p, o in g:
        if p in (
            RDFS.subClassOf,
            OWL.equivalentClass,
            RDFS.domain,
            RDFS.range,
        ):
            continue
        rules.append(f"Triple: ({str(s)}, {str(p)}, {str(o)}).")

    json_out = {
        "classes": classes,
        "properties": properties,
    }

    return json_out, rules


if __name__ == "__main__":
    # pull in all .ttl files in a directory
    ttl_dir = Path("../../ontology/")
    ttl_files = list(ttl_dir.glob("*.ttl"))

    json_model, rules = ttl_to_json_and_rules(ttl_files)

    with open("ontology.json", "w") as f:
        json.dump(json_model, f, indent=2)

    with open("rules.txt", "w") as f:
        for r in rules:
            f.write(r + "\n")

    print(f"Loaded {len(ttl_files)} ontology files → merged model built.")
