import React, { Component } from 'react';
import styles from './App.scss';

class App extends Component {
  render() {
    return (
      <div className={styles.App}>
        <header className={styles.App__header}>
          <h1 className={styles.App__title}>Welcome to React</h1>
        </header>
        <p className={styles.App__intro}>
          To get started, edit <code>src/App.js</code> and save to reload.<br/>
          yarn start -> 3000server: develop app<br/>(proxy: 3000 -> 8000)<br/>>yarn build -> 8000server: product
        </p>
      </div>
    );
  }
}

export default App;
