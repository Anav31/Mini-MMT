from playwright.sync_api import sync_playwright


class ExplorerAgent:


    BASE_URL="http://localhost:3000"



    def explore(self,page):


        scenarios=[]


        modules=[

            ("flight",f"{self.BASE_URL}/flights"),

            ("bus",f"{self.BASE_URL}/buses"),

            ("train",f"{self.BASE_URL}/trains"),

            ("hotel",f"{self.BASE_URL}/hotels")

        ]


        for module,url in modules:


            page_data = self.inspect_page(

                    page,

                    module,

                    url

            )


            scenarios.extend(

                self.generate_scenarios(

                    page_data

                )

            )


        return scenarios




    ################################################


    def inspect_page(


            self,

            page,

            module,

            url

    ):


        page.goto(url)


        page.wait_for_timeout(2000)


        inputs=self.discover_inputs(page)


        buttons=self.discover_buttons(page)


        cards=self.discover_cards(page)


        links=self.discover_links(page)


        forms=self.discover_forms(page)



        return{


            "module":module,


            "url":url,


            "inputs":inputs,


            "buttons":buttons,


            "cards":cards,


            "links":links,


            "forms":forms

        }




#########################################################


    def discover_inputs(


            self,

            page

    ):


        discovered=[]


        elements=page.locator("input")



        for i in range(elements.count()):



            try:



                discovered.append({


                    "placeholder":elements.nth(i).get_attribute("placeholder"),


                    "type":elements.nth(i).get_attribute("type")


                })



            except:


                pass



        return discovered





#######################################################


    def discover_buttons(


            self,

            page

    ):



        buttons=[]


        elements=page.locator("button")



        for i in range(elements.count()):



            try:



                buttons.append({


                    "text":

                    elements.nth(i).inner_text(),


                    "index":i

                })



            except:


                pass




        return buttons






########################################################


    def discover_cards(


            self,

            page

    ):



        cards=[]



        elements=page.locator(


            ".flight-card"

        )



        for i in range(elements.count()):



            try:



                cards.append(


                    elements.nth(i).inner_text()

                )


            except:


                pass




        return cards





########################################################


    def discover_links(


            self,

            page

    ):



        links=[]



        elements=page.locator("a")



        for i in range(elements.count()):



            try:



                links.append({



                    "text":


                    elements.nth(i).inner_text(),



                    "href":


                    elements.nth(i).get_attribute(


                        "href"

                    )


                })



            except:


                pass




        return links






#######################################################


    def discover_forms(


            self,

            page

    ):



        forms=[]



        elements=page.locator("form")



        for i in range(elements.count()):



            forms.append(


                f"form_{i}"

            )



        return forms
    
    ########################################################


    def generate_scenarios(

            self,

            page_data

    ):


        scenarios=[]


        module = page_data["module"]



    ########################################


        scenarios.append({


            "module":module,


            "scenario":"normal_flow"

        })

        scenarios.append({

            "module":module,

            "scenario":"booking_flow"

        })

        scenarios.append({

            "module":module,

            "scenario":"cancel_booking"

        })



    ########################################


        for field in page_data["inputs"]:



            placeholder = field["placeholder"]

            field_type = field["type"]



    ########################################


            if field_type=="text":



                scenarios.append({


                    "module":module,


                    "scenario":"empty_text",


                    "field":placeholder

                })



                scenarios.append({


                    "module":module,


                    "scenario":"special_characters",


                    "field":placeholder

                })



    ########################################



            elif field_type=="number":



                scenarios.append({


                    "module":module,


                    "scenario":"negative_value",


                    "value":-1

                })



                scenarios.append({


                    "module":module,


                    "scenario":"zero_value",


                    "value":0

                })

        ###################################################
        # BOOKING SCENARIOS
        ###################################################

        scenarios.append({

            "module": module,

            "scenario": "booking_flow"

        })

        scenarios.append({

            "module": module,

            "scenario": "booking_negative_passengers"

        })

        scenarios.append({

            "module": module,

            "scenario": "booking_zero_passengers"

        })

        ###################################################
        # CANCELLATION SCENARIOS
        ###################################################

        scenarios.append({

            "module": module,

            "scenario": "cancel_booking"

        })

        scenarios.append({

            "module": module,

            "scenario": "cancel_invalid_booking"

        })




        return scenarios





#########################################################


if __name__=="__main__":



    print(

        "\nExplorer requires authenticated page"

    )



    print(

        "Run from User Persona Agent"

    )
