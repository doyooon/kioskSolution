import React, { useEffect, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import axios from "axios";

const styles = {
  chatContainer: {
    width: "400px",
    margin: "0 auto",
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "10px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  messageContainer: {
    height: "300px",
    overflowY: "scroll",
    padding: "10px",
    borderBottom: "1px solid #ccc",
  },
  userMessage: {
    textAlign: "right",
    margin: "5px 0",
    padding: "10px",
    background: "#DCF8C6",
    borderRadius: "10px",
  },
  errorMessage: {
    textAlign: "right",
    margin: "5px 0",
    padding: "10px",
    background: "#f4cccc",
    borderRadius: "10px",
  },
  botMessage: {
    textAlign: "left",
    margin: "5px 0",
    padding: "10px",
    background: "#E8E8E8",
    borderRadius: "10px",
  },
  inputContainer: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px 0",
  },
  input: {
    flex: "1",
    padding: "10px",
    fontSize: "16px",
    borderRadius: "4px",
    border: "1px solid #ccc",
    marginRight: "10px",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    borderRadius: "4px",
    border: "none",
    background: "#4CAF50",
    color: "white",
    cursor: "pointer",
  },
};

function generateUniqueName() {
  return Math.random().toString(36).substr(2, 9);
}

const Kiosk = () => {
  const [messages, setMessages] = useState([]);
  const [errorMessages, setErrorMessages] = useState([]);
  const [input, setInput] = useState("");
  const [prevInput, setPrevInput] = useState("");
  const [eroor, setError] = useState(false);
  const [botLoading, setBotLoading] = useState(false);
  const {
    transcript,
    resetTranscript,
    listening,
    finalTranscript,
    interimTranscript,
  } = useSpeechRecognition();

  useEffect(() => {
    SpeechRecognition.startListening();
  }, []);

  useEffect(() => {
    async function send() {
      if (!listening && finalTranscript !== "") {
        console.log(finalTranscript);
        const userMessage = { sender: randName, text: finalTranscript };

        try {
          await setBotLoading(true);
          const response = await axios.post(
            "http://thing-won.com:5005/webhooks/rest/webhook",
            {
              sender: randName,
              message: transcript,
            }
          );
          console.log(response);

          const botMessage = { sender: "bot", text: response.data[0].text };
          await resetTranscript();

          await setBotLoading(false);
          await setMessages((prevMessages) => [
            ...prevMessages,
            userMessage,
            botMessage,
          ]);
          await setErrorMessages([]);
        } catch (error) {
          console.error("Error sending message:", error);

          // await setMessages(async (prevMessages) => {
          //   await prevMessages.pop();
          //   return prevMessages;
          // });
          await setErrorMessages([userMessage]);

          await setBotLoading(false);
        } finally {
          SpeechRecognition.startListening();

          console.log(messages);
          console.log(errorMessages);
        }
      } else if (!listening) {
        SpeechRecognition.startListening();
      }
    }

    send();
  }, [listening]);

  const randName = generateUniqueName();

  return (
    <>
      <div style={styles.chatContainer}>
        <div style={styles.messageContainer}>
          {Array.from(messages).map((msg, index) => (
            <div
              key={index}
              style={
                msg.sender !== "bot" ? styles.userMessage : styles.botMessage
              }
            >
              {msg.text}
            </div>
          ))}
          {Array.from(errorMessages).map((msg, index) => (
            <div key={index} style={styles.errorMessage}>
              {msg.text}
            </div>
          ))}

          {botLoading && (
            <div key={1000000} style={styles.botMessage}>
              ...
            </div>
          )}
        </div>
        <div style={styles.inputContainer}>
          <input
            type="text"
            value={transcript}
            style={styles.input}
            placeholder="Listening..."
          />
        </div>
      </div>
    </>
  );
};
export default Kiosk;
