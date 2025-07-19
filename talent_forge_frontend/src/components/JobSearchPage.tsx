import React, { useState } from 'react';
import Header from "./HeaderBar_Job_Seeker";

type Job = {
  id: number;
  employer_name: string;
  job_title: string;
  description: string;
  location: string;
  created_at: string;
};

const JobSearchPage = () => {
  const [query, setQuery] = useState('');
  const [jobType, setJobType] = useState('');
  const [skills, setSkills] = useState('');
  const [results, setResults] = useState<Job[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`/api/jobs_search/?name=${encodeURIComponent(query)}&job_type=${encodeURIComponent(jobType)}&skills=${encodeURIComponent(skills)}`);
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  return (
    <div>
      <Header />
      <div className="p-4">
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by job title..."
            className="border p-2 rounded w-full"
          />

          <input
            type="text"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            placeholder="Job type (e.g. full-time, part-time)"
            className="border p-2 rounded w-full"
          />

          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Skills (comma-separated)"
            className="border p-2 rounded w-full"
          />

          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
            Search
          </button>
        </form>

        {results.length > 0 ? (
          <ul className="space-y-4 mt-6">
            {results.map((job) => (
              <li key={job.id} className="border p-4 rounded shadow">
                <h3 className="text-lg font-bold">{job.job_title}</h3>
                <p>{job.employer_name} — {job.location}</p>
                <p className="text-sm text-gray-600">{job.description.slice(0, 100)}...</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-4">No jobs found.</p>
        )}
      </div>
    </div>
  );
};

export default JobSearchPage;
