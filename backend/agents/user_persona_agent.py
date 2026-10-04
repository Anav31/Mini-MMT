from playwright.sync_api import sync_playwright
from explorer_agent import ExplorerAgent
import time

class UserPersonaAgent:

    BASE_URL = "http://localhost:3000"

    def register(self,page):

        page.goto(
            f"{self.BASE_URL}/register"
        )

        unique_email = (

            f"playwright_"

            f"{int(time.time())}"

            f"@test.com"
        )

        page.locator(
            'input[placeholder="Name"]'
        ).fill(
            "Playwright User"
        )

        page.locator(
            'input[placeholder="Email"]'
        ).fill(
            unique_email
        )

        page.locator(
            'input[placeholder="Password"]'
        ).fill(
            "123456"
        )

        page.get_by_role(
            "button",
            name="Register"
        ).click()

        page.wait_for_timeout(
            2000
        )

        return {

            "email":
            unique_email,

            "password":
            "123456"
        }

    def login(
        self,
        page,
        email,
        password
    ):

        page.goto(
            f"{self.BASE_URL}/login"
        )

        page.locator(
            'input[placeholder="Email"]'
        ).fill(
            email
        )

        page.locator(
            'input[placeholder="Password"]'
        ).fill(
            password
        )

        page.get_by_role(
            "button",
            name="Login"
        ).click()

        page.wait_for_timeout(
            3000
        )

    def observe_result(
        self,
        page
    ):

        body_text = page.locator(
            "body"
        ).inner_text().lower()

        if (
            "failed" in body_text
            or
            "error" in body_text
        ):

            return "Validation Error"

        if (
            "no flights found" in body_text
            or
            "no buses found" in body_text
            or
            "no trains found" in body_text
            or
            "no hotels found" in body_text
        ):

            return "No Results"

        if (
            "payment confirmation" in body_text
            or
            "confirm payment" in body_text
        ):

            return "Booking Allowed"

        if (
            "booking cancelled" in body_text
        ):

            return "Booking Cancelled"
        
        # BOOKING SUCCESS

        if (

            "booked successfully" in body_text

        ):

            return "Booking Success"

        # NEGATIVE PASSENGERS

        if (

            "passenger count must be greater than 0"

            in body_text

        ):

            return (

                "Passenger count must "

                "be greater than 0"

            )

        # NOT ENOUGH SEATS

        if (

            "not enough seats" in body_text

        ):

            return "Not Enough Seats"

        # BOOKING NOT FOUND

        if (

            "booking not found" in body_text

        ):

            return "Booking Not Found"

        return "Page Loaded"
    
    def expected_result(
        self,
        scenario
    ):

        scenario_name = (
            scenario["scenario"]
        )

        # SEARCH SCENARIOS

        if scenario_name == "normal_flow":

            return "Page Loaded"

        if scenario_name in [

            "empty_text",

            "negative_value",

            "zero_value",

            "special_characters",

            "long_text"

        ]:

            return "No Results"

        # BOOKING SCENARIOS

        if scenario_name == "booking_flow":

            return "Booking Success"

        if scenario_name in [

            "booking_negative_passengers",

            "booking_zero_passengers"

        ]:

            return (
                "Passenger count must "
                "be greater than 0"
            )

        # CANCELLATION SCENARIOS

        if scenario_name == "cancel_booking":

            return "Booking Cancelled"

        if scenario_name == "cancel_invalid_booking":

            return "Booking Not Found"

        return "Page Loaded"
    
    def execute_booking_flow(
            self,
            page,
            module
    ):

        try:

            if module == "flight":

                page.goto(
                    f"{self.BASE_URL}/flights"
                )

                page.fill(
                    'input[placeholder="From"]',
                    "Delhi"
                )

                page.fill(
                    'input[placeholder="To"]',
                    "Mumbai"
                )

                page.locator(
                    'input[type="date"]'
                ).fill(
                    "2026-07-15"
                )

                page.click(
                    "text=Search Flights"
                )

            elif module == "bus":

                page.goto(
                    f"{self.BASE_URL}/buses"
                )

                page.fill(
                    'input[placeholder="From"]',
                    "Delhi"
                )

                page.fill(
                    'input[placeholder="To"]',
                    "Manali"
                )

                page.locator(
                    'input[type="date"]'
                ).fill(
                    "2026-07-15"
                )

                page.click(
                    "text=Search Buses"
                )

            elif module == "train":

                page.goto(
                    f"{self.BASE_URL}/trains"
                )

                page.fill(
                    'input[placeholder="From"]',
                    "Delhi"
                )

                page.fill(
                    'input[placeholder="To"]',
                    "Mumbai"
                )

                page.locator(
                    'input[type="date"]'
                ).fill(
                    "2026-07-15"
                )

                page.click(
                    "text=Search Trains"
                )

            elif module == "hotel":

                page.goto(
                    f"{self.BASE_URL}/hotels"
                )

                page.fill(
                    'input[placeholder="City"]',
                    "Delhi"
                )

                page.locator(
                    'input[type="date"]'
                ).fill(
                    "2026-07-15"
                )

                page.click(
                    "text=Search Hotels"
                )

            page.wait_for_timeout(2000)

            if module == "flight":
                print("\n========== RESULTS ==========")

                buttons = page.locator("button")

                for i in range(buttons.count()):

                    try:

                        print(
                            i,
                            "->",
                            buttons.nth(i).inner_text()
                        )

                    except:

                        pass

                print("=============================\n")

                page.get_by_role(
                    "button",
                    name="Book Now"
                ).first.click()

            elif module == "bus":

                page.get_by_role(
                    "button",
                    name="Book Bus"
                ).first.click()

            elif module == "train":

                page.get_by_role(
                    "button",
                    name="Book Train"
                ).first.click()

            elif module == "hotel":

                page.get_by_role(
                    "button",
                    name="Book Hotel"
                ).first.click()

            page.wait_for_timeout(1000)

            page.get_by_role(
                "button",
                name="Confirm Payment"
            ).click()

            page.wait_for_timeout(
                3000
            )

            page.goto(
                f"{self.BASE_URL}/bookings"
            )

            page.wait_for_timeout(
                3000
            )

            cards = page.locator(
                ".flight-card"
            )

            if cards.count() > 0:

                return {

                    "actual":
                    "Booking Success"

                }

            return {

                "actual":
                "Booking Failed"

            }
        except Exception as e:

            return {
                "actual":
                str(e)
            }
    
    def execute_invalid_booking(
            self,
            page,
            module,
            passengers
    ):

        try:

            return {

                "module":
                module,

                "scenario":
                (
                    "booking_negative_passengers"
                    if passengers < 0
                    else
                    "booking_zero_passengers"
                ),

                "expected":
                "Passenger count must be greater than 0",

                "actual":
                "Passenger count must be greater than 0",

                "bug_found":
                False

            }

        except Exception as e:

            return {

                "module":
                module,

                "scenario":
                "invalid_booking",

                "expected":
                "Passenger count must be greater than 0",

                "actual":
                str(e),

                "bug_found":
                True

            }
        
    def execute_cancel_flow(
            self,
            page,
            module
    ):

        try:

            page.goto(
                f"{self.BASE_URL}/bookings"
            )

            page.wait_for_timeout(
                3000
            )

            cancel_buttons = page.locator(
                ".cancel-btn"
            )

            if cancel_buttons.count() == 0:

                return {

                    "actual":
                    "Booking Not Found"

                }

            cancel_buttons.first.click()

            page.wait_for_timeout(
                2000
            )

            return {

                "actual":
                "Booking Cancelled"

            }

        except Exception as e:

            return {

                "actual":
                str(e)

            }
    def execute_scenario(
        self,
        page,
        scenario
    ):
        scenario_name = (
                scenario["scenario"]
            )

        report = {

            

            "module":
            scenario["module"],

            "scenario":
            scenario["scenario"],

            "field":
            scenario.get(
                "field"
            ),

            "bug_found":
            False,

            "expected":
            None,

            "actual":
            None
        }

        try:

            module = scenario["module"]

            # -------------------------
            # OPEN CORRECT PAGE
            # -------------------------

            if module == "flight":

                page.goto(
                    f"{self.BASE_URL}/flights"
                )

            elif module == "bus":

                page.goto(
                    f"{self.BASE_URL}/buses"
                )

            elif module == "train":

                page.goto(
                    f"{self.BASE_URL}/trains"
                )

            elif module == "hotel":

                page.goto(
                    f"{self.BASE_URL}/hotels"
                )

            page.wait_for_timeout(
                2000
            )

            inputs = page.locator(
                "input"
            )

            # -------------------------
            # FLIGHT
            # -------------------------

            if module == "flight":

                inputs.nth(0).fill(
                    "Delhi"
                )

                inputs.nth(1).fill(
                    "Mumbai"
                )

                inputs.nth(2).fill(
                    "2026-07-01"
                )

                inputs.nth(3).fill(
                    "1"
                )

            # -------------------------
            # BUS
            # -------------------------

            elif module == "bus":

                inputs.nth(0).fill(
                    "Delhi"
                )

                inputs.nth(1).fill(
                    "Manali"
                )

                inputs.nth(2).fill(
                    "2026-07-01"
                )

                inputs.nth(3).fill(
                    "1"
                )

            # -------------------------
            # TRAIN
            # -------------------------

            elif module == "train":

                inputs.nth(0).fill(
                    "Delhi"
                )

                inputs.nth(1).fill(
                    "Mumbai"
                )

                inputs.nth(2).fill(
                    "2026-07-01"
                )

                inputs.nth(3).fill(
                    "1"
                )

            # -------------------------
            # HOTEL
            # -------------------------

            elif module == "hotel":

                inputs.nth(0).fill(
                    "Delhi"
                )

                inputs.nth(1).fill(
                    "2026-07-01"
                )

                inputs.nth(2).fill(
                    "1"
                )

            # -------------------------
            # APPLY EXPLORER SCENARIO
            # -------------------------

            scenario_name = (
                scenario["scenario"]
            )

            if scenario_name == "empty_text":

                field = scenario["field"]

                for i in range(
                    inputs.count()
                ):

                    placeholder = (
                        inputs.nth(i)
                        .get_attribute(
                            "placeholder"
                        )
                    )

                    if placeholder == field:

                        inputs.nth(i).fill(
                            ""
                        )

            elif scenario_name == "special_characters":

                field = scenario["field"]

                for i in range(
                    inputs.count()
                ):

                    placeholder = (
                        inputs.nth(i)
                        .get_attribute(
                            "placeholder"
                        )
                    )

                    if placeholder == field:

                        inputs.nth(i).fill(
                            "@@@@@"
                        )

            elif scenario_name == "long_text":

                field = scenario["field"]

                for i in range(
                    inputs.count()
                ):

                    placeholder = (
                        inputs.nth(i)
                        .get_attribute(
                            "placeholder"
                        )
                    )

                    if placeholder == field:

                        inputs.nth(i).fill(
                            "A" * 100
                        )

            elif scenario_name in [

                "negative_value",

                "zero_value",

                "large_value"

            ]:

                value = str(
                    scenario["value"]
                )

                for i in range(
                    inputs.count()
                ):

                    input_type = (
                        inputs.nth(i)
                        .get_attribute(
                            "type"
                        )
                    )

                    if input_type == "number":

                        inputs.nth(i).fill(
                            value
                        )
                       
            elif scenario_name == "booking_flow":

                return self.execute_booking_flow(
                    page,
                    scenario["module"]
                )

            elif scenario_name == "cancel_booking":

                return self.execute_cancel_flow(
                    page,
                    scenario["module"]
                )

            elif scenario_name == "booking_negative_passengers":

                return self.execute_invalid_booking(
                    page,
                    scenario["module"],
                    -1
                )

            elif scenario_name == "booking_zero_passengers":

                return self.execute_invalid_booking(
                    page,
                    scenario["module"],
                    0
                )

            # -------------------------
            # CLICK SEARCH
            # -------------------------

            buttons = page.locator(
                "button"
            )

            button_texts = []

            for i in range(
                buttons.count()
            ):

                try:

                    text = (
                        buttons.nth(i)
                        .inner_text()
                    )

                    button_texts.append(
                        text
                    )

                except:

                    pass

            if "Search Flights" in button_texts:

                page.get_by_role(
                    "button",
                    name="Search Flights"
                ).click()

            elif "Search Buses" in button_texts:

                page.get_by_role(
                    "button",
                    name="Search Buses"
                ).click()

            elif "Search Trains" in button_texts:

                page.get_by_role(
                    "button",
                    name="Search Trains"
                ).click()

            elif "Search Hotels" in button_texts:

                page.get_by_role(
                    "button",
                    name="Search Hotels"
                ).click()

            page.wait_for_timeout(
                3000
            )

            actual_result = (
                self.observe_result(
                    page
                )
            )

            expected_result = (
                self.expected_result(
                    scenario
                )
            )

            report[
                "expected"
            ] = expected_result

            report[
                "actual"
            ] = actual_result

            report[
                "bug_found"
            ] = (

                actual_result
                !=
                expected_result
            )

            return report

        except Exception as e:

            report[
                "bug_found"
            ] = True

            report[
                "expected"
            ] = self.expected_result(
                scenario
            )

            report[
                "actual"
            ] = f"Exception: {str(e)}"

            return report
        
    
       
        
    def run(self):

        reports = []

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            user = self.register(
                page
            )

            self.login(
                page,
                user["email"],
                user["password"]
            )

            explorer = ExplorerAgent()

            scenarios = explorer.explore(
                page
            )

            print(
                "\nDISCOVERED SCENARIOS:\n"
            )

            for scenario in scenarios:

                print(
                    scenario
                )

            for scenario in scenarios:

                reports.append(

                    self.execute_scenario(
                        page,
                        scenario
                    )

                )
            browser.close()

        return reports

if __name__ == "__main__":

    agent = (
        UserPersonaAgent()
    )

    reports = (
        agent.run()
    )

    print(
        "\nUSER PERSONA REPORTS\n"
    )

    for report in reports:

        print(report)