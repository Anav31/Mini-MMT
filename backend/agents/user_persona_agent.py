import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from fastapi.testclient import TestClient

from app import app

from agents.scenarios import SCENARIOS

from agents.inspector_agent import InspectorAgent
from agents.architect_agent import (
    ArchitectAgent
)

client = TestClient(app)


class UserPersonaAgent:

    def run(self):

        results = []

        for scenario in SCENARIOS:

            response = client.post(

                scenario["endpoint"],

                json=scenario["payload"]

            )

            actual_message = response.json().get(
                "message",
                "No Message"
            )

            results.append({

                "module":
                scenario["module"],

                "scenario":
                scenario["name"],

                "expected":
                scenario["expected"],

                "actual":
                actual_message,

                "test_passed":
                (
                    actual_message
                    ==
                    scenario["expected"]
                )
            })

        return results


if __name__ == "__main__":

    user_agent = UserPersonaAgent()

    results = user_agent.run()

    print(
        "\nUSER PERSONA RESULTS\n"
    )

    for item in results:

        print(item)

    inspector = InspectorAgent()

    reports = inspector.inspect(
        results
    )

    print(
        "\nINSPECTOR REPORTS\n"
    )

    for report in reports:
        print(report)
    architect = ArchitectAgent()
    analysis = architect.analyze(reports)
    print("\nARCHITECT REPORTS\n")
    for item in analysis:
        print(item)