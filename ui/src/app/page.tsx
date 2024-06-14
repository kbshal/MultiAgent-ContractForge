import React from 'react';

const Home = () => {
  return (
    <nav className="flex flex-wrap justify-between px-4 py-2">
      <button className="w-full sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg flex items-center mb-4 sm:mb-0 sm:mr-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M3 6l3 6v9a2 2 0 002 2h8a2 2 0 002-2V12l3-6M9 12v7m6-7v7"
          />
        </svg>
        <a href="/general" className="block sm:inline-block">General Info</a>
      </button>
      <button className="w-full sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M15 8a5 5 0 00-10 0v4a5 5 0 0010 0V8z"
          />
        </svg>
        <a href="/employee" className="block sm:inline-block">Update Employee Info</a>
      </button>
    </nav>
  );
};

export default Home;
