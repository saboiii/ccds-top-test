import { MongoClient } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI);

async function handler(req, res) {
  if (req.method === "GET") {
    await client.connect();
    const db = client.db("telegram_bot");
    const messagesCollection = db.collection("messages");
    const messages = await messagesCollection.find({}).toArray()
    await client.close();
    res.status(200).json(messages);
  } else {
    res.status(405).json({ error: "not allowed" });
  }
}

export default handler;
