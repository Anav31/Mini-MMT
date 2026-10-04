import os
import shutil
import ast
import subprocess

class ExecutorAgentV2:

    def create_backup(
        self,
        target_file
    ):

        backup_dir = "backups"

        os.makedirs(
            backup_dir,
            exist_ok=True
        )

        filename = os.path.basename(
            target_file
        )

        backup_path = os.path.join(
            backup_dir,
            filename + ".bak"
        )

        shutil.copy2(
            target_file,
            backup_path
        )

        return backup_path

    def rollback(
        self,
        backup_file,
        target_file
    ):

        shutil.copy2(
            backup_file,
            target_file
        )

    def patch_exists(
        self,
        source_code,
        code_patch
    ):

        patch_keywords = [

            "Passenger count must be greater than 0",

            "Rooms booked must be greater than 0",

            "Invalid Passenger Count"

        ]

        for keyword in patch_keywords:

            if keyword in source_code:

                return True

        return False

    def validate_syntax(
        self,
        source_code
    ):

        try:

            ast.parse(
                source_code
            )

            return True

        except SyntaxError:

            return False

    def format_patch(
        self,
        code_patch
    ):

        lines = code_patch.strip().splitlines()

        formatted = []

        for line in lines:

            if line.strip():

                formatted.append(
                    "    " + line.lstrip()
                )

            else:

                formatted.append("")

        return "\n".join(
            formatted
        )
    
    def apply_patch(
        self,
        target_file,
        target_function,
        code_patch
    ):

        with open(
            target_file,
            "r",
            encoding="utf-8"
        ) as file:

            source_code = file.read()

        function_signature = (
            f"def {target_function}"
        )

        if function_signature not in source_code:

            return {

                "patch_applied":
                False,

                "reason":
                "FUNCTION_NOT_FOUND"
            }

        if self.patch_exists(
            source_code,
            code_patch
        ):

            return {

                "patch_applied":
                False,

                "reason":
                "PATCH_ALREADY_PRESENT"
            }

        function_start = source_code.find(
            function_signature
        )

        body_start = source_code.find(
            "\n",
            function_start
        ) + 1

        formatted_patch = (
            self.format_patch(
                code_patch
            )
        )

        modified_code = (

            source_code[:body_start]

            +

            formatted_patch

            +

            "\n"

            +

            source_code[body_start:]

        )

        if not self.validate_syntax(
            modified_code
        ):

            print(
                "\n===== GENERATED CODE =====\n"
            )

            print(
                modified_code
            )

            print(
                "\n==========================\n"
            )

            return {

                "patch_applied":
                False,

                "reason":
                "SYNTAX_VALIDATION_FAILED"
            }

        with open(
            target_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                modified_code
            )

        return {

            "patch_applied":
            True,

            "reason":
            "PATCH_APPLIED"
        }
    
    def run_tests(self):

        try:

            result = subprocess.run(

                ["pytest"],

                capture_output=True,

                text=True,

                cwd=os.getcwd()

            )

            return {

                "success":
                result.returncode == 0,

                "output":
                result.stdout,

                "errors":
                result.stderr
            }

        except Exception as e:

            return {

                "success":
                False,

                "output":
                "",

                "errors":
                str(e)
            }
    
    def calculate_confidence(
        self,
        syntax_valid,
        tests_passed
    ):

        score = 0

        if syntax_valid:

            score += 50

        if tests_passed:

            score += 50

        return score

    def execute(
        self,
        engineer_patches
    ):

        reports = []

        for patch in engineer_patches:

            target_file = patch[
                "target_file"
            ]

            if not os.path.exists(
                target_file
            ):

                reports.append({

                    "target_file":
                    target_file,

                    "status":
                    "FILE_NOT_FOUND"
                })

                continue

            backup_file = (
                self.create_backup(
                    target_file
                )
            )

            patch_result = (
                self.apply_patch(
                    target_file,
                    patch[
                        "target_function"
                    ],
                    patch[
                        "code_patch"
                    ]
                )
            )

            if not patch_result[
                "patch_applied"
            ]:

                if patch_result[
                    "reason"
                ] == (
                    "SYNTAX_VALIDATION_FAILED"
                ):

                    self.rollback(
                        backup_file,
                        target_file
                    )

                    confidence = 100

                    if patch_result["reason"] == "PATCH_ALREADY_PRESENT":

                        confidence = 100

                    elif patch_result["reason"] == "FUNCTION_NOT_FOUND":

                        confidence = 0

                    elif patch_result["reason"] == "SYNTAX_VALIDATION_FAILED":

                        confidence = 0

                    reports.append({

                        "target_file":
                        target_file,

                        "backup_file":
                        backup_file,

                        "patch_applied":
                        False,

                        "tests_passed":
                        False,

                        "rollback":
                        False,

                        "confidence":
                        confidence,

                        "status":
                        patch_result["reason"]

                    })
                else:

                    reports.append({

                        "target_file":
                        target_file,

                        "backup_file":
                        backup_file,

                        "patch_applied":
                        False,

                        "tests_passed":
                        False,

                        "rollback":
                        False,

                        "confidence":
                        0,

                        "status":
                        patch_result[
                            "reason"
                        ]
                    })

                continue

            test_result = (
                self.run_tests()
            )

            if not test_result[
                "success"
            ]:

                self.rollback(

                    backup_file,

                    target_file
                )

                reports.append({

                    "target_file":
                    target_file,

                    "backup_file":
                    backup_file,

                    "patch_applied":
                    True,

                    "tests_passed":
                    False,

                    "rollback":
                    True,

                    "confidence":
                    50,

                    "status":
                    "ROLLED_BACK",

                    "errors":
                    test_result[
                        "errors"
                    ]
                })

                continue

            confidence = (
                self.calculate_confidence(

                    syntax_valid=True,

                    tests_passed=True
                )
            )

            reports.append({

                "target_file":
                target_file,

                "backup_file":
                backup_file,

                "patch_applied":
                True,

                "tests_passed":
                True,

                "rollback":
                False,

                "confidence":
                confidence,

                "status":
                "PATCH_DEPLOYED"
            })

        return reports