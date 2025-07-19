import { Card, CardContent } from "./card";
import { useEffect, useState } from "react";
import { BadgeCheck} from "lucide-react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import axios from 'axios';
const data = [
  { name: 'Declined', value: 3 },
  { name: 'Interview', value: 2 },
  { name: 'No response', value: 5 },
];
import Header from "./HeaderBar_Job_Seeker";
const COLORS = ["#D88288", "#81A67C", "#9FAAAB"];

type Skill = {
  name: string;
};

type JobSeekerProfileData = {
  first_name: string;
  email: string;
  skills: Skill[];
};

const JobSeekerHome = () => {

  const [profile, setProfile] = useState<JobSeekerProfileData | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get<JobSeekerProfileData>('/api/jobseeker/profile/', {
          withCredentials: true, // Ensure cookies (auth) are sent
          headers: {
            'Content-Type': 'application/json',
          },
        });
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  return (
    <div>
      <Header />
      <div className="page">
        <div>{profile?.email}</div>
        <h2 className="title">Hi {profile?.first_name}! Here’s a quick look at your journey</h2>

        <div className="flex flex-col items-center gap-8 px-4">
          {/* Chart Card */}
          <Card className="w-full max-w-3xl shadow-lg card">
            <CardContent className="card-body">
              <h3 className="section-title text-xl mb-4 text-center">An Overview of Applied Jobs</h3>
              <div className="flex justify-center"> {/* This flex container centers the ResponsiveContainer */}
                <ResponsiveContainer width="100%" height={320}>
                  {/* Remove the unnecessary div around PieChart and its flex properties */}
                  <PieChart width={400} height={300}>
                    <Pie
                      data={data}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label={({ name }) => name}
                    >
                      {data.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
          <hr></hr>
          {/* Skills Card */}
          <Card className="w-full max-w-3xl shadow-lg card">
            <CardContent>
              <div className="skills-header mb-4 card-body">
                <h3 className="section-title text-xl text-center">Skills</h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {profile?.skills.map((skill) => (
                  <div
                    key={skill.name}
                    className="flex items-center gap-3 p-4 bg-gray-100 rounded-lg shadow-sm"
                  >
                    <BadgeCheck className="text-green-500 w-6 h-6" />
                    <span className="text-lg font-medium">{skill.name}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

        </div>
      </div>
    </div>
  );
};

export default JobSeekerHome;
