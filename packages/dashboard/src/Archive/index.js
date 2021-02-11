import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Header from "./Header";
import Message from "./Message";

export default function Archive() {
  const { id } = useParams();
  const [data, setData] = useState();

  useEffect(() => {
    if (!/^\d{15,21}$/u.exec(id)) {
      setData({ error: "Invalid archive ID specified." });
      return;
    }

    async function fetchData() {
      let resp;

      try {
        resp = await fetch(`https://api.mousey.app/v4/archives/${id}`);
      } catch {
        setData({ error: "Failed to fetch archive data." });
        return;
      }

      const data = await resp.json();

      if (!resp.ok) {
        setData({ error: data.error });
      } else {
        data.sort((a, b) => (a.id > b.id ? 1 : -1));
        setData(data);
      }
    }
    fetchData();
  }, [id]);

  if (!data) {
    return <div className="status">Loading archive ...</div>;
  } else if (data.error) {
    return <div className="status error">{data.error}</div>;
  }

  return (
    <>
      <Header id={id} />
      <div className="messages">
        {data.map((message) => (
          <Message data={message} key={message.id} />
        ))}
      </div>
    </>
  );
}
