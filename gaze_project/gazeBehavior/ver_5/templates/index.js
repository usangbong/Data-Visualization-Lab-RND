import React from 'react';
import ReactDOM from 'react-dom';
import { Data } from 'pages';
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
        <nav className="menu">
          {/* <Menu page={page} onClick={this.onMenuClick} /> */}
        </nav>
        <main className="content">
          {/* {page == '/' &&
            <Home />
          } */}
          {/* {page == '/data' &&
            <Data />
          } */}
          {/* {page === '/' && */}
            <Data />
          {/* } */}
        </main>
        {/* <aside className="aside">
          <Aside />
        </aside> */}
        <footer className="footer">
          {/* <Footer /> */}
        </footer>
      </>
    );
  }
}

ReactDOM.render(<Application />, document.getElementById('app'));
