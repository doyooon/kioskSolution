from dateutil.parser import parse
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from rasa_sdk.forms import FormValidationAction
# import uuid
import json
from typing import Any, Dict, List, Text, Optional
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import requests
from rasa_sdk.events import ReminderScheduled
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import Restarted

def request_rpa_api(docuType, startDate, endDate, utime, reason):
    
    datas ={
            # "Id": str(uuid.uuid4()), #개체 고유식별자
            "docuType": docuType,
            "startDate": startDate,
            "endDate": endDate,
            "utime": utime,
            "reason": reason
    }
    
    print(f"request_info = ", datas)
    try:
        url = "http://localhost:8090/web/chatInsert.do"
        
        headers = {"Content-Type":"application/json; charset=utf-8", "Accept": "application/json"}
        # cookies = {}
        
        response = requests.post(url, json=datas, headers=headers)
        print('response =', response)

    except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
    return response


# 폼 제출 action
class SubmiForm(Action):

    def name(self) -> Text:
        return "submit_form"

    # async 비동기방식
    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        docuType = tracker.get_slot("docuType")
        startDate = tracker.get_slot("startDate")
        endDate = tracker.get_slot("endDate")
        utime= tracker.get_slot("utime")
        reason = tracker.get_slot("reason")

        request_rpa_api(docuType, startDate, endDate, utime, reason)
        dispatcher.utter_message("기안문 저장이 완료되었습니다.")

        return []
    
    
# 연차 휴직
class ValidateDayoffRestForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_dayoff_rest_form"

    """Example of a form validation action."""

    @staticmethod
    def workscope_db() -> List[Text]:
        """Database of supported workscope by DOWOORI."""
        # 도우리가 지원하는 업무범위 정의
        return [
            "연차",
            "반차", 
            "사직",
            "휴직"
        ]
    
    
    def validate_docuType(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate docuType value."""
        
        if value.lower() in self.workscope_db():
            # validation succeeded, set the value of the "workscope" slot to value
            # 조건문 : workscope_db안에 해당하는 업무일 경우 value 값 반환
            print("연차 종류 >>", value)
            return {"docuType": value}
        else:
            dispatcher.utter_message(response="utter_wrong_workscope")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            print("연차 종류 제대로 안들어옴 ")
            return {"docuType": None}

    def validate_startDate(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        
        print("연차 startDate >> ", value)
        
        return {"startDate": value}
     
    
     
    def validate_endDate(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        # date slot에 할당된 value값 뽑아내기
        stdate = tracker.get_slot("startDate")
        eddate = tracker.get_slot("endDate")
        print("stdate >>>> ", stdate)
        print("eddate >>>>",eddate)
        
        sdate=parse(stdate)
        edate=parse(eddate)
        
        if sdate > edate:
            dispatcher.utter_message("시작일 보다 종료일이 빠릅니다. 다시 입력해주시길 바랍니다.")
            return {"endDate": None}
        else:
            return {"endDate": value}
        
     
    def validate_reason(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate reason value."""
        print("연차 reason >> ", value)
        return {"reason": value}

# 반차 사직 actions    
class ValidateHalfoffResignForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_halfoff_resign_form"

    """Example of a form validation action."""

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        for key, value in tracker.current_slot_values().items():
            if value=="사직":
                slots_mapped_in_domain.remove("utime")
        return slots_mapped_in_domain
    
    @staticmethod
    def workscope_db() -> List[Text]:
        """Database of supported workscope by DOWOORI."""
        # 도우리가 지원하는 업무범위 정의
        return [
            "연차",
            "반차", 
            "사직",
            "휴직"
        ]
    
    def validate_docuType(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate docuType value."""
        
        if value.lower() in self.workscope_db():
            print("docuType : 반차 및 사직")
            return {"docuType": value}
        else:
            dispatcher.utter_message(response="utter_wrong_workscope")
            print("docuType 제대로 안들어옴(반차,사직부분)")
            return {"docuType": None}
     
    def validate_startDate(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        print("반차 및 사직일 startDate 출력!", value)
        return {"startDate": value}
  
    def validate_utime(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        return {"utime": value}
    
    def validate_reason(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate reason value."""
        return {"reason": value}
    

# 예외 단어 처리
class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
    
# 알림설정 알려주기  
class ActionSetReminder(Action):
        
    def name(self) -> Text:
            return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text,Any],
    ) -> List[Dict[Text,Any]]:
        
        dispatcher.utter_message("10초뒤 알림기능이 설정되었습니다.")
        date=datetime.now() + timedelta(seconds=10) # hours=2
        entities=tracker.latest_message.get("entities")
        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time= date,
            entities= entities,
            name= "my_reminder",
            kill_on_user_message= False
        )
        
        return [reminder]
    
    
# 실제 알람 반응
class ActionReactToReminder(Action):
        
    def name(self) -> Text:
            return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text,Any],
    ) -> List[Dict[Text,Any]]:
        
        # docuType = tracker.get_slot("docuType")
        # docuType = next(tracker.get_latest_entity_values("docuType"),"someone")
        dispatcher.utter_message(f"기안문 확인 알람입니다!! \n\n 결재현황을 확인해주세요!")
        
        return []
    
class ActionRestarted(Action):

    def name(self) -> Text:
        return "action_restart"   
    
    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        return [Restarted()]