"use client";
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const General = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (inputValue.trim() !== "") {
      const newMessage = { role: "user", content: inputValue };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setInputValue("");

      try {
        const response = await axios.post(
          "https://gpt.aifagoon.com/api/v2/fagoongpt/",
          { messages: messages.concat(newMessage) }, // Updated key from "message" to "messages"
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        setMessages((prevMessages) => [
          ...prevMessages,
          { role: "assistant", content: response.data.message },
        ]);

        // Check for contract_id in the response and store it in session storage
        if (response.data.contract_id) {
          sessionStorage.setItem("contract_id", response.data.contract_id);
        } else {
          console.log("No contract_id in the response");
        }
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <header className="bg-blue-500 py-4 text-white text-center">
        <h1 className="text-lg font-bold">General Info</h1>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M3 6l3 6v9a2 2 0 002 2h8a2 2 0 002-2V12l3-6M9 12v7m6-7v7"
            />
          </svg>
          <a href="/" className="text-white">
            Home
          </a>
        </button>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M3 6l3 6v9a2 2 0 002 2h8a2 2 0 002-2V12l3-6M9 12v7m6-7v7"
            />
          </svg>
          <a href="/employee" className="text-white">
            Update Employee Info
          </a>
        </button>
      </header>

      <main className="flex-1 p-4 overflow-y-auto">
        <div className="flex flex-col space-y-2">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : ""}`}
            >
              {message.role === "user" && (
                <div className="px-4 py-2 rounded-lg shadow-md bg-black text-white ml-auto animate-slideInFromRight">
                  {message.content}
                </div>
              )}
              {message.role === "assistant" && (
                <div className="px-4 py-2 rounded-lg shadow-md bg-gray-200 text-black mr-auto animate-slideInFromLeft">
                  {message.content}
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </main>
      <footer className="bg-gray-100 py-4 px-4">
        <div className="flex items-center">
          <input
            type="text"
            placeholder="Type your message here..."
            className="flex-1 py-2 px-4 border border-gray-300 rounded-full focus:outline-none"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            style={{ color: "black" }}
          />
          <button
            className="ml-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full"
            onClick={sendMessage}
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
};

export default General;
