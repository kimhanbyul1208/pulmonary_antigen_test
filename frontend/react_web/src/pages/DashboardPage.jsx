/**
 * Dashboard Page for medical staff.
 * Main overview of patients, appointments, and AI predictions.
 */
import { useAuth } from '../auth/AuthContext';

const DashboardPage = () => {
  const { user, logout } = useAuth();

  return (
    <div style={{ padding: '2rem' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <h1>NeuroNova 대시보드</h1>
        <div>
          <span style={{ marginRight: '1rem' }}>환영합니다, {user?.username}님</span>
          <button onClick={logout}>로그아웃</button>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>오늘의 예약</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>12</p>
        </div>

        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>대기 중인 진단</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>5</p>
        </div>

        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>AI 분석 완료</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>8</p>
        </div>

        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <h3>총 환자 수</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>245</p>
        </div>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h2>최근 AI 진단 결과</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ccc' }}>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>환자명</th>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>진단 유형</th>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>신뢰도</th>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>상태</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '0.75rem' }}>홍길동</td>
              <td style={{ padding: '0.75rem' }}>Meningioma</td>
              <td style={{ padding: '0.75rem' }}>94%</td>
              <td style={{ padding: '0.75rem' }}>검토 대기</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DashboardPage;
