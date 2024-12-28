import { useState, useEffect } from "react";
import ChatBot from "react-chatbotify";
import axios from "axios";

const MyComponent = () => {
  const [threadId, setThreadId] = useState("");
  const [customerName, setCustomerName] = useState("");
  const [hasError, setHasError] = useState(false); // Updated to use React state for error management

  useEffect(() => {
    // Generate a new thread_id only on page refresh
    const newThreadId = crypto.randomUUID();
    setThreadId(newThreadId);
    console.log("Generated thread_id:", newThreadId);
  }, []); // Empty dependency array ensures this runs only on initial mount

  const call_openai = async (params) => {
    try {
      const response = await axios.post("http://localhost:5000/api/chat", {
        message: params.userInput.trim(),
        thread_id: threadId,
        customer_name: customerName,
        responseType: "stream",
      });
      const stream = response.data;

      let text = "";
      for await (const chunk of stream) {
        text += chunk;
        await params.streamMessage(text);
        await new Promise((resolve) => setTimeout(resolve, 15)); // Optional delay for streaming
      }

      // Call endStreamMessage to indicate that all streaming has ended
      await params.endStreamMessage();
    } catch (error) {
      setHasError(true); // Update state to reflect error
      await params.injectMessage("Unable to load model, is your API Key valid?");
    }
  };

  const flow = {
    start: {
      message: "Hello! 👋 Welcome to Pizza Innovation Customer Support. Could you tell me your name?",
      path: "name",
    },
    name: {
      message: (params) => {
        const username = params.userInput.trim();
        setCustomerName(username);
        return `Hi ${username},\n\nI'm here to assist you with your queries and provide you with the best possible help. ` +
               "Whether it's about our menu, placing an order, or checking your past orders, feel free to ask.\n\nHow can I help you today? 🍕";
      },
      path: "loop",
    },
    loop: {
      message: async (params) => {
        await call_openai(params);
      },
      path: () => "loop",
    },
  };

  const settings = {
    chatHistory: {
      storageKey: threadId,
    },
    header: {
      title: "Customer Support",
    },
    footer: {
      text: "",
    },
    general: { embedded: true },
    botBubble: {
      simStream: true,
    },
  };

  return <ChatBot settings={settings} flow={flow} />;
};

export default MyComponent;
