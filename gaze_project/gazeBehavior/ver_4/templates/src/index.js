import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom';
import { Home, Data, SpatialVariance, Analysis, Visualization } from 'pages';
import { Menu, Aside } from 'components';
import 'fonts/NotoSansKR/NotoSansKR-Hestia.css';
import 'index.scss';

class Application extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      page: '/'
    };
  }

  onMenuClick = (page) => {
    this.setState({ page });
  }

  render() {
    const { page } = this.state;

    return (
      <>
        <nav className="menu">
          <Menu page={page} onClick={this.onMenuClick} />
        </nav>
        <main className="content">
          {page == '/' &&
            <Home />
          }
          {page == '/data' &&
            <Data />
          }
          {page == '/spatial-variance' &&
            <SpatialVariance />
          }
          {page == '/analysis' &&
            <Analysis />
          }
          {page == '/visualization' &&
            <Visualization />
          }
          {/*<BrowserRouter>
            <Route exact path="/" component={Home} />
            <Route path="/data" render={() => <Data />} />
            <Route path="/spatial-variance" component={SpatialVariance} />
            <Route path="/analysis" render={() => <Analysis />} />
            <Route path="/visualization" component={Visualization} />
          </BrowserRouter>*/}
        </main>
        <aside className="aside">
          <Aside />
        </aside>
        <footer className="footer">
          {/*<Footer />*/}
        </footer>
      </>
    );
  }
}

ReactDOM.render(<Application />, document.getElementById('app'));
