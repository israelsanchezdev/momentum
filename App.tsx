// src/App.tsx
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TooltipProvider } from "@/components/ui/tooltip";
import AnimatedProgressItem from './AnimatedProgressItem';

// Define interfaces directly in App.tsx or a new types file if preferred
export interface DashboardItem {
  name: string;
  percentage: number;
}

export interface DashboardCategory {
  title: string;
  items: DashboardItem[];
}

const App: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardCategory[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // data.json is placed in the public folder, so it's served at the root
        const response = await fetch('/data.json');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setDashboardData(data);
      } catch (e) {
        if (e instanceof Error) {
          setError(e.message);
        } else {
          setError('An unknown error occurred');
        }
        console.error("Failed to fetch dashboard data:", e);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 text-white text-2xl">Loading Dashboard Data...</div>;
  }

  if (error) {
    return <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-900 to-red-800 text-white text-2xl">Error loading data: {error}. Please check if data.json is correctly placed in the public folder and is valid JSON.</div>;
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-4 sm:p-6 md:p-8 text-white">
        <header className="mb-8 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
            Interactive Initiatives Dashboard
          </h1>
          <p className="mt-2 text-lg text-slate-300">Visualizing Progress Across Key Areas (Data from JSON)</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {dashboardData.map((category: DashboardCategory, categoryIndex: number) => (
            <Card 
              key={categoryIndex} 
              className="bg-slate-800 border-slate-700 shadow-xl hover:shadow-2xl transition-shadow duration-300 transform hover:-translate-y-1"
            >
              <CardHeader className="pb-4">
                <CardTitle className="text-xl font-semibold text-sky-400">{category.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {category.items.map((item, itemIndex) => (
                    <AnimatedProgressItem key={itemIndex} item={item} index={itemIndex} />
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>
        <footer className="mt-12 text-center text-slate-400 text-sm">
          <p>Powered by Manus AI | Data as of May 13, 2025 (Editable via data.json)</p>
        </footer>
      </div>
    </TooltipProvider>
  );
};

export default App;

