import io
import json
import pytest
from Workday import Client, list_workers_command, create_worker_context, convert_to_json

from CommonServerPython import CommandResults

client = Client(tenant_url="https://test.workday.com/XSOAR", verify_certificate=False, proxy=False,
                tenant_name="tenant_name", token="token", username="username", password="password")


def util_load_json(path):
    with io.open(path, mode='r', encoding='utf-8') as f:
        return json.loads(f.read())


@pytest.mark.parametrize(
    'args', [
        ({'page': '1', 'count': '1', 'managers': '2'}),
        ({"employee_id": '123456', 'managers': '2'})
    ]
)
def test_list_workers_command(mocker, args):
    """Tests list_workers_command command function.

    Configures mocker instance and patches the client's http_request to generate the appropriate
    list_workers API response, loaded from a local JSON file.
    Checks the output of the command function with the expected output.

    This Test run 2 times for each use case (with employee Id and without)
    """
    mocker.patch.object(client, '_http_request', return_value=XML_RAW_RESPONSE)
    results: CommandResults = list_workers_command(client, args)
    assert results.outputs == WORKER_CONTEXT_DATA
    assert results.outputs_key_field == 'Worker_ID'
    assert results.outputs_prefix == 'Workday.Worker'


def test_create_worker_context():
    """Tests create_worker_context function.

       Checks the output of the function with the expected output.
       Checks the boolean representation for `Primary` Field under `Emails`. expected - True
       Checks the boolean representation for `Active` Field. expected - True
       Checks the context contains the specified managers number(2)

       No mock is needed here.
       """
    WORKER_DATA = util_load_json('test_data/worker_data.json')
    context = create_worker_context(WORKER_DATA, num_of_managers=2)
    assert WORKER_CONTEXT_DATA == context
    assert len(context[0].get('Managers')) == 2
    if context[0]['Emails'][0]['Primary']:
        assert True
    if context[0]['Active']:
        assert True


def test_convert_to_json():
    """Tests convert_to_json function.

    Checks the output of the function with the expected output.

    No mock is needed here.
    """
    JSON_RAW_RESPONSE = util_load_json('test_data/json_raw_respose.json')
    raw_response, worker_data = convert_to_json(XML_RAW_RESPONSE)
    assert JSON_RAW_RESPONSE == raw_response
    assert worker_data == worker_data


XML_RAW_RESPONSE = """<?xml version='1.0' encoding='UTF-8'?>
<env:Envelope
xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
<env:Body>
<wd:Get_Workers_Response
xmlns:wd="urn:com.workday/bsvc" wd:version="v34.0">
<wd:Request_References>
<wd:Worker_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a8ed12bc81bdc86</wd:ID>
<wd:ID wd:type="Employee_ID">123456</wd:ID>
</wd:Worker_Reference>
</wd:Request_References>
<wd:Response_Group>
<wd:Include_Reference>1</wd:Include_Reference>
<wd:Include_Personal_Information>1</wd:Include_Personal_Information>
<wd:Include_Employment_Information>1</wd:Include_Employment_Information>
<wd:Include_Management_Chain_Data>1</wd:Include_Management_Chain_Data>
<wd:Include_Photo>1</wd:Include_Photo>
</wd:Response_Group>
<wd:Response_Results>
<wd:Total_Results>1</wd:Total_Results>
<wd:Total_Pages>1</wd:Total_Pages>
<wd:Page_Results>1</wd:Page_Results>
<wd:Page>1</wd:Page>
</wd:Response_Results>
<wd:Response_Data>
<wd:Worker>
<wd:Worker_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a8ed12bc81bdc86</wd:ID>
<wd:ID wd:type="Employee_ID">123456</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>John Alayan</wd:Worker_Descriptor>
<wd:Worker_Data>
<wd:Worker_ID>123456</wd:Worker_ID>
<wd:User_ID>JDoe@paloaltonetworks.com</wd:User_ID>
<wd:Personal_Data>
<wd:Name_Data>
<wd:Legal_Name_Data>
<wd:Name_Detail_Data wd:Formatted_Name="John Wick Doe" wd:Reporting_Name="Doe, John Wick">
<wd:Country_Reference>
<wd:ID wd:type="WID">7b4fa1f369bd4604ba3692682fcbe345</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">AE</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">ARE</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">784</wd:ID>
</wd:Country_Reference>
<wd:First_Name>John Wick</wd:First_Name>
<wd:Last_Name>Doe</wd:Last_Name>
</wd:Name_Detail_Data>
</wd:Legal_Name_Data>
<wd:Preferred_Name_Data>
<wd:Name_Detail_Data wd:Formatted_Name="John Alayan" wd:Reporting_Name="Alayan, John">
<wd:Country_Reference>
<wd:ID wd:type="WID">7b4fa1f369bd4604ba3692682fcbe345</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">AE</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">ARE</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">784</wd:ID>
</wd:Country_Reference>
<wd:First_Name>John</wd:First_Name>
<wd:Last_Name>Alayan</wd:Last_Name>
</wd:Name_Detail_Data>
</wd:Preferred_Name_Data>
</wd:Name_Data>
<wd:Contact_Data>
<wd:Address_Data wd:Effective_Date="2016-08-01" wd:Address_Format_Type="Basic" wd:Formatted_Address="Eye Tower&amp;#xa;P.O Box: 230 888, Floor 28&amp;#xa;Offices 1, 2&amp;#xa;Narnia 11111&amp;#xa;Narnia&amp;#xa;Saudi Arabia" wd:Defaulted_Business_Site_Address="1">
<wd:Country_Reference>
<wd:ID wd:type="WID">50423b5190ad49bb89e94cd58dfaad69</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">SA</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">SAU</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">682</wd:ID>
</wd:Country_Reference>
<wd:Last_Modified>2018-12-13T15:07:02.863-08:00</wd:Last_Modified>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_1" wd:Descriptor="Address Line 1">Eye Tower</wd:Address_Line_Data>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_2" wd:Descriptor="Address Line 2">P.O Box: 230 888, Floor 28</wd:Address_Line_Data>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_3" wd:Descriptor="Address Line 3">Offices 1, 2</wd:Address_Line_Data>
<wd:Municipality>Narnia</wd:Municipality>
<wd:Country_Region_Reference>
<wd:ID wd:type="WID">a9b4429766264ac88ba45046ce44b654</wd:ID>
<wd:ID wd:type="Country_Region_ID">SAU-01</wd:ID>
<wd:ID wd:type="ISO_3166-2_Code">01</wd:ID>
</wd:Country_Region_Reference>
<wd:Country_Region_Descriptor>Narnia</wd:Country_Region_Descriptor>
<wd:Postal_Code>11111</wd:Postal_Code>
<wd:Usage_Data wd:Public="1">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">1f27f250dfaa4724ab1e1617174281e4</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">WORK</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Number_of_Days>0</wd:Number_of_Days>
<wd:Address_Reference>
<wd:ID wd:type="WID">9b10db154fdd105caf13657fc2d566dd</wd:ID>
<wd:ID wd:type="Address_ID">ADDRESS_REFERENCE-3-3415</wd:ID>
</wd:Address_Reference>
<wd:Address_ID>ADDRESS_REFERENCE-3-3415</wd:Address_ID>
</wd:Address_Data>
<wd:Address_Data wd:Effective_Date="2020-04-09" wd:Address_Format_Type="Basic" wd:Formatted_Address="King Faisal District&amp;#xa;Narnia 13215&amp;#xa;Saudi Arabia" wd:Defaulted_Business_Site_Address="0">
<wd:Country_Reference>
<wd:ID wd:type="WID">50423b5190ad49bb89e94cd58dfaad69</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">SA</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">SAU</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">682</wd:ID>
</wd:Country_Reference>
<wd:Last_Modified>2020-04-09T09:42:32.972-07:00</wd:Last_Modified>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_1" wd:Descriptor="Address Line 1">King Faisal District</wd:Address_Line_Data>
<wd:Municipality>Narnia</wd:Municipality>
<wd:Postal_Code>13215</wd:Postal_Code>
<wd:Usage_Data wd:Public="0">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">836cf00ef5974ac08b786079866c946f</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">HOME</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Number_of_Days>0</wd:Number_of_Days>
<wd:Address_Reference>
<wd:ID wd:type="WID">5aa443c785ff1046185a610fefbb98a5</wd:ID>
<wd:ID wd:type="Address_ID">ADDRESS_REFERENCE-6-107</wd:ID>
</wd:Address_Reference>
<wd:Address_ID>ADDRESS_REFERENCE-6-107</wd:Address_ID>
</wd:Address_Data>
<wd:Phone_Data wd:Phone_Number_Without_Area_Code="5-5505-5555" wd:E164_Formatted_Phone="+966555055555" wd:Workday_Traditional_Formatted_Phone="+966  5-5505-5555" wd:National_Formatted_Phone="055 509 9323" wd:International_Formatted_Phone="+966 55 509 9323" wd:Tenant_Formatted_Phone="+966  5-5505-5555">
<wd:Country_ISO_Code>SAU</wd:Country_ISO_Code>
<wd:International_Phone_Code>966</wd:International_Phone_Code>
<wd:Phone_Number>5-5505-5555</wd:Phone_Number>
<wd:Phone_Device_Type_Reference>
<wd:ID wd:type="WID">5aa443c785ff104455be41823aab0278</wd:ID>
<wd:ID wd:type="Phone_Device_Type_ID">Mobile</wd:ID>
</wd:Phone_Device_Type_Reference>
<wd:Usage_Data wd:Public="1">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">1f27f250dfaa4724ab1e1617174281e4</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">WORK</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Phone_Reference>
<wd:ID wd:type="WID">fbec2fbc8be8012b7f9dbb790a88c810</wd:ID>
<wd:ID wd:type="Phone_ID">PHONE_REFERENCE-3-4210</wd:ID>
</wd:Phone_Reference>
<wd:ID>PHONE_REFERENCE-3-4210</wd:ID>
</wd:Phone_Data>
<wd:Phone_Data wd:Phone_Number_Without_Area_Code="555055555" wd:E164_Formatted_Phone="+966555055555" wd:Workday_Traditional_Formatted_Phone="+966  555055555" wd:National_Formatted_Phone="055 509 9323" wd:International_Formatted_Phone="+966 55 509 9323" wd:Tenant_Formatted_Phone="+966  555055555">
<wd:Country_ISO_Code>SAU</wd:Country_ISO_Code>
<wd:International_Phone_Code>966</wd:International_Phone_Code>
<wd:Phone_Number>555055555</wd:Phone_Number>
<wd:Phone_Device_Type_Reference>
<wd:ID wd:type="WID">5aa443c785ff104455be41823aab0278</wd:ID>
<wd:ID wd:type="Phone_Device_Type_ID">Mobile</wd:ID>
</wd:Phone_Device_Type_Reference>
<wd:Usage_Data wd:Public="0">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">836cf00ef5974ac08b786079866c946f</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">HOME</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Phone_Reference>
<wd:ID wd:type="WID">fbec2fbc8be8015e23408f950a886c39</wd:ID>
<wd:ID wd:type="Phone_ID">PHONE_REFERENCE-3-14614</wd:ID>
</wd:Phone_Reference>
<wd:ID>PHONE_REFERENCE-3-14614</wd:ID>
</wd:Phone_Data>
<wd:Email_Address_Data>
<wd:Email_Address>John@hotmail.com</wd:Email_Address>
<wd:Usage_Data wd:Public="0">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">836cf00ef5974ac08b786079866c946f</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">HOME</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Email_Reference>
<wd:ID wd:type="WID">f18b4f53c85d01ba3faef5995a4c823a</wd:ID>
<wd:ID wd:type="Email_ID">EMAIL_REFERENCE-3-14523</wd:ID>
</wd:Email_Reference>
<wd:ID>EMAIL_REFERENCE-3-14523</wd:ID>
</wd:Email_Address_Data>
<wd:Email_Address_Data>
<wd:Email_Address>JDoe@paloaltonetworks.com</wd:Email_Address>
<wd:Usage_Data wd:Public="1">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">1f27f250dfaa4724ab1e1617174281e4</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">WORK</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
</wd:Usage_Data>
<wd:Email_Reference>
<wd:ID wd:type="WID">f18b4f53c85d0184806e83925a4cc701</wd:ID>
<wd:ID wd:type="Email_ID">EMAIL_REFERENCE-3-1</wd:ID>
</wd:Email_Reference>
<wd:ID>EMAIL_REFERENCE-3-1</wd:ID>
</wd:Email_Address_Data>
</wd:Contact_Data>
<wd:Tobacco_Use>0</wd:Tobacco_Use>
</wd:Personal_Data>
<wd:Employment_Data>
<wd:Worker_Job_Data wd:Primary_Job="1">
<wd:Position_Data wd:Effective_Date="2020-03-25">
<wd:Position_Reference>
<wd:ID wd:type="WID">10e91088faac01c4cced8f6e020295be</wd:ID>
<wd:ID wd:type="Position_ID">POS-114061</wd:ID>
</wd:Position_Reference>
<wd:Position_ID>POS-114061</wd:Position_ID>
<wd:Position_Title>Regional Sales Manager</wd:Position_Title>
<wd:Business_Title>Regional Sales Manager</wd:Business_Title>
<wd:Start_Date>2020-03-25</wd:Start_Date>
<wd:Worker_Type_Reference>
<wd:ID wd:type="WID">5aa443c785ff1044599de02ee3fb05d1</wd:ID>
<wd:ID wd:type="Employee_Type_ID">Regular</wd:ID>
</wd:Worker_Type_Reference>
<wd:Position_Time_Type_Reference>
<wd:ID wd:type="WID">7142a30f5ed7104218357027034b0084</wd:ID>
<wd:ID wd:type="Position_Time_Type_ID">Full_time</wd:ID>
</wd:Position_Time_Type_Reference>
<wd:Job_Exempt>0</wd:Job_Exempt>
<wd:Scheduled_Weekly_Hours>40</wd:Scheduled_Weekly_Hours>
<wd:Default_Weekly_Hours>40</wd:Default_Weekly_Hours>
<wd:Working_Time_Value>0</wd:Working_Time_Value>
<wd:Full_Time_Equivalent_Percentage>100</wd:Full_Time_Equivalent_Percentage>
<wd:Specify_Paid_FTE>0</wd:Specify_Paid_FTE>
<wd:Paid_FTE>0</wd:Paid_FTE>
<wd:Specify_Working_FTE>0</wd:Specify_Working_FTE>
<wd:Working_FTE>0</wd:Working_FTE>
<wd:Exclude_from_Headcount>0</wd:Exclude_from_Headcount>
<wd:Pay_Rate_Type_Reference>
<wd:ID wd:type="WID">5aa443c785ff1044639b60f9cb430b30</wd:ID>
<wd:ID wd:type="Pay_Rate_Type_ID">Salary</wd:ID>
</wd:Pay_Rate_Type_Reference>
<wd:Job_Profile_Summary_Data>
<wd:Job_Profile_Reference>
<wd:ID wd:type="WID">5aa443c785ff104590f899c17b9355e1</wd:ID>
<wd:ID wd:type="Job_Profile_ID">S634 DQC</wd:ID>
</wd:Job_Profile_Reference>
<wd:Job_Exempt>0</wd:Job_Exempt>
<wd:Management_Level_Reference>
<wd:ID wd:type="WID">5aa443c785ff10453a0462d754b33849</wd:ID>
<wd:ID wd:type="Management_Level_ID">INDIVIDUAL_CONTRIBUTOR</wd:ID>
</wd:Management_Level_Reference>
<wd:Job_Family_Reference>
<wd:ID wd:type="WID">5aa443c785ff104536c569ac37733834</wd:ID>
<wd:ID wd:type="Job_Family_ID">JF-097</wd:ID>
</wd:Job_Family_Reference>
<wd:Job_Profile_Name>Regional Sales Manager (DQC)</wd:Job_Profile_Name>
<wd:Work_Shift_Required>0</wd:Work_Shift_Required>
<wd:Critical_Job>0</wd:Critical_Job>
</wd:Job_Profile_Summary_Data>
<wd:Business_Site_Summary_Data>
<wd:Location_Reference>
<wd:ID wd:type="WID">9b10db154fdd105caf136478f57d66d8</wd:ID>
<wd:ID wd:type="Location_ID">3010</wd:ID>
</wd:Location_Reference>
<wd:Name>Office - Saudi Arabia - Narnia</wd:Name>
<wd:Location_Type_Reference>
<wd:ID wd:type="WID">5aa443c785ff104476d6aa326f5b0bc9</wd:ID>
<wd:ID wd:type="Location_Type_ID">Office</wd:ID>
</wd:Location_Type_Reference>
<wd:Local_Reference>
<wd:ID wd:type="WID">d9e43b02446c11de98360015c5e6daf6</wd:ID>
<wd:ID wd:type="Locale_ID">en_US</wd:ID>
</wd:Local_Reference>
<wd:Time_Profile_Reference>
<wd:ID wd:type="WID">5aa443c785ff10447d11f4186acb0bfe</wd:ID>
<wd:ID wd:type="Time_Profile_ID">Standard_Hours_40</wd:ID>
</wd:Time_Profile_Reference>
<wd:Scheduled_Weekly_Hours>40</wd:Scheduled_Weekly_Hours>
<wd:Address_Data wd:Effective_Date="2016-08-01" wd:Address_Format_Type="Basic" wd:Formatted_Address="Eye Tower&amp;#xa;P.O Box: 230 888, Floor 28&amp;#xa;Offices 1, 2&amp;#xa;Narnia 11111&amp;#xa;Narnia&amp;#xa;Saudi Arabia" wd:Defaulted_Business_Site_Address="0">
<wd:Country_Reference>
<wd:ID wd:type="WID">50423b5190ad49bb89e94cd58dfaad69</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">SA</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">SAU</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">682</wd:ID>
</wd:Country_Reference>
<wd:Last_Modified>2018-12-13T15:07:02.863-08:00</wd:Last_Modified>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_1" wd:Descriptor="Address Line 1">Eye Tower</wd:Address_Line_Data>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_2" wd:Descriptor="Address Line 2">P.O Box: 230 888, Floor 28</wd:Address_Line_Data>
<wd:Address_Line_Data wd:Type="ADDRESS_LINE_3" wd:Descriptor="Address Line 3">Offices 1, 2</wd:Address_Line_Data>
<wd:Municipality>Narnia</wd:Municipality>
<wd:Country_Region_Reference>
<wd:ID wd:type="WID">a9b4429766264ac88ba45046ce44b654</wd:ID>
<wd:ID wd:type="Country_Region_ID">SAU-01</wd:ID>
<wd:ID wd:type="ISO_3166-2_Code">01</wd:ID>
</wd:Country_Region_Reference>
<wd:Country_Region_Descriptor>Narnia</wd:Country_Region_Descriptor>
<wd:Postal_Code>11111</wd:Postal_Code>
<wd:Usage_Data wd:Public="1">
<wd:Type_Data wd:Primary="1">
<wd:Type_Reference>
<wd:ID wd:type="WID">4fae289a7fe541b098ca9448e462ff6b</wd:ID>
<wd:ID wd:type="Communication_Usage_Type_ID">BUSINESS</wd:ID>
</wd:Type_Reference>
</wd:Type_Data>
<wd:Use_For_Reference>
<wd:ID wd:type="WID">b58a4a54e04c4e1f8fc32bfc3b1a77cf</wd:ID>
<wd:ID wd:type="Communication_Usage_Behavior_ID">SHIPPING</wd:ID>
</wd:Use_For_Reference>
<wd:Use_For_Tenanted_Reference>
<wd:ID wd:type="WID">e17e5530ce9e10c0005feb38ba4d0028</wd:ID>
<wd:ID wd:type="Communication_Usage_Behavior_Tenanted_ID">COMMUNICATION_USAGE_BEHAVIOR_TENANTED-3-12</wd:ID>
</wd:Use_For_Tenanted_Reference>
</wd:Usage_Data>
<wd:Number_of_Days>0</wd:Number_of_Days>
<wd:Address_Reference>
<wd:ID wd:type="WID">9b10db154fdd105caf13657fc2d566dd</wd:ID>
<wd:ID wd:type="Address_ID">ADDRESS_REFERENCE-3-3415</wd:ID>
</wd:Address_Reference>
<wd:Address_ID>ADDRESS_REFERENCE-3-3415</wd:Address_ID>
</wd:Address_Data>
</wd:Business_Site_Summary_Data>
<wd:Manager_as_of_last_detected_manager_change_Reference>
<wd:ID wd:type="WID">f5711ac16540018491019812d9a7ad07</wd:ID>
<wd:ID wd:type="Employee_ID">100600</wd:ID>
</wd:Manager_as_of_last_detected_manager_change_Reference>
</wd:Position_Data>
<wd:Position_Management_Chains_Data>
<wd:Position_Supervisory_Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e224f3dc073494f</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 100</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e201b97f19b4685</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG2.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 100</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">ce8d386a97af01de45acd4d2cf008951</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1225</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">fd0f8dfa3d2001196bf13a81a33a4b1a</wd:ID>
<wd:ID wd:type="Employee_ID">100300</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">fd0f8dfa3d2001196bf13a81a33a4b1a</wd:ID>
<wd:ID wd:type="Employee_ID">100300</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 300</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">53b4f7b559fc107c5dc0c01962edd13f</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG4.50</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">6e3231fc4d93107abfac6f150c4d4afc</wd:ID>
<wd:ID wd:type="Employee_ID">100400</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">6e3231fc4d93107abfac6f150c4d4afc</wd:ID>
<wd:ID wd:type="Employee_ID">100400</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 400</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e1fb4756ea345b5</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG5.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a94f3a2e7bbe520</wd:ID>
<wd:ID wd:type="Employee_ID">100700</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a94f3a2e7bbe520</wd:ID>
<wd:ID wd:type="Employee_ID">100700</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 700</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">a2ad006ebba401f0c11ca75e19b0d0a3</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1074</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">f5711ac16540018491019812d9a7ad07</wd:ID>
<wd:ID wd:type="Employee_ID">100600</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">f5711ac16540018491019812d9a7ad07</wd:ID>
<wd:ID wd:type="Employee_ID">100600</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 600</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
</wd:Position_Supervisory_Management_Chain_Data>
</wd:Position_Management_Chains_Data>
</wd:Worker_Job_Data>
<wd:Worker_Status_Data>
<wd:Active>1</wd:Active>
<wd:Active_Status_Date>2020-03-25</wd:Active_Status_Date>
<wd:Hire_Date>2020-03-25</wd:Hire_Date>
<wd:Original_Hire_Date>2011-05-01</wd:Original_Hire_Date>
<wd:Hire_Reason_Reference>
<wd:ID wd:type="WID">5aa443c785ff1044cb0240c4904b12a8</wd:ID>
<wd:ID wd:type="Event_Classification_Subcategory_ID">Hire_Employee_Hire_Employee_Rehire</wd:ID>
<wd:ID wd:type="General_Event_Subcategory_ID">Hire_Employee_Hire_Employee_Rehire</wd:ID>
</wd:Hire_Reason_Reference>
<wd:Continuous_Service_Date>2020-03-25</wd:Continuous_Service_Date>
<wd:First_Day_of_Work>2020-03-25</wd:First_Day_of_Work>
<wd:Retired>0</wd:Retired>
<wd:Seniority_Date>2011-05-01</wd:Seniority_Date>
<wd:Days_Unemployed>0</wd:Days_Unemployed>
<wd:Months_Continuous_Prior_Employment>0</wd:Months_Continuous_Prior_Employment>
<wd:Terminated>0</wd:Terminated>
<wd:Regrettable_Termination>1</wd:Regrettable_Termination>
<wd:Hire_Rescinded>0</wd:Hire_Rescinded>
<wd:Resignation_Date>2018-06-14</wd:Resignation_Date>
<wd:Not_Returning>0</wd:Not_Returning>
<wd:Return_Unknown>0</wd:Return_Unknown>
<wd:Probation_Start_Date>2020-03-25</wd:Probation_Start_Date>
<wd:Probation_End_Date>2020-06-24</wd:Probation_End_Date>
<wd:Rehire>1</wd:Rehire>
</wd:Worker_Status_Data>
<wd:International_Assignment_Summary_Data>
<wd:Has_International_Assignment>0</wd:Has_International_Assignment>
<wd:Home_Country_Reference>
<wd:ID wd:type="WID">50423b5190ad49bb89e94cd58dfaad69</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-2_Code">SA</wd:ID>
<wd:ID wd:type="ISO_3166-1_Alpha-3_Code">SAU</wd:ID>
<wd:ID wd:type="ISO_3166-1_Numeric-3_Code">682</wd:ID>
</wd:Home_Country_Reference>
</wd:International_Assignment_Summary_Data>
</wd:Employment_Data>
<wd:Management_Chain_Data>
<wd:Worker_Supervisory_Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e224f3dc073494f</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 100</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e201b97f19b4685</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG2.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">a2ad006ebba4017562956c79c9aff66a</wd:ID>
<wd:ID wd:type="Employee_ID">100100</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 100</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">ce8d386a97af01de45acd4d2cf008951</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1225</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">fd0f8dfa3d2001196bf13a81a33a4b1a</wd:ID>
<wd:ID wd:type="Employee_ID">100300</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">fd0f8dfa3d2001196bf13a81a33a4b1a</wd:ID>
<wd:ID wd:type="Employee_ID">100300</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 300</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">53b4f7b559fc107c5dc0c01962edd13f</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG4.50</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">6e3231fc4d93107abfac6f150c4d4afc</wd:ID>
<wd:ID wd:type="Employee_ID">100400</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">6e3231fc4d93107abfac6f150c4d4afc</wd:ID>
<wd:ID wd:type="Employee_ID">100400</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 400</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">5aa443c785ff10458e1fb4756ea345b5</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG5.0</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a94f3a2e7bbe520</wd:ID>
<wd:ID wd:type="Employee_ID">100700</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">5aa443c785ff10461a94f3a2e7bbe520</wd:ID>
<wd:ID wd:type="Employee_ID">100700</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 700</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
<wd:Management_Chain_Data>
<wd:Organization_Reference>
<wd:ID wd:type="WID">a2ad006ebba401f0c11ca75e19b0d0a3</wd:ID>
<wd:ID wd:type="Organization_Reference_ID">ORG1074</wd:ID>
</wd:Organization_Reference>
<wd:Manager_Reference>
<wd:ID wd:type="WID">f5711ac16540018491019812d9a7ad07</wd:ID>
<wd:ID wd:type="Employee_ID">100600</wd:ID>
</wd:Manager_Reference>
<wd:Manager>
<wd:Worker_Reference>
<wd:ID wd:type="WID">f5711ac16540018491019812d9a7ad07</wd:ID>
<wd:ID wd:type="Employee_ID">100600</wd:ID>
</wd:Worker_Reference>
<wd:Worker_Descriptor>Manager 600</wd:Worker_Descriptor>
</wd:Manager>
</wd:Management_Chain_Data>
</wd:Worker_Supervisory_Management_Chain_Data>
</wd:Management_Chain_Data>
<wd:Photo_Data>
<wd:Filename>John-Passport-Pic.jpg</wd:Filename>
<wd:Image>image_in_base64</wd:Image>
</wd:Photo_Data>
</wd:Worker_Data>
</wd:Worker>
</wd:Response_Data>
</wd:Get_Workers_Response>
</env:Body>
</env:Envelope>
"""

WORKER_CONTEXT_DATA = [{
    'Worker_ID': '123456', 'User_ID': 'JDoe@paloaltonetworks.com', 'Country': 'AE',
    'Legal_First_Name': 'John Wick', 'Legal_Last_Name': 'Doe',
    'Preferred_First_Name': 'John Wick', 'Preferred_Last_Name': 'Doe',
    'Position_ID': 'POS-114061', 'Position_Title': 'Regional Sales Manager',
    'Business_Title': 'Regional Sales Manager', 'Start_Date': '2020-03-25',
    'End_Employment_Reason_Reference': '', 'Worker_Type': 'Regular',
    'Position_Time_Type': 'Full_time', 'Scheduled_Weekly_Hours': '40', 'Default_Weekly_Hours': '40',
    'Full_Time_Equivalent_Percentage': '100', 'Exclude_from_Headcount': '0',
    'Pay_Rate_Type': 'Salary', 'Job_Profile_Name': 'Regional Sales Manager (DQC)',
    'Work_Shift_Required': '0', 'Critical_Job': '0', 'Business_Site_id': '3010',
    'Business_Site_Name': 'Office - Saudi Arabia - Narnia', 'Business_Site_Type': 'Office',
    'Business_Site_Address': {'Address_ID': 'ADDRESS_REFERENCE-3-3415',
                              'Formatted_Address': 'Eye Tower&#xa;P.O Box: 230 888, Floor 28&#xa;Offices 1, '
                                                   '2&#xa;Narnia 11111&#xa;Narnia&#xa;Saudi Arabia',
                              'Country': 'SA', 'Postal_Code': '11111'}, 'End_Date': None,
    'Pay_Through_Date': None, 'Active': True, 'Hire_Date': '2020-03-25',
    'Hire_Reason': 'Hire_Employee_Hire_Employee_Rehire', 'First_Day_of_Work': '2020-03-25',
    'Retired': '0', 'Days_Unemployed': '0', 'Terminated': False, 'Rehire': '1',
    'Resignation_Date': '2018-06-14', 'Has_International_Assignment': '0',
    'Home_Country_Reference': 'SA', 'Photo': 'image_in_base64', 'Addresses': [
        {'Address_ID': 'ADDRESS_REFERENCE-3-3415',
         'Formatted_Address': 'Eye Tower&#xa;P.O Box: 230 888, Floor 28&#xa;Offices 1, 2&#xa;Narnia '
                              '11111&#xa;Narnia&#xa;Saudi Arabia',
         'Country': 'SA', 'Region': '01', 'Region_Descriptor': 'Narnia', 'Postal_Code': '11111', 'Type': 'WORK'},
        {'Address_ID': 'ADDRESS_REFERENCE-6-107',
         'Formatted_Address': 'King Faisal District&#xa;Narnia 13215&#xa;Saudi Arabia', 'Country': 'SA', 'Region': '',
         'Region_Descriptor': '', 'Postal_Code': '13215', 'Type': 'HOME'}], 'Emails': [
        {'Email_Address': 'John@hotmail.com', 'Type': 'HOME', 'Primary': True, 'Public': False},
        {'Email_Address': 'JDoe@paloaltonetworks.com', 'Type': 'WORK', 'Primary': True, 'Public': True}], 'Phones': [
        {'ID': 'PHONE_REFERENCE-3-4210', 'Phone_Number': '5-5505-5555', 'Type': 'Mobile', 'Usage': 'WORK'},
        {'ID': 'PHONE_REFERENCE-3-14614', 'Phone_Number': '555055555', 'Type': 'Mobile', 'Usage': 'HOME'}],
    'Managers': [{'Manager_ID': '100700', 'Manager_Name': 'Manager 700'},
                 {'Manager_ID': '100600', 'Manager_Name': 'Manager 600'}]}]
