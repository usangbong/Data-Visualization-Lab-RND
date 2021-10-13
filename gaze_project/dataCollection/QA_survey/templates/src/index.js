import React from 'react';
import ReactDOM from 'react-dom';
// import { Data } from 'pages';
// import { Analysis } from 'pages';
import { Home } from 'pages';
import { Footer } from 'components';
import 'fonts/NotoSansKR/NotoSansKR-Hestia.css';
import 'index.scss';

class Application extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      page: '/'
    };
  }

  // onMenuClick = (page) => {
  //   this.setState({ page });
  // }

  render() {
    const { page } = this.state;

    return (
      <>
        <main className="content">
          <Home />
        </main>
        <footer className="footer">
          <Footer />
        </footer>
      </>
    );
  }
}

ReactDOM.render(<Application />, document.getElementById('app'));
