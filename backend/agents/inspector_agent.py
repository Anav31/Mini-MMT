class InspectorAgent:
    def inspect(
            self,
            user_reports
    ):

        aggregated = {}

        for report in user_reports:

            bug = self.analyze_report(
                report
            )

            if bug is None:
                continue


            key = (

                bug["module"],

                bug["root_cause"]

            )


            self.aggregate_bug(

                aggregated,

                key,

                bug

            )


        for item in aggregated.values():

            item["severity"] = (

                self.calculate_severity(

                    item["count"]

                )

            )


            item["recommendation"] = (

                self.get_recommendation(

                    item["root_cause"]

                )

            )


        return list(

            aggregated.values()

        )


###################################################


    def analyze_report(

            self,

            report
    ):


        if not report.get(

                "bug_found",

                False

        ):

            return None



        scenario = (

            report.get(

                "scenario",

                "Unknown"

            )

        )



        root_cause = (

            self.detect_root_cause(

                report

            )

        )


        return {


            "module":

            report["module"],


            "scenario":

            scenario,


            "root_cause":

            root_cause

        }


###################################################


    def detect_root_cause(

            self,

            report
    ):


        actual = str(

            report.get(

                "actual",

                ""

            )

        ).lower()


        expected = str(

            report.get(

                "expected",

                ""

            )

        ).lower()


        if "booking" in actual:

            return (

                "Booking Creation Failure"

            )


        if report["scenario"] in [

        "empty_text",

        "negative_value",

        "zero_value",

        "special_characters"

        ]:
            return "Validation Failure"
        
        if report["scenario"] == "cancel_invalid_booking":
            return "Booking Cancellation Failure"


        if "login" in actual:

            return (

                "Authentication Failure"

            )


        if "search" in actual:

            return (

                "Search Failure"

            )


        return (

            "Unknown Failure"

        )


###################################################


    def aggregate_bug(

            self,

            aggregated,

            key,

            bug
    ):


        if key not in aggregated:


            aggregated[key] = {


                "module":

                bug["module"],


                "root_cause":

                bug["root_cause"],


                "count":

                1,


                "affected_scenarios":

                [

                    bug["scenario"]

                ]

            }


        else:


            aggregated[key][

                "count"

            ] += 1


            if bug["scenario"] not in aggregated[key]["affected_scenarios"]:

                aggregated[key]["affected_scenarios"].append(

                    bug["scenario"]

                )


###################################################


    def calculate_severity(

            self,

            count
    ):


        if count >= 5:

            return "HIGH"


        elif count >= 2:

            return "MEDIUM"


        return "LOW"


###################################################


    def get_recommendation(

            self,

            root_cause
    ):


        recommendations = {


            "Validation Failure":

            "Inspect frontend and backend validation layers.",



            "Search Failure":

            "Inspect search endpoint and filtering logic.",



            "Booking Creation Failure":

            "Inspect booking service and database persistence.",



            "Authentication Failure":

            "Inspect login service and credential validation.",

            "Cancellation Failure":
            "Inspect booking cancellation workflow.",


            "Unknown Failure":

            "Manual Investigation Required."
            

        }


        return recommendations.get(

            root_cause,

            "Manual Investigation Required."

        )


###################################################


if __name__ == "__main__":


    sample_reports = [

        {

            "module": "flight",

            "scenario": "empty_text",

            "bug_found": True,

            "expected": "Validation Error",

            "actual": "Page Loaded"

        },


        {

            "module": "flight",

            "scenario": "negative_value",

            "bug_found": True,

            "expected": "Validation Error",

            "actual": "Page Loaded"

        },


        {

            "module": "hotel",

            "scenario": "booking",

            "bug_found": True,

            "expected": "Booking Created",

            "actual": "Booking Missing"

        }

    ]


    inspector = (

        InspectorAgent()

    )


    reports = (

        inspector.inspect(

            sample_reports

        )

    )


    print(

        "\nINSPECTOR REPORTS\n"

    )


    for report in reports:

        print(report)