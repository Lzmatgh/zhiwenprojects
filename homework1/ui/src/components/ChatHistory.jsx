import React , { useState } from "react";

const ChatHistory = ({ history }) => {
  // TODO: make the history clickable, and can resume history chat
  const [currentInput, setCurrentInput] = useState("");
  
    const handleItemClick = (item) => {
      setCurrentInput(item.input);
    };
  return (
    <ul className="history-list">
      {history.map((item, index) => (
        <li key={index} onClick={() => handleItemClick(item)}>
          <div className="history-item">
            <div className="history-input">{item.input}</div>
            <div className="history-output">{item.output}</div>
          </div>
        </li>
      ))}
    {currentInput && (
            <li>
              <div className="history-item">
                <div className="history-input">{currentInput}</div>
              </div>
            </li>
          )}
        </ul>
      );
    };

export default ChatHistory;