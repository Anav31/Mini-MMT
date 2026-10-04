from retester_agent import ValidationAgentV2

sample_results = [

    {
        "module":"flight",
        "scenario":"negative_passengers",
        "expected":"Passenger count must be greater than 0",
        "actual":"Page Loaded",
        "bug_found":True
    }

]

validator = ValidationAgentV2()

reports = validator.validate(
    sample_results
)

print("\nVALIDATION REPORTS\n")

for report in reports:
    print(report)