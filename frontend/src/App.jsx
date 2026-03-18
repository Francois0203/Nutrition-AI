import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { useTheme } from './hooks/useTheme';
import {
  NavigationBar,
  Settings,
  PageTransition
} from './components';
import { Home, Predict, Models, About } from './pages';
import styles from './App.module.css';

function App() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  // Navigation configuration
  const navigationLinks = [
    { label: 'Home', to: '/', icon: 0 },
    { label: 'Predict', to: '/predict', icon: 1 },
    { label: 'Models', to: '/models', icon: 2 },
    { label: 'About', to: '/about', icon: 3 }
  ];

  const handleNavigate = (path) => {
    navigate(path);
  };

  // Get current active path
  const getActivePath = () => {
    if (location.pathname === '/' || location.pathname === '') return '/';
    return location.pathname;
  };

  return (
    <div className={styles.app} data-theme={theme}>
      {/* Navigation */}
      <NavigationBar
        links={navigationLinks}
        onNavigate={handleNavigate}
        activeTab={getActivePath()}
        burgerSize={50}
      />

      {/* Main Content */}
      <main className={styles.main}>
        <PageTransition>
          <Routes>
            <Route path="/" element={<Home onNavigate={handleNavigate} />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/models" element={<Models />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </PageTransition>
      </main>

      {/* Settings - Always visible in top right */}
      <Settings
        theme={theme}
        toggleTheme={toggleTheme}
      />

      {/* Footer */}
      <footer className={styles.footer}>
        <p className={styles.footerText}>
          Nutrition AI © {new Date().getFullYear()} - Powered by Machine Learning
        </p>
      </footer>
    </div>
  );
}

export default App;