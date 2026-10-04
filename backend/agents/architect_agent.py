class ArchitectAgent:

    def analyze(
            self,
            inspector_reports
    ):

        architectures = []

        for report in inspector_reports:

            architectures.append(

                self.map_issue(
                    report
                )
            )

        return architectures

################################################

    def map_issue(
            self,
            report
    ):

        module = report["module"]

        root_cause = report["root_cause"]

        architecture = (
            self.architecture_library()
        )

        module_data = architecture.get(
            module,
            {}
        )

        return {

            "module":
            module,

            "root_cause":
            root_cause,

            "severity":
            report["severity"],

            "affected_scenarios":
            report["affected_scenarios"],

            "count":
            report["count"],

            ####################################

            "frontend_file":
            module_data.get(
                "frontend_file"
            ),

            "frontend_component":
            module_data.get(
                "frontend_component"
            ),

            ####################################

            "backend_file":
            module_data.get(
                "backend_file"
            ),

            "backend_function":
            module_data.get(
                "backend_function"
            ),

            ####################################

            "database_table":
            module_data.get(
                "database_table"
            ),

            ####################################

            "target_layer":
            self.get_target_layer(
                root_cause
            ),

            "target_file":
            self.get_target_file(
                module,
                root_cause
            ),

            "target_function":
            self.get_target_function(
                module,
                root_cause
            ),

            ####################################

            "priority":
            self.get_priority(
                report["severity"]
            ),

            "estimated_fix_complexity":
            self.fix_complexity(
                root_cause
            ),

            "recommended_strategy":
            self.strategy(
                root_cause
            )

        }

################################################

    def architecture_library(self):

        return {

            "flight": {

                "frontend_file":
                "pages/Flights.jsx",

                "frontend_component":
                "FlightSearch",

                "backend_file":
                "routes/bookings.py",

                "backend_function":
                "book_flight",

                "database_table":
                "bookings"

            },

            "bus": {

                "frontend_file":
                "pages/Buses.jsx",

                "frontend_component":
                "BusSearch",

                "backend_file":
                "routes/buses.py",

                "backend_function":
                "book_bus",

                "database_table":
                "bus_bookings"

            },

            "train": {

                "frontend_file":
                "pages/Trains.jsx",

                "frontend_component":
                "TrainSearch",

                "backend_file":
                "routes/trains.py",

                "backend_function":
                "book_train",

                "database_table":
                "train_bookings"

            },

            "hotel": {

                "frontend_file":
                "pages/Hotels.jsx",

                "frontend_component":
                "HotelSearch",

                "backend_file":
                "routes/hotels.py",

                "backend_function":
                "book_hotel",

                "database_table":
                "hotel_bookings"

            }

        }

################################################

    def get_target_layer(
            self,
            root_cause
    ):

        if root_cause == "Validation Failure":

            return "backend"

        if root_cause == "Booking Creation Failure":

            return "backend"

        if root_cause == "Authentication Failure":

            return "backend"

        return "unknown"

################################################

    def get_target_file(
            self,
            module,
            root_cause
    ):

        architecture = (
            self.architecture_library()
        )

        module_data = architecture.get(
            module,
            {}
        )

        return module_data.get(
            "backend_file"
        )

################################################

    def get_target_function(
            self,
            module,
            root_cause
    ):

        mapping = {

            "flight":
            "book_flight",

            "bus":
            "book_bus",

            "train":
            "book_train",

            "hotel":
            "book_hotel"

        }

        return mapping.get(
            module
        )

################################################

    def get_priority(
            self,
            severity
    ):

        mapping = {

            "HIGH":
            "P1",

            "MEDIUM":
            "P2",

            "LOW":
            "P3"

        }

        return mapping.get(
            severity,
            "P3"
        )

################################################

    def fix_complexity(
            self,
            root_cause
    ):

        complexity = {

            "Validation Failure":
            "LOW",

            "Booking Creation Failure":
            "MEDIUM",

            "Authentication Failure":
            "HIGH",

            "Cancellation Failure":
            "LOW"

        }

        return complexity.get(
            root_cause,
            "UNKNOWN"
        )

################################################

    def strategy(
            self,
            root_cause
    ):

        strategies = {

            "Validation Failure":
            "Add backend validation guards.",

            "Booking Creation Failure":
            "Inspect booking endpoint and database transaction.",

            "Cancellation Failure":
            "Inspect cancellation endpoint and booking lookup.",

            "Authentication Failure":
            "Inspect login session and JWT workflow."

        }

        return strategies.get(
            root_cause,
            "Manual investigation"
        )

################################################

if __name__ == "__main__":

    sample = [

        {

            "module":
            "flight",

            "root_cause":
            "Validation Failure",

            "count":
            2,

            "severity":
            "MEDIUM",

            "affected_scenarios": [

                "empty_text",

                "negative_value"

            ]

        }

    ]

    reports = (

        ArchitectAgent()

        .analyze(sample)

    )

    print(
        "\nARCHITECT REPORTS\n"
    )

    for report in reports:

        print(report)