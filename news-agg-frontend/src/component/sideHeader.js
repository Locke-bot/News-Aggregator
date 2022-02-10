import React, { Component } from 'react';

export default class SideHeader extends Component{
    render(){
        return (<header className="sidenav" id="sidenav">
            
                <div className="sidenav__close">
                  <button className="sidenav__close-button" id="sidenav__close-button" aria-label="close sidenav">
                    <i className="ui-close sidenav__close-icon"></i>
                  </button>
                </div>
                
                <nav className="sidenav__menu-container">
                  <ul className="sidenav__menu" role="menubar">

                    <li>
                      <a href="#" className="sidenav__menu-url">Pages</a>
                      <button className="sidenav__menu-toggle" aria-haspopup="true" aria-label="Open dropdown"><i className="ui-arrow-down"></i></button>
                      <ul className="sidenav__menu-dropdown">
                        <li><a href="about.html" className="sidenav__menu-url">About</a></li>
                        <li><a href="contact.html" className="sidenav__menu-url">Contact</a></li>
                        <li><a href="search-results.html" className="sidenav__menu-url">Search Results</a></li>
                        <li><a href="categories.html" className="sidenav__menu-url">Categories</a></li>
                        <li><a href="404.html" className="sidenav__menu-url">404</a></li>
                      </ul>
                    </li>
                  </ul>
                </nav>

              </header>)
    }
}