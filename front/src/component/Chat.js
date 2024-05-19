import React, { useState } from "react";
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

const Chat = () => {
  const [messages, setMessages] = useState(new Set());
  const [errorMessages, setErrorMessages] = useState(new Set());
  const [input, setInput] = useState("");
  const [prevInput, setPrevInput] = useState("");
  const [eroor, setError] = useState(false);
  const [botLoading, setBotLoading] = useState(false);

  const { transcript, resetTranscript, listening } = useSpeechRecognition();

  const randName = generateUniqueName();

  const handleSend = async () => {
    if (transcript.trim() !== "") {
      setInput("");
      const userMessage = { sender: randName, text: transcript };
      await setMessages([...messages, userMessage]);

      try {
        setBotLoading(true);
        const response = await axios.post(
          "http://thing-won.com:5005/webhooks/rest/webhook",
          {
            sender: "shbae",
            message: transcript,
          }
        );
        console.log(response);

        const botMessage = { sender: "bot", text: response.data[0].text };
        resetTranscript();

        setBotLoading(false);
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setErrorMessages([]);
      } catch (error) {
        console.error("Error sending message:", error);

        await setMessages((prevMessages) => [
          ...prevMessages.splice(0, prevMessages.length - 1),
        ]);
        await setErrorMessages((prevMessages) => [userMessage]);

        setBotLoading(false);
        resetTranscript();
      }

      return;
    }
    if (input.trim() === "") return;
    const userMessage = { sender: randName, text: input };

    await setMessages([...messages, userMessage]);

    try {
      setBotLoading(true);
      const response = await axios.post(
        "http://thing-won.com:5005/webhooks/rest/webhook",
        {
          sender: "shbae",
          message: input,
        }
      );
      console.log(response);

      const botMessage = { sender: "bot", text: response.data[0].text };

      setBotLoading(false);
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      setErrorMessages([]);
    } catch (error) {
      console.error("Error sending message:", error);

      await setMessages((prevMessages) => [
        ...prevMessages.slice(0, prevMessages.length - 1),
      ]);

      await setErrorMessages((prevMessages) => [userMessage]);

      setBotLoading(false);
    }
    setInput("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter") {
      console.log("enter");
      handleSend();
    }
  };

  const startListening = () => {
    SpeechRecognition.startListening({
      continuous: true,
    });
  };

  const stopListening = () => {
    SpeechRecognition.stopListening();
    handleSend();
  };

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
          <button
            onMouseDown={startListening}
            onMouseUp={stopListening}
            style={styles.micButton}
          >
            🎤
          </button>
          {listening ? (
            <input
              type="text"
              value={transcript}
              style={styles.input}
              placeholder="Recording..."
            />
          ) : (
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyUp={(e) => {
                handleKey(e);
              }}
              style={styles.input}
              placeholder="Type a message..."
            />
          )}

          <button onClick={handleSend} style={styles.button}>
            Send
          </button>
        </div>
      </div>
    </>
  );
};
export default Chat;
