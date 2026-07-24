import { createRoot } from 'react-dom/client';
import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom';
import Game from './pages/Game';
import Dashboard from './pages/Dashboard';
import Rules from './pages/Rules';
import './style.css';

function App() {
  return (
    <BrowserRouter>
      <header>
        <NavLink to="/" className="brand">♞ Adaptive Chess <i>RL</i></NavLink>
        <nav>
          <NavLink to="/">Play</NavLink>
          <NavLink to="/dashboard">Learning</NavLink>
          <NavLink to="/rules">Rules</NavLink>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<Game />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/rules" element={<Rules />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = document.getElementById('root');
if (!root) throw new Error('Application root element was not found.');
createRoot(root).render(<App />);
