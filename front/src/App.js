import Dictaphone from "./component/Dictaphone";
import Speecher from "./component/Speecher";
import Chat from "./component/Chat";

import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

function App() {
  return (
    <div style={{ position: "relative", height: "500px" }}>
      {/* <Dictaphone /> */}
      <Chat />
    </div>
  );
}

export default App;
