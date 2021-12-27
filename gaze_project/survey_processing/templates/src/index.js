import React from 'react';
import ReactDOM from 'react-dom';
import { Home } from 'pages';
import 'fonts/NotoSansKR/NotoSansKR-Hestia.css';
import 'index.scss';

class Application extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      page: '/'
    };
  }

  render() {
    return (
      <>
        <main className="content">
          <Home />
        </main>
      </>
    );
  }
}

ReactDOM.render(<Application />, document.getElementById('app'));
