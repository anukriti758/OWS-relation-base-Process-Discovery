"""
object_wise_sub_relation_process_discovery.py
--------------------------------
This module provides functionality to discover object-type–wise submodels
from an Object-Centric Event Log (OCEL) using PM4Py.

It extracts universal Event–Object relations, computes object-type–specific
sub-relations, and applies discovery algorithms to generate object-wise models.

import pm4py
from pm4py.objects.ocel.obj import OCEL
from collections import defaultdict
from typing import Dict, List, Tuple, Any


def _extract_universal_relation(ocel: OCEL) -> Tuple[List[Dict[str, Any]], int]:
    """
    Extract the universal Event–Object relation from an OCEL log.

    Args:
        ocel (OCEL): The input Object-Centric Event Log.

    Returns:
        Tuple[List[Dict[str, Any]], int]: 
            - List of dictionaries with event_id, object_id, and object_type.
            - Total count of event–object relations.
    """
    # Copy dataframes to avoid modifying the original OCEL
    events_df = ocel.events.copy()
    objects_df = ocel.objects.copy()
    relations_df = ocel.relations.copy()

    # Define OCEL standard column names
    event_id_col = "ocel:eid"
    object_id_col = "ocel:oid"
    object_type_col = "ocel:type"

    # Map object IDs to their respective types
    object_id_to_type = dict(zip(objects_df[object_id_col], objects_df[object_type_col]))

    # Build mapping: event_id → list of associated object_ids
    event_to_objects = defaultdict(list)
    for _, row in relations_df.iterrows():
        event_to_objects[row[event_id_col]].append(row[object_id_col])

    # Create the universal event–object relation
    universal_relation = [
        {
            "event_id": eid,
            "object_id": oid,
            "object_type": object_id_to_type.get(oid)
        }
        for eid, oids in event_to_objects.items()
        for oid in oids
    ]

    total_relation_count = len(universal_relation)
    print(f"Total Event–Object universal relation count: {total_relation_count}")

    return universal_relation, total_relation_count


def _discover_sub_model_for_object_type(
    ocel: OCEL,
    universal_relation: List[Dict[str, Any]],
    object_type: str
) -> Tuple[int, Any]:
    """
    Discover the object-type–specific submodel from the OCEL.

    Args:
        ocel (OCEL): The input Object-Centric Event Log.
        universal_relation (List[Dict[str, Any]]): The universal event–object relations.
        object_type (str): The focus object type for submodel discovery.

    Returns:
        Tuple[int, Any]:
            - Count of event–object relations for this object type.
            - The discovered OC-DFG model.
    """
    # Define OCEL column names
    event_id_col = "ocel:eid"
    object_id_col = "ocel:oid"

    # Copy original dataframes
    events_df = ocel.events.copy()
    objects_df = ocel.objects.copy()
    relations_df = ocel.relations.copy()

    print(f"\n=== [DISCOVERY] Object Type Perspective: {object_type} ===")

    # Identify events relevant to the current object type
    relevant_event_ids = [
        rel["event_id"] for rel in universal_relation if rel["object_type"] == object_type
    ]

    # Filter data for the selected object type
    sub_events = events_df[events_df[event_id_col].isin(relevant_event_ids)]
    sub_relations = relations_df[relations_df[event_id_col].isin(relevant_event_ids)]

    # Identify all related objects for these relations
    related_object_ids = set(sub_relations[object_id_col])
    related_objects = objects_df[objects_df[object_id_col].isin(related_object_ids)]

    # Create a sub-OCEL for this object type
    sub_ocel = OCEL(events=sub_events, objects=related_objects, relations=sub_relations)

    # Count event–object pairs for this sub-OCEL
    sub_relation_count = len(sub_relations)
    print(f"Total Event–Object count for object type '{object_type}': {sub_relation_count}")

    # Apply discovery algorithm (Object-Centric Directly-Follows Graph)
    ocdfg_model = pm4py.discover_ocdfg(sub_ocel)

    # Optional visualization
    pm4py.view_ocdfg(ocdfg_model)

    return sub_relation_count, ocdfg_model


def discover_object_wise_sub_models_with_counts(ocel: OCEL) -> Tuple[int, Dict[str, int], Dict[str, Any]]:
    """
    Discover object-type–specific submodels along with relation counts
    from an Object-Centric Event Log (OCEL).

    Steps:
    1. Extract universal Event–Object relation.
    2. For each object type:
       - Build a sub-OCEL.
       - Discover the object-type perspective model (OC-DFG).
       - Record relation counts.

    Args:
        ocel (OCEL): The input Object-Centric Event Log.

    Returns:
        Tuple[int, Dict[str, int], Dict[str, Any]]:
            - Total universal relation count.
            - Object-type–wise relation counts.
            - Discovered object-type–wise models.
    """
    # Step 1: Extract the universal relation
    universal_relation, total_universal_count = _extract_universal_relation(ocel)

    # Step 2: Initialize containers for results
    discovered_models: Dict[str, Any] = {}
    sub_relation_counts: Dict[str, int] = {}

    # Step 3: Discover models for each object type
    object_types = ocel.objects["ocel:type"].unique()
    for obj_type in object_types:
        sub_count, sub_model = _discover_sub_model_for_object_type(ocel, universal_relation, obj_type)
        sub_relation_counts[obj_type] = sub_count
        discovered_models[obj_type] = sub_model

    print("\n=== [SUMMARY] ===")
    for obj_type, count in sub_relation_counts.items():
        print(f"Object Type '{obj_type}': {count} Event–Object relations")

    return total_universal_count, sub_relation_counts, discovered_models


# ---------------------------------------------------------------------
# Example Usage
# ---------------------------------------------------------------------
# if __name__ == "__main__":
#     ocel = pm4py.read_ocel2_json("your_log.json")
#     total_count, sub_counts, models = discover_object_wise_sub_models_with_counts(ocel)
