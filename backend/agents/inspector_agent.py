from business_rules.rules import SCENARIO_RULES


class InspectorAgent:

    def inspect(self, results):

        reports = []

        for result in results:

            if result["test_passed"]:

                reports.append({

                    "module":
                    result["module"],

                    "scenario":
                    result["scenario"],

                    "bug_detected":
                    False,

                    "severity":
                    "NONE",

                    "recommendation":
                    "No action required"
                })

            else:

                rule = SCENARIO_RULES.get(
                    result["scenario"],
                    {}
                )

                reports.append({

                    "module":
                    result["module"],

                    "scenario":
                    result["scenario"],

                    "bug_detected":
                    True,

                    "severity":
                    rule.get(
                        "severity",
                        "LOW"
                    ),

                    "root_cause":
                    rule.get(
                        "root_cause",
                        "Unknown Cause"
                    ),

                    "recommendation":
                    rule.get(
                        "recommendation",
                        "Review business rules"
                    )
                })

        return reports