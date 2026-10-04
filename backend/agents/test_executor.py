from architect_agent import ArchitectAgent
from engineer_agent import EngineerAgent
from self_healing_agent import ExecutorAgentV2


sample_inspector_report = [

    {

        "module": "flight",

        "root_cause": "Validation Failure",

        "severity": "MEDIUM",

        "count": 4,

        "affected_scenarios": [

            "empty_text",

            "negative_value",

            "zero_value"

        ]

    }

]


architect = ArchitectAgent()

architect_reports = (

    architect.analyze(

        sample_inspector_report

    )

)

print("\nARCHITECT REPORTS\n")

for report in architect_reports:

    print(report)


engineer = EngineerAgent()

patches = (

    engineer.generate_fix(

        architect_reports

    )

)

print("\nGENERATED PATCHES\n")

for patch in patches:

    print(patch)


executor = ExecutorAgentV2()

reports = (

    executor.execute(

        patches

    )

)

print("\nEXECUTOR REPORTS\n")

for report in reports:

    print(report)