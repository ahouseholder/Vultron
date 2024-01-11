#  Copyright (c) 2024 Carnegie Mellon University and Contributors.
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
import os
import tempfile
import unittest
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

import vultron.scripts.vocab_examples as examples
from vultron.as_vocab.base.objects.activities.base import as_Activity
from vultron.as_vocab.base.objects.activities.transitive import (
    as_Accept,
    as_Add,
    as_Create,
    as_Ignore,
    as_Join,
    as_Leave,
    as_Offer,
    as_Read,
    as_Reject,
    as_Undo,
)
from vultron.as_vocab.base.objects.actors import as_Actor
from vultron.as_vocab.base.objects.base import as_Object
from vultron.as_vocab.objects.vulnerability_case import VulnerabilityCase
from vultron.as_vocab.objects.vulnerability_report import VulnerabilityReport


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Foo:
    bar: str = "baz"


class MyTestCase(unittest.TestCase):
    def test_json2md(self):
        # an object with a to_json method

        foo = Foo(bar="baz")

        txt = examples.json2md(foo)
        self.assertTrue(txt.startswith("```json"))
        self.assertTrue(txt.endswith("```"))
        self.assertTrue("bar" in txt)
        self.assertTrue("baz" in txt)

    def test_obj_to_file(self):
        foo = Foo(bar="baz")
        # open a temporary file
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename = tmpdirname + "/test.md"
            self.assertFalse(os.path.exists(filename))
            examples.obj_to_file(foo, filename)
            self.assertTrue(os.path.exists(filename))

            # read the file
            with open(filename, "r") as f:
                obj = json.load(f)
            self.assertEqual(obj["bar"], "baz")

    def test_finder(self):
        finder = examples.finder()
        self.assertIsInstance(finder, as_Actor)

    def test_vendor(self):
        vendor = examples.vendor()
        self.assertIsInstance(vendor, as_Actor)

    def test_report(self):
        report = examples.report()
        self.assertIsInstance(report, as_Object)
        self.assertIsInstance(report, VulnerabilityReport)

        self.assertTrue(hasattr(report, "to_json"))
        json = report.to_json()
        self.assertIsInstance(json, str)

    def test_create_report(self):
        # is it an activity?
        create_report = examples.create_report()
        self.assertIsInstance(create_report, as_Activity)
        finder = examples.finder()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(create_report, as_Create)
        self.assertEqual(create_report.as_type, "Create")
        self.assertEqual(create_report.actor, finder.as_id)
        self.assertEqual(create_report.as_object, report)

    def test_submit_report(self):
        # is it an activity?
        submit_report = examples.submit_report()
        self.assertIsInstance(submit_report, as_Activity)
        finder = examples.finder()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(submit_report, as_Offer)
        self.assertEqual(submit_report.as_type, "Offer")
        self.assertEqual(submit_report.actor, finder.as_id)
        self.assertEqual(submit_report.as_object, report)

    def test_read_report(self):
        # is it an activity?
        read_report = examples.read_report()
        self.assertIsInstance(read_report, as_Activity)
        vendor = examples.vendor()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(read_report, as_Read)
        self.assertEqual(read_report.as_type, "Read")
        self.assertEqual(read_report.actor, vendor.as_id)
        self.assertEqual(read_report.as_object, report.as_id)

    def test_validate_report(self):
        # is it an activity?
        validate_report = examples.validate_report()
        self.assertIsInstance(validate_report, as_Activity)
        vendor = examples.vendor()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(validate_report, as_Accept)
        self.assertEqual(validate_report.as_type, "Accept")
        self.assertEqual(validate_report.actor, vendor.as_id)
        self.assertEqual(validate_report.as_object, report.as_id)

    def test_invalidate_report(self):
        # is it an activity?
        invalidate_report = examples.invalidate_report()
        self.assertIsInstance(invalidate_report, as_Activity)
        vendor = examples.vendor()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(invalidate_report, as_Reject)
        self.assertEqual(invalidate_report.as_type, "Reject")
        self.assertEqual(invalidate_report.actor, vendor.as_id)
        self.assertEqual(invalidate_report.as_object, report.as_id)

    def test_close_report(self):
        # is it an activity?
        close_report = examples.close_report()
        self.assertIsInstance(close_report, as_Activity)
        vendor = examples.vendor()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(close_report, as_Leave)
        self.assertEqual(close_report.as_type, "Leave")
        self.assertEqual(close_report.actor, vendor.as_id)
        self.assertEqual(close_report.as_object, report.as_id)

    def test_case(self):
        case = examples.case()
        self.assertIsInstance(case, as_Object)
        self.assertIsInstance(case, VulnerabilityCase)

        self.assertTrue(hasattr(case, "to_json"))
        json = case.to_json()
        self.assertIsInstance(json, str)

    def test_create_case(self):
        # is it an activity?
        create_case = examples.create_case()
        self.assertIsInstance(create_case, as_Activity)
        vendor = examples.vendor()
        case = examples.case()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(create_case, as_Create)
        self.assertEqual(create_case.as_type, "Create")
        self.assertEqual(create_case.actor, vendor.as_id)

        case_from_activity = create_case.as_object
        # the case should be the object, but it will have the report and participant embedded
        self.assertEqual(case_from_activity.as_id, case.as_id)
        # report should be the report id
        self.assertEqual(
            case_from_activity.vulnerability_reports[0], report.as_id
        )
        # actor should be a pointer to the vendor
        self.assertEqual(
            case_from_activity.case_participants[0].actor, vendor.as_id
        )

    def test_add_report_to_case(self):
        # is it an activity?
        add_report_to_case = examples.add_report_to_case()
        self.assertIsInstance(add_report_to_case, as_Activity)
        vendor = examples.vendor()
        case = examples.case()
        report = examples.report()

        # does it have the right fields?
        self.assertIsInstance(add_report_to_case, as_Add)
        self.assertEqual(add_report_to_case.as_type, "Add")
        self.assertEqual(add_report_to_case.actor, vendor.as_id)
        self.assertEqual(add_report_to_case.as_object, report.as_id)
        self.assertEqual(add_report_to_case.target, case.as_id)

    def test_add_vendor_participant_to_case(self):
        activity = examples.add_vendor_participant_to_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        case = examples.case()

        self.assertIsInstance(activity, as_Add)
        self.assertEqual(activity.as_type, "Add")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.target, case.as_id)

        participant = activity.as_object
        self.assertEqual(participant.actor, vendor.as_id)
        self.assertEqual(participant.name, vendor.name)
        self.assertEqual(participant.context, case.as_id)

    def test_add_finder_participant_to_case(self):
        activity = examples.add_finder_participant_to_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        finder = examples.finder()
        case = examples.case()

        self.assertIsInstance(activity, as_Add)
        self.assertEqual(activity.as_type, "Add")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.target, case.as_id)

        participant = activity.as_object
        self.assertEqual(participant.actor, finder.as_id)
        self.assertEqual(participant.name, finder.name)
        self.assertEqual(participant.context, case.as_id)

    def test_add_coordinator_participant_to_case(self):
        activity = examples.add_coordinator_participant_to_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        coordinator = examples.coordinator()
        case = examples.case()

        self.assertIsInstance(activity, as_Add)
        self.assertEqual(activity.as_type, "Add")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.target, case.as_id)

        participant = activity.as_object
        self.assertEqual(participant.actor, coordinator.as_id)
        self.assertEqual(participant.name, coordinator.name)
        self.assertEqual(participant.context, case.as_id)

    def test_engage_case(self):
        activity = examples.engage_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        case = examples.case()

        self.assertIsInstance(activity, as_Join)
        self.assertEqual(activity.as_type, "Join")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.as_object, case.as_id)

    def test_close_case(self):
        activity = examples.close_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        case = examples.case()

        self.assertIsInstance(activity, as_Leave)
        self.assertEqual(activity.as_type, "Leave")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.as_object, case.as_id)

    def test_defer_case(self):
        activity = examples.defer_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        case = examples.case()

        self.assertIsInstance(activity, as_Ignore)
        self.assertEqual(activity.as_type, "Ignore")

        self.assertEqual(activity.actor, vendor.as_id)
        self.assertEqual(activity.as_object, case.as_id)

    def test_reengage_case(self):
        activity = examples.reengage_case()
        self.assertIsInstance(activity, as_Activity)
        vendor = examples.vendor()
        case = examples.case()

        self.assertIsInstance(activity, as_Undo)
        self.assertEqual(activity.as_type, "Undo")

        self.assertEqual(activity.actor, vendor.as_id)
        # inside the activity is a deferral activity
        self.assertEqual(activity.as_object.as_type, "Ignore")
        self.assertEqual(activity.as_object.actor, vendor.as_id)
        self.assertEqual(activity.as_object.as_object, case.as_id)

        self.assertEqual(activity.context, case.as_id)


if __name__ == "__main__":
    unittest.main()
