import { useEffect, useState } from "react";

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMessages = async () => {
      const response = await fetch("/api/messages");
      console.log("API Response:", response);
      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      } else {
        console.error(`HTTP error! status: ${response.status}`);
      }
      setLoading(false);
    };
    fetchMessages();
  }, []);  

  return (
    <div className="flex flex-col gap-4 w-screen px-20 py-16">
      <h1>LET'S DISPLAY MESSAGES.</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="w-full grid grid-cols-1 gap-4">
          {messages.map((message) => (
            <div key={message._id}>
              <strong>{message.user_name}:</strong> {message.user_message} <br />
              <em>{new Date(message.timestamp).toLocaleString()}</em>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;