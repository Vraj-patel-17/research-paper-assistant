import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";

function PaperDetails() {
  const { paperId } = useParams();

  const [paper, setPaper] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/papers/${paperId}`)
      .then((data) => {
        setPaper(data);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [paperId]);

  if (loading) {
    return <h1>Loading paper...</h1>;
  }

  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
      <h1>{paper.title}</h1>
      <p>{paper.authors}</p>
      <p>{paper.publication_date}</p>
      <p>{paper.source}</p>
    </div>
  );
}

export default PaperDetails;