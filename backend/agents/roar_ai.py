import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.user_persona_agent import (
    UserPersonaAgent
)

from agents.inspector_agent import (
    InspectorAgent
)

from agents.architect_agent import (
    ArchitectAgent
)

from agents.engineer_agent import (
    EngineerAgent
)

from retester_agent import (
    ValidationAgentV2
)

from self_healing_agent import (
    ExecutorAgentV2
)

from agents.healing_logger import (
    HealingLogger
)


class SelfHealingOrchestrator:

    def run(self):

        logger = HealingLogger()

        print("\n")
        print("=" * 70)
        print("            ROAR AI - SELF HEALING AUTONOMOUS PIPELINE")
        print("=" * 70)

        ####################################################
        # STEP 1 : USER PERSONA
        ####################################################

        print("\n[STEP 1] USER PERSONA AGENT")

        user_agent = UserPersonaAgent()

        results = user_agent.run()

        print(f"✓ Completed")
        print(f"Validation Reports : {len(results)}")

        ####################################################
        # STEP 2 : INSPECTOR
        ####################################################

        print("\n[STEP 2] INSPECTOR AGENT")

        inspector = InspectorAgent()

        inspector_reports = inspector.inspect(results)

        bugs = inspector_reports

        print("✓ Completed")
        print(f"Root Causes Found : {len(bugs)}")

        ####################################################
        # HEALTHY SYSTEM
        ####################################################

        if not bugs:

            cycle_data = {

                "cycle_id":
                logger.generate_cycle_id(),

                "timestamp":
                logger.current_timestamp(),

                "bugs_found":
                0,

                "bugs_fixed":
                0,

                "patches_applied":
                0,

                "confidence_score":
                100,

                "system_status":
                "HEALTHY"

            }

            logger.save_cycle(cycle_data)

            print("\nSystem Status : HEALTHY")
            print("=" * 70)

            return cycle_data

        ####################################################
        # STEP 3 : ARCHITECT
        ####################################################

        print("\n[STEP 3] ARCHITECT AGENT")

        architect = ArchitectAgent()

        architect_reports = architect.analyze(
            inspector_reports
        )

        print("✓ Completed")
        print(f"Architecture Reports : {len(architect_reports)}")

        ####################################################
        # STEP 4 : ENGINEER
        ####################################################

        print("\n[STEP 4] ENGINEER AGENT")

        engineer = EngineerAgent()

        patches = engineer.generate_fix(
            architect_reports
        )

        tests = engineer.generate_tests(
            architect_reports
        )

        print("✓ Completed")
        print(f"Patches Generated : {len(patches)}")
        print(f"Test Suites Generated : {len(tests)}")

        ####################################################
        # STEP 5 : EXECUTOR
        ####################################################

        print("\n[STEP 5] SELF HEALING EXECUTOR")

        executor = ExecutorAgentV2()

        execution_reports = executor.execute(
            patches
        )

        patches_applied = len([

            report

            for report in execution_reports

            if report.get("status") == "PATCH_DEPLOYED"

        ])

        patches_already_present = len([

            report

            for report in execution_reports

            if report.get("status") == "PATCH_ALREADY_PRESENT"

        ])

        successful_healing = (

            patches_applied

            +

            patches_already_present

        )

        print("✓ Completed")

        print(f"Patches Applied         : {patches_applied}")

        print(f"Already Present         : {patches_already_present}")

        print(f"Successful Healing      : {successful_healing}")
        ####################################################
        # STEP 6 : RETESTER
        ####################################################

        print("\n[STEP 6] RETESTER AGENT")

        validator = ValidationAgentV2()

        validation_reports = validator.validate(
            results
        )

        fixed = len([
            report
            for report in validation_reports
            if report["bug_fixed"]
        ])

        print("✓ Completed")
        print(f"Validated Fixes : {fixed}")

        ####################################################
        # STEP 7 : LOGGER
        ####################################################

        print("\n[STEP 7] HEALING LOGGER")

        confidence = round(

            (

                successful_healing

                /

                max(len(bugs), 1)

            ) * 100,

            2

        )
        cycle_data = {

            "cycle_id":
            logger.generate_cycle_id(),

            "timestamp":
            logger.current_timestamp(),

            "bugs_found":
            len(bugs),

            "bugs_fixed":
            successful_healing,

            "patches_applied":
            patches_applied,

            "patches_already_present":
            patches_already_present,

            "confidence_score":
            confidence,

            "system_status":
            "HEALING_COMPLETE",

            "architect_reports":
            architect_reports,

            "validation_reports":
            validation_reports,

            "execution_reports":
            execution_reports

        }

        logger.save_cycle(cycle_data)

        print("✓ Healing Cycle Saved")

        ####################################################
        # FINAL SUMMARY
        ####################################################

        print("\n")
        print("=" * 70)
        print("                 ROAR AI EXECUTION SUMMARY")
        print("=" * 70)

        print(f"User Persona Reports : {len(results)}")
        print(f"Bugs Found           : {len(bugs)}")
        print(f"Patches Generated    : {len(patches)}")
        print(f"Patches Applied      : {patches_applied}")
        print(f"Already Present      : {patches_already_present}")
        print(f"Successful Healing   : {successful_healing}")
        print(f"Validated Fixes      : {fixed}")
        print(f"Confidence Score     : {confidence}%")

        print("\nSystem Status : HEALING COMPLETE")

        print("=" * 70)

        return cycle_data

if __name__ == "__main__":

    orchestrator = (
        SelfHealingOrchestrator()
    )

    report = (
        orchestrator.run()
    )

    print(
        "\nSELF HEALING REPORT\n"
    )

    print(report)