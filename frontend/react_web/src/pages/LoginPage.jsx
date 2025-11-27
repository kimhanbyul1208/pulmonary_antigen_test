/**
 * Login Page for NeuroNova Medical Staff.
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ maxWidth: '400px', width: '100%', padding: '2rem' }}>
        <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>NeuroNova</h1>
        <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>의료진 로그인</h2>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label>
              사용자명
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label>
              비밀번호
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem' }}
              />
            </label>
          </div>

          {error && (
            <div style={{ color: 'red', marginBottom: '1rem' }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{ width: '100%', padding: '0.75rem', cursor: 'pointer' }}
          >
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
