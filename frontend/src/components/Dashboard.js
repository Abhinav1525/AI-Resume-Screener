import React, { useEffect, useState } from "react";
import api from "../api";

const Dashboard = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await api.get("/resumes");
        setResumes(res.data);
      } catch (err) {
        console.error("Failed to fetch resumes", err);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Resume Dashboard</h2>
      {loading ? (
        <p>Loading resumes...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 text-left">Name</th>
                <th className="p-3 text-left">Skills</th>
                <th className="p-3 text-left">Similarity Score</th>
                <th className="p-3 text-left">ATS Score</th>
              </tr>
            </thead>
            <tbody>
              {resumes.map((resume, idx) => (
                <tr key={idx} className="border-t hover:bg-gray-50">
                  <td className="p-3">{resume.name}</td>
                  <td className="p-3">{resume.skills}</td>
                  <td className="p-3">{(resume.similarity_score * 100).toFixed(2)}%</td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-1 rounded text-white text-sm font-semibold ${
                        resume.ats_score > 60 ? "bg-green-500" : resume.ats_score > 30 ? "bg-yellow-500" : "bg-red-500"
                      }`}
                    >
                      {resume.ats_score.toFixed(2)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
