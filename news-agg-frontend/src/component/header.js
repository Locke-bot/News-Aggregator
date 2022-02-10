import React, { Component } from 'react';

export default class Header extends Component{
    render(){
        return (<header className="nav">
                  <div className="nav__holder nav--sticky sticky offset scrolling">
                    <div className="container relative">
                      <div className="flex-parent">
            
                        <button className="nav-icon-toggle" id="nav-icon-toggle" aria-label="Open side menu">
                          <span className="nav-icon-toggle__box">
                            <span className="nav-icon-toggle__inner"></span>
                          </span>
                        </button> 
            
                        <a href="index.html" className="logo">
                          <img className="logo__img" src="img/logo_default.png" srcSet="img/logo_default.png 1x, img/logo_default@2x.png 2x" alt="logo"/>
                        </a>
            
                        <nav className="flex-child nav__wrap d-none d-lg-block">              
                          <ul className="nav__menu">
                            <li className="nav__dropdown">
                              <a href="#">Pages</a>
                              <ul className="nav__dropdown-menu">
                                <li><a href="about.html">About</a></li>
                                <li><a href="contact.html">Contact</a></li>
                                <li><a href="search-results.html">Search Results</a></li>
                                <li><a href="categories.html">Categories</a></li>
                                <li><a href="404.html">404</a></li>
                              </ul>
                            </li>                
                          </ul>
                        </nav>
                      </div>
                    </div>
                  </div>
                </header>)
    }
}