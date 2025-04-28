import React, { useState } from "react";
import api from "../api";

const UploadResume = () => {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resume || !jobDesc) return alert("Please provide resume and job description");

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_desc", jobDesc);

    try {
      const res = await api.post("/upload", formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto bg-white rounded-xl shadow-md">
      <h2 className="text-2xl font-bold mb-4">Upload Resume</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files[0])} className="mb-3" />
        <textarea
          placeholder="Paste job description..."
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          className="w-full h-32 p-2 border mb-3"
        />
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Submit</button>
      </form>

      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <p><strong>ATS Score:</strong> {result.ats_score}%</p>
          <p><strong>Skills Matched:</strong> {result.skills.join(", ")}</p>
        </div>
      )}
    </div>
  );
};

export default UploadResume;
