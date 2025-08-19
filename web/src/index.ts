import './styles.css';
import { App } from './app';

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const appElement = document.getElementById('app');
  if (appElement) {
    new App(appElement);
  } else {
    console.error('App container not found');
  }
});
