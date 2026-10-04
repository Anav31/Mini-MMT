from user_persona_agent import UserPersonaAgent
from inspector_agent import InspectorAgent
from architect_agent import ArchitectAgent
from engineer_agent import EngineerAgent


####################################################

user_reports = UserPersonaAgent().run()

print("\nUSER REPORTS\n")

for report in user_reports:
    print(report)



####################################################

inspector_reports = InspectorAgent().inspect(

    user_reports

)

print("\nINSPECTOR REPORTS\n")

for report in inspector_reports:
    print(report)


####################################################

architect_reports = ArchitectAgent().analyze(

    inspector_reports

)

print("\nARCHITECT REPORTS\n")

for report in architect_reports:
    print(report)


####################################################

engineer = EngineerAgent()

engineer_reports = engineer.generate_fix(

    architect_reports

)

print("\nENGINEER REPORTS\n")

for report in engineer_reports:
    print(report)