class ArchitectAgent:

    def analyze(
        self,
        inspector_reports
    ):

        architecture_reports = []

        for report in inspector_reports:

            if not report["bug_detected"]:

                continue

            architecture_reports.append(

                self._build_analysis(
                    report
                )

            )

        return architecture_reports

    def _build_analysis(
        self,
        report
    ):

        scenario = report["scenario"]

        analysis_map = {

            "negative_passengers": {

                "affected_file":
                "routes/bookings.py",

                "affected_function":
                "book_flight",

                "business_impact":
                "Inventory corruption",

                "technical_analysis":
                "Negative passenger values increase available seats because subtracting a negative number becomes addition.",

                "fix_strategy":
                "Add passenger validation before seat calculation."
            },

            "negative_bus_passengers": {

                "affected_file":
                "routes/buses.py",

                "affected_function":
                "book_bus",

                "business_impact":
                "Seat inventory corruption",

                "technical_analysis":
                "Negative passenger values can increase seat availability.",

                "fix_strategy":
                "Validate passenger count before updating seats."
            },

            "negative_train_passengers": {

                "affected_file":
                "routes/trains.py",

                "affected_function":
                "book_train",

                "business_impact":
                "Seat inventory corruption",

                "technical_analysis":
                "Negative passenger values can increase seat availability.",

                "fix_strategy":
                "Validate passenger count before updating seats."
            },

            "negative_rooms": {

                "affected_file":
                "routes/hotels.py",

                "affected_function":
                "book_hotel",

                "business_impact":
                "Room inventory corruption",

                "technical_analysis":
                "Negative room values can increase room availability.",

                "fix_strategy":
                "Validate room count before updating inventory."
            }
        }

        details = analysis_map.get(
            scenario,
            {}
        )

        return {

            "module":
            report["module"],

            "scenario":
            scenario,

            **details
        }