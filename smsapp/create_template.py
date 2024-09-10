import requests

def template_create(waba_id,template_name, language, category, header_type,header_content,body_text,footer_text,call_button_text,phone_number,url_button_text,website_url):


    url = f'https://graph.facebook.com/v20.0/{waba_id}/message_templates'
    token1="Bearer EAAOPkGzfCvsBO5XzFGoAvCFlBdqw436heEJVmk7fsxH6WqXo8wMri5e8SImPpoJivRaITMh7ZAfBnVTmYTAOREpDHQG9jlPANZCrnd5ZBoIZBCZBnzfeqihDjXP2zWl1jwqFxmEsQwZAS7QNxw7bp6YVQj9E1H3KIyVPQhDT1MUyHO42Ifmj7DSOaNtBrYaBJVQeELHhz2UeA4JiDs0hXLSUMt0Lqlvs2a2yRS4ili"
    token2="Bearer EAAGnWBuof2oBO8EUKs94mmrIeQjrneD9A4lAhZCLQXxZB8HyitAxbyGucbYLm8VoSoxeAsyTsBKioFDSktX3tBe8ytWaWHlS7up2m1BDjy5Y0pZAv4JyPMD4Ujfs7hJZAKE5CIzseNHQyImZAzpNol6AUCuYZAfAUzj1ik4TRXj9OuYfwKVOHPznVb5yZCBOpiP2UWZCYIrIGcUan0TKA9axCc1lrkPl9itO7Van2c7j"
    token3="Bearer EAAX4JBLg3MgBOZCXmE6QQncXD0ZBeq4FhpZBkODTfVcBxNdMUDkrT0ZC2jzde323MQAkZBB2ikgkZBbJkZBuWajKmDObk5buKyDeOelq76tf6pCDL7EsfsOp5Vaw2T4cBxOsExvqmKtm8P5h6KmC1sd8iY5sY1J1Ojgsjuv8gAZAETsYThuVhvCQHCCJ7SzuH2bzJ50Uv0wVc0AyCLPExmYGFpVXK60zrjtym7znWWIb"
    token=None
    if waba_id =="332618029945458" or waba_id== "330090043524228" or waba_id =="383548151515080" or waba_id =="391799964022878": 
        token=token1
    elif waba_id =="409990208861505" or waba_id == "397930006742161" or waba_id=="406024185930467":
        token=token3
        
    elif waba_id=="389460670923677" or waba_id == "401368339722342":
        token=token2

    components = []

    # Create header component if provided
    if header_type and header_content:
        if header_type == "headerText":
            components.append({
                "type": "HEADER",
                "format": "TEXT",
                "text": header_content
            })
        elif header_type in ["headerImage", "headerDocument", "headerVideo","headerAudio"]:
            components.append({
                "type": "HEADER",
                "format": header_type.split("header")[-1].upper(),
                "example": {
                    "header_handle": [
                        header_content
                    ]
                }
            })
        else:
            
            return

    # Add body component
    components.append({
        "type": "BODY",
        "text": body_text
    })

    # Add footer component if provided
    if footer_text:
        components.append({
            "type": "FOOTER",
            "text": footer_text
        })

    # Create button components if provided
    buttons = []
    if call_button_text and phone_number:
        buttons.append({
            "type": "PHONE_NUMBER",
            "text": call_button_text,
            "phone_number":phone_number
        })
    if url_button_text and website_url:
        buttons.append({
            "type": "URL",
            "text": url_button_text,
            "url": website_url
        })
    if buttons:
        components.append({
            "type": "BUTTONS",
            "buttons": buttons
        })

    payload = {
        "name": template_name,
        "language": language,
        "category": category,
        "components": components
    }

    headers = {
        'Authorization': token
    }
    

    response = requests.post(url=url, json=payload, headers=headers)
    response_dict = response.json()
    
   
   
    return response.status_code,response_dict

    
    
'''
template_create(
    waba_id="318794741325676",
    template_name="example_template1",
    language="en_US",
    category="Marketing",
    header_type="headerImage",
    header_content="4::YXBwbGljYXRpb24vb2N0ZXQtc3RyZWFt:ARbp3NxfKCTnotO_6ZojyIsDak1YDrcmaku_jJl4cJvKk-nrt6lKBgNDKTf-G9kElPUR-74ab9bwgGOqSunXE_6HkQz1ltZL3_23pnKYcg0Zxg:e:1720928506:1002275394751227:61560603673003:ARbQbHWnFfKRtUWd7_g",
    body_text="This is the body of the template.",
    footer_text="This is the footer.",
    call_button_text="Call Us",
    phone_number="+917905968734",
    url_button_text="Visit Website",
    website_url="https://example.com"
)

'''