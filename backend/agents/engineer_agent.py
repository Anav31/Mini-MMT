from logging import root


class EngineerAgent:


    #################################################

    def generate_fix(
            self,
            architect_reports
    ):

        reports = []

        for report in architect_reports:

            if report["root_cause"] == "Unknown Failure":

                continue

            reports.append(
                self.build_fix(report)
            )


        return reports


    #################################################

    def build_fix(self,report):

        module = report["module"]

        root = report["root_cause"]



        return{


        "module":module,


        "priority":report["priority"],



        #################################

        "target_file":


        report["backend_file"],


        #################################


        "target_function":


        report["backend_function"],



        #################################


        "code_patch":


        self.backend_patch(root),



        #################################


        "frontend_patch":

        self.frontend_patch(root),



        "database_patch":

        self.database_patch(root),



        "confidence":

        self.confidence(root),



        "estimated_fix_time":

        self.fix_time(root)


        }
    #################################################

    def get_target_file(self,report):


        root=report["root_cause"]


        module=report["module"]



        mapping={


            "flight":

            "routes/flights.py",



            "bus":

            "routes/buses.py",



            "train":

            "routes/trains.py",



            "hotel":

            "routes/hotels.py"

        }


        return mapping.get(

            module,

            ""

        )
    
    def get_target_function(

            self,

            report

    ):



        root=report["root_cause"]


        module=report["module"]



        if root=="Validation Failure":



            mapping={


                "flight":"search_flights",

                "bus":"search_buses",

                "train":"search_trains",

                "hotel":"book_hotel"

            }


            return mapping.get(

                module

            )




        if root=="Booking Creation Failure":


            return "create_booking"



        return ""

    def build_patch(self, root):

        if root == "Validation Failure":

            return '''
    if data["passengers"] <= 0:
        return {
            "message":
            "Passenger count must be greater than 0"
        }
    '''

        if root == "Booking Creation Failure":

            return '''
    if not booking_created:
        raise Exception(
            "Booking Failed"
        )
    '''
        
        if root == "Cancellation Failure":

            return '''
        if not booking:
            return {
                "message":
                "Booking Not Found"
            }
        '''

        return ""
    ############################################################

    def frontend_patch(self, root):

        patches = {

            "Validation Failure":
            '''
    Validate inputs before API call

    if passengers <= 0:

        toast.error(
            "Passengers Invalid"
        )

    return
    ''',

            "Booking Creation Failure":
            '''
    Disable booking button

    until API confirms success
    '''
        }

        return patches.get(
            root,
            "Manual Frontend Review"
        )

    ############################################################

    def backend_patch(self, root):

        return self.build_patch(root)

    ############################################################

    def database_patch(self, root):

        patches = {

            "Validation Failure":
            "No DB Change Required",

            "Booking Creation Failure":
            '''
    ALTER TABLE bookings

    ADD CONSTRAINT passenger_positive

    CHECK(passengers > 0);
    '''
        }

        return patches.get(
            root,
            "Manual DB Review"
        )

    ############################################################

    def unit_tests(self, root):

        tests = {

            "Validation Failure":
            '''
    def test_invalid_passenger():

        response = api()

        assert response.status_code == 400
    ''',

            "Booking Creation Failure":
            '''
    def test_booking_created():

        assert booking_id
    '''
        }

        return tests.get(
            root,
            "Manual Unit Test"
        )

    ############################################################

    def integration_tests(self, root):

        tests = {

            "Validation Failure":
            '''
    Search API

    Frontend Validation

    Backend Validation
    ''',

            "Booking Creation Failure":
            '''
    Booking API

    Database

    Booking History

    Verification
    '''
        }

        return tests.get(
            root,
            "Manual Integration Test"
        )

    ############################################################

    def regression_tests(self, root):

        tests = {

            "Validation Failure":
            '''
    Run complete search suite

    Flights
    Bus
    Train
    Hotel
    ''',

            "Booking Creation Failure":
            '''
    Run booking suite

    Flights
    Bus
    Train
    Hotel
    '''
        }

        return tests.get(
            root,
            "Manual Regression Test"
        )
    
    def confidence(self,root):



        confidence={


            "Validation Failure":95,

            "Booking Creation Failure":90


        }


        return confidence.get(

            root,

            60

        )



############################################################



    def fix_time(self,root):



        mapping={


            "Validation Failure":"15 Minutes",


            "Booking Creation Failure":"30 Minutes"



        }



        return mapping.get(

            root,

            "Unknown"

        )
    
    def generate_tests(


            self,

            architect_reports

    ):


        tests=[]



        for report in architect_reports:



            tests.append({



                "module":


                report["module"],



                "unit_test":


                self.unit_tests(


                    report["root_cause"]

                ),




                "integration_test":


                self.integration_tests(


                    report["root_cause"]

                ),




                "regression_test":


                self.regression_tests(


                    report["root_cause"]

                )



            })




        return tests



############################################################



if __name__=="__main__":



    sample=[


        {


            "module":"flight",


            "root_cause":"Validation Failure",


            "priority":"P2"


        }


    ]



    engineer=EngineerAgent()



    reports=engineer.generate_fix(

        sample

    )



    print(

        "\nENGINEER REPORTS\n"

    )



    for r in reports:


        print(r)