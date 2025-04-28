import React, { useEffect, useState } from "react";
import api from "../api";

const Admin = () => {
  const [resumes, setResumes] = useState([]);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await api.get("/resumes");
        setResumes(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchResumes();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Admin Panel</h2>
      <ul className="space-y-3">
        {resumes.map((r, index) => (
          <li key={index} className="p-4 bg-gray-100 rounded">
            <p><strong>Name:</strong> {r.name}</p>
            <p><strong>Skills:</strong> {r.skills}</p>
            <p><strong>Similarity:</strong> {r.similarity_score.toFixed(2)}</p>
            <p><strong>ATS Score:</strong> {r.ats_score}%</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Admin;
