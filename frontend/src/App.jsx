import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

function App() {
  const [stats, setStats] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [cpuChart, setCpuChart] = useState(null);
  const [memoryChart, setMemoryChart] = useState(null);
  const [networkChart, setNetworkChart] = useState(null);

  useEffect(() => {
    // 初始化WebSocket连接
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setStats(newData);
      
      // 更新历史数据
      setHistoricalData(prev => {
        const updated = [...prev, newData];
        if (updated.length > 30) updated.shift(); // 保持最近30个数据点
        
        // 存储到localStorage
        localStorage.setItem('monitoringHistory', JSON.stringify(updated));
        
        return updated;
      });
    };

    // 从localStorage加载历史数据
    const savedHistory = localStorage.getItem('monitoringHistory');
    if (savedHistory) {
      setHistoricalData(JSON.parse(savedHistory));
    }

    return () => ws.close();
  }, []);

  useEffect(() => {
    // 初始化图表
    if (!cpuChart) {
      const chart = echarts.init(document.getElementById('cpuChart'));
      setCpuChart(chart);
    }
    if (!memoryChart) {
      const chart = echarts.init(document.getElementById('memoryChart'));
      setMemoryChart(chart);
    }
    if (!networkChart) {
      const chart = echarts.init(document.getElementById('networkChart'));
      setNetworkChart(chart);
    }

    // 更新图表数据
    if (historicalData.length > 0 && cpuChart && memoryChart && networkChart) {
      updateCharts();
    }
  }, [historicalData]);

  const updateCharts = () => {
    // CPU图表配置
    cpuChart.setOption({
      title: { text: 'CPU使用率' },
      xAxis: {
        type: 'category',
        data: historicalData.map(d => d.timestamp)
      },
      yAxis: { type: 'value', max: 100 },
      series: [{
        data: historicalData.map(d => d.cpu.percent),
        type: 'line',
        smooth: true
      }]
    });

    // 内存图表配置
    memoryChart.setOption({
      title: { text: '内存使用率' },
      xAxis: {
        type: 'category',
        data: historicalData.map(d => d.timestamp)
      },
      yAxis: { type: 'value', max: 100 },
      series: [{
        data: historicalData.map(d => d.memory.percent),
        type: 'line',
        smooth: true
      }]
    });

    // 网络图表配置
    networkChart.setOption({
      title: { text: '网络流量' },
      xAxis: {
        type: 'category',
        data: historicalData.map(d => d.timestamp)
      },
      yAxis: { type: 'value' },
      series: [
        {
          name: '发送',
          data: historicalData.map(d => d.network.bytes_sent),
          type: 'line',
          smooth: true
        },
        {
          name: '接收',
          data: historicalData.map(d => d.network.bytes_recv),
          type: 'line',
          smooth: true
        }
      ]
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">系统监控面板</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg shadow">
            <div id="cpuChart" style={{height: '300px'}} />
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow">
            <div id="memoryChart" style={{height: '300px'}} />
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow">
            <div id="networkChart" style={{height: '300px'}} />
          </div>
        </div>

        {stats && (
          <div className="mt-6 bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">实时数据</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="font-medium">CPU使用率</p>
                <p>{stats.cpu.percent}%</p>
              </div>
              <div>
                <p className="font-medium">内存使用率</p>
                <p>{stats.memory.percent}%</p>
              </div>
              <div>
                <p className="font-medium">网络流量</p>
                <p>发送: {(stats.network.bytes_sent / 1024 / 1024).toFixed(2)} MB</p>
                <p>接收: {(stats.network.bytes_recv / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
