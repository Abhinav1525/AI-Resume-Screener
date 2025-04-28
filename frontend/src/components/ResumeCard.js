import "../styles/ResumeCard.css";

const ResumeCard = ({ resume }) => {
  return (
    <div className="resume-card">
      <h3>{resume.name}</h3>
      <p>Skills: {resume.skills.join(", ")}</p>
      <p>ATS Score: {resume.ats_score}%</p>
    </div>
  );
};

export default ResumeCard;
