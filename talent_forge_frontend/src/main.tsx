import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import EmployerHome from './components/EmployerHome';
import JobSeekerHome from './components/JobSeekerHome';
import JobSeekerProfileForm from './components/JobSeekerProfileForm';
import JobSearchPage from './components/JobSearchPage';

const rootElement = document.getElementById('root');

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <BrowserRouter>
        <Routes>
          <Route path="/job_search_page/*" element={<JobSearchPage />} />
          <Route path="/employer_dashboard/*" element={<EmployerHome />} />
          <Route path="/job_seeker_dashboard/*" element={<JobSeekerHome />} />
          <Route path="/create_jobseeker_profile/*" element={<JobSeekerProfileForm />} />
          <Route path="/edit_jobseeker_profile/*" element={<JobSeekerProfileForm />} />
          <Route path="*" element={<div>404 - Not Found</div>} />
        </Routes>
      </BrowserRouter>
    </React.StrictMode>
  );
}