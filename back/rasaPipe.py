
class RASAPipe(object):    
    def __init__(self, user_conversation_index):
        
        self.user_conversation_index = user_conversation_index

    def request_rasa_for_question(self, message):
        rasa_requestdata = {"message": message, 
                            "sender": self.user_conversation_index}
        x = requests.post(self.messages_url, json = rasa_requestdata)
        rasa_response = x.json()
        processed_rasa_response = self.process_rasa_response(rasa_response)
        return processed_rasa_response

class ChatBot(object):    
    def __init__(self, user_conversation_index, verbose=False):        
        self.id = user_conversation_index        
        self.asr = AS

class ChatBot(object):
    def __init__(self, user_conversation_index, verbose=False):
        self.id = user_conversation_index
        self.asr = ASRPipe()
        self.rasa = RASAPipe(user_conversation_index)
        self.tts = TTSPipe()
        self.thread_asr = None
        self.pause_asr_flag = False
        self.enableTTS = False

    def server_asr(self):
            self.asr.main_asr()
    def start_asr(self, sio):
        self.thread_asr = sio.start_background_task(self.server_asr)
    def asr_fill_buffer(self, audio_in):        
        if not self.pause_asr_flag:           
             self.asr.fill_buffer(audio_in)    
    def asr_fill_buffer(self, audio_in):
        if not self.pause_asr_flag:
            self.asr.fill_buffer(audio_in)
    def get_asr_transcript(self):
        return self.asr.get_transcript()
    
    def rasa_tts_pipeline(self, text):
        response_text = self.rasa.request_rasa_for_question(text)
        if len(response_text) and self.enableTTS == True:
            self.tts_fill_buffer(response_text)
        return response_text