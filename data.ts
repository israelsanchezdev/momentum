// src/data.ts
export interface DashboardItem {
  name: string;
  percentage: number;
}

export interface DashboardCategory {
  title: string;
  items: DashboardItem[];
}

export const dashboardData: DashboardCategory[] = [
  {
    title: "Community & Placemaking Initiatives",
    items: [
      { name: "Topeka-Shawnee County Housing Strategies", percentage: 33 },
      { name: "Housing Advocacy Task Force", percentage: 20 },
      { name: "Downtown and NOTO Master Plan", percentage: 27 },
      { name: "21st Century Riverfront – RAC, GTP", percentage: 37 },
      { name: "Gateways and Corridors", percentage: 27 },
      { name: "Topeka Arts and Culture Master Plan", percentage: 35 },
      { name: "Active Recreation Initiatives", percentage: 40 },
    ],
  },
  {
    title: "Economic Development & Business Growth",
    items: [
      { name: "Existing Business Services", percentage: 35 },
      { name: "Career Connections Program", percentage: 27 },
      { name: "ASTRA Innovation Center and District", percentage: 30 },
      { name: "Entrepreneurial Ecosystem Building", percentage: 30 },
      { name: "Targeted Corporate Attraction", percentage: 35 },
      { name: "Developer Outreach and Engagement", percentage: 30 },
    ],
  },
  {
    title: "Talent Development & Workforce Support",
    items: [
      { name: "C2C Collaborative and Data Exchange", percentage: 12 },
      { name: "Washburn Now", percentage: 55 },
      { name: "Career Navigation", percentage: 27 },
      { name: "Child Care Task Force", percentage: 40 },
    ],
  },
  {
    title: "Community Identity & Engagement",
    items: [
      { name: "Diversity and Inclusion Strategy", percentage: 34 },
      { name: "“My Topeka” Campaign", percentage: 32 },
      { name: "Choose Topeka 2.0", percentage: 40 },
      { name: "Talent Immersion Efforts", percentage: 35 },
    ],
  },
];

