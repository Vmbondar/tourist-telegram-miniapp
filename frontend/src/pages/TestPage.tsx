import React, { useState } from 'react';
import { getCities, getAttractions } from '../services/api';

const TestPage: React.FC = () => {
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const addResult = (message: string) => {
    setResults((prev) => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testCities = async () => {
    setLoading(true);
    addResult('🔄 Тестируем Cities API...');
    try {
      const response = await getCities();
      addResult(`✅ Успех! Получено городов: ${response.data.total}`);
      addResult(`Данные: ${JSON.stringify(response.data.items)}`);
    } catch (error: any) {
      addResult(`❌ Ошибка: ${error.message}`);
      if (error.response) {
        addResult(`Статус: ${error.response.status}`);
        addResult(`Данные: ${JSON.stringify(error.response.data)}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const testAttractions = async () => {
    setLoading(true);
    addResult('🔄 Тестируем Attractions API...');
    try {
      const response = await getAttractions({ city_id: 1, page: 1, page_size: 5 });
      addResult(`✅ Успех! Получено достопримечательностей: ${response.data.items.length}`);
      response.data.items.forEach((item: any) => {
        addResult(`  - ${item.name}`);
      });
    } catch (error: any) {
      addResult(`❌ Ошибка: ${error.message}`);
      if (error.response) {
        addResult(`Статус: ${error.response.status}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const testDirect = async () => {
    setLoading(true);
    addResult('🔄 Прямой запрос к API...');
    try {
      const response = await fetch('https://acrobat-weights-grow-von.trycloudflare.com/health');
      const data = await response.json();
      addResult(`✅ Прямой запрос успешен: ${JSON.stringify(data)}`);
    } catch (error: any) {
      addResult(`❌ Прямой запрос failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>🔍 API Test Page</h1>

      <div style={{ marginBottom: '20px' }}>
        <p><strong>API URL:</strong> {process.env.REACT_APP_API_URL}</p>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <button onClick={testCities} disabled={loading} style={buttonStyle}>
          Test Cities
        </button>
        <button onClick={testAttractions} disabled={loading} style={buttonStyle}>
          Test Attractions
        </button>
        <button onClick={testDirect} disabled={loading} style={buttonStyle}>
          Test Direct
        </button>
        <button onClick={() => setResults([])} style={buttonStyle}>
          Clear
        </button>
      </div>

      {loading && <p>⏳ Загрузка...</p>}

      <div style={{
        backgroundColor: '#f5f5f5',
        padding: '10px',
        borderRadius: '5px',
        maxHeight: '500px',
        overflow: 'auto'
      }}>
        {results.length === 0 ? (
          <p>Нажмите кнопку для тестирования</p>
        ) : (
          results.map((result, index) => (
            <div key={index} style={{
              marginBottom: '5px',
              fontSize: '12px',
              fontFamily: 'monospace'
            }}>
              {result}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const buttonStyle: React.CSSProperties = {
  padding: '10px 15px',
  backgroundColor: '#3390ec',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer'
};

export default TestPage;
