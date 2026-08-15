import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Link } from "react-router-dom";
function Dashboard() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/papers")
      .then((data) => {
        console.log("FULL PAPERS RESPONSE:", data);
        setPapers(data.items);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <h1>Loading papers...</h1>;
  }

  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
      <h1>Research Papers</h1>

      {papers.map((paper) => (
        <div key={paper.id}>
          <h2><Link to={`/papers/${paper.id}`}>
              {paper.title}</Link></h2>
          <p>{paper.authors}</p>
          <p>{paper.publication_date}</p>
          <p>{paper.source}</p>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;