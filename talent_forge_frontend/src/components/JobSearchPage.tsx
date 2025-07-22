import React, { useState } from 'react';
import Header from "./HeaderBar_Job_Seeker";

type Job = {
  id: number;
  employer_name: string;
  job_title: string;
  description: string;
  location: string;
  work_mode: string;
  has_applied: boolean;
};

const JobSearchPage = () => {
  const [query, setQuery] = useState('');
  const [jobType, setJobType] = useState('');
  const [skills, setSkills] = useState('');
  const [results, setResults] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResults([]);
    try {
      const res = await fetch(`/api/jobs_search/?name=${encodeURIComponent(query)}&job_type=${encodeURIComponent(jobType)}&skills=${encodeURIComponent(skills)}`);
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
      // Optionally, set an error message state here
    } finally {
      setIsLoading(false);
    }
  };

  function getCookie(name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const handleApply = async (jobId: number) => {
    try {
      const res = await fetch(`/api/apply_job/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || '', // Django CSRF token
        },
        body: JSON.stringify({ job_id: jobId }),
      });

      if (res.ok) {
        window.location.href = '/my_applications/';
      } else {
        const data = await res.json();
        alert(`Error applying: ${data.detail || 'Something went wrong.'}`);
      }
    } catch (error) {
      console.error('Application error:', error);
      alert('Failed to apply. Please try again.');
    }
  };

  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const handleKnowMore = (job: Job) => {
    console.log("Selected Job:", job);
    setSelectedJob(job);
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
            disabled={isLoading}
          />

          <input
            type="text"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            placeholder="Job type (e.g. full-time, part-time)"
            className="border p-2 rounded w-full"
            disabled={isLoading}
          />

          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Skills (comma-separated)"
            className="border p-2 rounded w-full"
            disabled={isLoading}
          />

          <button
            type="submit"
            className="btn btn-primary text-white px-4 py-2 rounded flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                {/* Bootstrap Spinner */}
                <div className="spinner-border spinner-border-sm text-white" role="status"></div>
                <span className="ml-2">Searching...</span>
              </>
            ) : (
              'Search'
            )}
          </button>
        </form>

        {isLoading && (
          <p className="mt-4 text-center text-blue-600 font-semibold flex items-center justify-center">
            {/* Bootstrap Spinner for loading message */}
            <div className="spinner-border spinner-border-sm text-blue-600 mr-2" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </p>
        )}

        {!isLoading && results.length > 0 ? (
          <ul className="list-unstyled space-y-4 mt-6">
            {results.map((job) => (
              
              <li key={job.id} className="border p-4 rounded shadow">
                <h3 className="text-lg font-bold">{job.job_title}</h3>
                <p>{job.employer_name} — {job.location}</p>
                <div className="mt-3">
                  {job.has_applied ? (
                      <button className="btn btn-success btn-sm me-2 rounded" disabled>Already Applied</button>
                    ) : (
                      <button className="btn btn-success btn-sm me-2 rounded" onClick={() => handleApply(job.id)}>Apply</button>
                    )}
                  <button
                    onClick={() => handleKnowMore(job)}
                    className="btn btn-outline-secondary btn-sm rounded"
                  >
                    Know More
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (!isLoading && <p className="mt-4">No jobs found.</p>)}
      </div>

      {selectedJob && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent black overlay
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000, // Make sure it's on top
          }}
        >
          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '8px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              maxWidth: '500px',
              width: '90%', // Responsive width
            }}
          >
            <div className="bg-white p-6 rounded shadow-lg max-w-xl w-full">
              <h2 className="text-xl font-bold mb-2">{selectedJob.job_title}</h2>
              <p className="text-gray-700"><strong>Employer:</strong> {selectedJob.employer_name}</p>
              <p className="text-gray-700"><strong>Location:</strong> {selectedJob.location}</p>
              <p className="text-gray-700"><strong>Work mode:</strong> {selectedJob.work_mode}</p>
              <p className="mt-4">{selectedJob.description}</p>
              <button
                className="btn btn-secondary mt-4"
                onClick={() => setSelectedJob(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobSearchPage;