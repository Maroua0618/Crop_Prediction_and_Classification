import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function AlgorithmComparison() {
  const [metricView, setMetricView] = useState('time');

  // Algorithm comparison data from your output
  const algorithmData = [
    { algorithm: 'Greedy', time_s: 1.360995, mem_mb: 1.142903 },
    { algorithm: 'A*', time_s: 1.323355, mem_mb: 1.156714 },
    { algorithm: 'Genetic', time_s: 26.647954, mem_mb: 0.136867 },
    { algorithm: 'CSP', time_s: 0.306543, mem_mb: 0.814701 }
  ];

  const chartData = algorithmData.map(item => ({
    algorithm: item.algorithm,
    value: metricView === 'time' ? item.time_s : item.mem_mb,
  }));

  return (
    <div className="w-full p-4 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-green-800">Algorithm Performance Comparison</h3>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded ${metricView === 'time' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setMetricView('time')}
          >
            Time (s)
          </button>
          <button 
            className={`px-3 py-1 rounded ${metricView === 'memory' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setMetricView('memory')}
          >
            Memory (MB)
          </button>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="algorithm" />
          <YAxis label={{ value: metricView === 'time' ? 'Time (seconds)' : 'Memory (MB)', angle: -90, position: 'insideLeft' }} />
          <Tooltip formatter={(value) => [value.toFixed(4), metricView === 'time' ? 'Time (s)' : 'Memory (MB)']} />
          <Legend verticalAlign="top" />
          <Bar 
            dataKey="value" 
            name={metricView === 'time' ? 'Execution Time' : 'Memory Usage'} 
            fill={metricView === 'time' ? '#388e3c' : '#0288d1'} 
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}