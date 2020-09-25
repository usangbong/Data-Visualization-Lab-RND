import React from 'react';

class MenuItem extends React.Component {
  render() {
    const { href, title, children } = this.props;
    const active = (window.location.pathname.split('/')[1] === href.split('/')[1]);
    const className = (active) ? "menu-button active" : "menu-button";

    return (
      <div className="menu-item">
        <a className={className} href={href} title={title}>{children}</a>
      </div>
    );
  }
}

export default MenuItem;
