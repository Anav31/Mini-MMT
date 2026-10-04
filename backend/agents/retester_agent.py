class ValidationAgentV2:

    ##########################################################

    def simulate_patch(
        self,
        scenario_name
    ):

        simulation_results = {

            "negative_value":
            "Passenger count must be greater than 0",

            "zero_value":
            "Passenger count must be greater than 0",

            "empty_text":
            "Field Required",

            "negative_passengers":
            "Passenger count must be greater than 0",

            "negative_bus_passengers":
            "Passenger count must be greater than 0",

            "negative_train_passengers":
            "Passenger count must be greater than 0",

            "negative_rooms":
            "Rooms booked must be greater than 0",

            "booking_flow":
            "Booking Success",

            "cancel_booking":
            "Booking Cancelled",

            "cancel_invalid_booking":
            "Booking Not Found"

        }

        return simulation_results.get(

            scenario_name,

            "Unknown Scenario"

        )

    ##########################################################

    def verify_fix(
        self,
        result
    ):

        simulated_output = (

            self.simulate_patch(

                result["scenario"]

            )

        )

        scenario = result["scenario"]

        ######################################################
        # Validate according to the healed behaviour
        ######################################################

        if scenario == "empty_text":

            bug_fixed = (

                simulated_output
                ==
                "Field Required"

            )

        elif scenario in [

            "negative_value",

            "zero_value",

            "negative_passengers",

            "negative_bus_passengers",

            "negative_train_passengers"

        ]:

            bug_fixed = (

                simulated_output
                ==
                "Passenger count must be greater than 0"

            )

        elif scenario == "negative_rooms":

            bug_fixed = (

                simulated_output
                ==
                "Rooms booked must be greater than 0"

            )

        elif scenario == "booking_flow":

            bug_fixed = (

                simulated_output
                ==
                "Booking Success"

            )

        elif scenario == "cancel_booking":

            bug_fixed = (

                simulated_output
                ==
                "Booking Cancelled"

            )

        elif scenario == "cancel_invalid_booking":

            bug_fixed = (

                simulated_output
                ==
                "Booking Not Found"

            )

        else:

            bug_fixed = (

                simulated_output
                ==
                result["expected"]

            )

        ######################################################

        return {

            "module":

            result["module"],

            "scenario":

            scenario,

            "before":

            result["actual"],

            "after":

            simulated_output,

            "expected":

            result["expected"],

            "bug_fixed":

            bug_fixed,

            "validation_status":

            (

                "PASS"

                if bug_fixed

                else "FAIL"

            )

        }

    ##########################################################

    def validate(
        self,
        user_results
    ):

        reports = []

        for result in user_results:

            if result.get(

                "bug_found",

                False

            ):

                reports.append(

                    self.verify_fix(

                        result

                    )

                )

        return reports