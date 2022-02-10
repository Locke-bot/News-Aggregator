import logo from './logo.svg';
import React, { Component } from 'react';

import SideHeader from './component/sideHeader';
import NavHeader from './component/header';
import NewsLetter from './component/newsletter';

import 'jquery/src/jquery';

import './css/bootstrap.min.css';
import './css/font-icons.css';
import './css/style.css';

import axios from 'axios';

const API = "http://127.0.0.1:8000/";
const noFromEach = 6;
const Newsletter = <NewsLetter />
                   
class App extends Component {

    constructor(props){
        super(props);
        let posts;
        this.state = {
            posts
        };
    }
    
    addPosts(){
        console.log(this.state.posts)
        if (this.state.posts == null){
            console.log("shit is null")
            return <p>Data Incoming!</p>
        }
        
        // the same number of articles must be taken from all newspapers
        // the Math.round is to take care of any floating point issues
        return [...Array(Math.round(this.state.posts.length-1)/noFromEach).keys()].map(
            item=>(
                <div className="row">
                    <div className="col-lg-8 blog__content">
                        <section className="section tab-post mb-16">
                            <div className="title-wrap title-wrap--line">
                                <h3 className="section-title">{this.state.posts.slice(1)[item*noFromEach].name}</h3>
                            </div>
                            <div className="tabs__content tabs__content-trigger tab-post__tabs-content">
                                <div className="tabs__content-pane tabs__content-pane--active" id="tab-all">
                                    <div className="row card-row">
                                        {console.log("WatchTower", this.state.posts.slice(1).slice(item*noFromEach, noFromEach*(item+1)))}
                                        {this.display(this.state.posts.slice(1).slice(item*noFromEach, noFromEach*(item+1)))}
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                    { (noFromEach*item==0) && Newsletter }
                </div>
            )
        )
    }
    
    display(posts){
        console.log(posts)
        if (posts == null){
            return <p>Data Outcoming!</p>
        }
        return posts.map(function(item){
            return (<div className="col-md-6">
                        <article className="entry card">
                          <div className="entry__img-holder card__img-holder">
                            <a href={item.url}>
                              <div className="thumb-container thumb-70">
                                <img data-src={item.post_thumbnail} src={item.post_thumbnail} className="entry__img lazyloaded" alt=""/>
                              </div>
                            </a>
  
                          </div>
                    
                          <div className="entry__body card__body">
                            <div className="entry__header">
                              
                              <h2 className="entry__title">
                                <a href="single-post.html">{item.title}</a>
                              </h2>
                              <ul className="entry__meta">
                                <li className="entry__meta-author">
                                  <span>by</span>&nbsp;
                                  <a href="#">{item.name}</a>
                                </li>
                                <li className="entry__meta-date">
                                  {item.created_at}
                                </li>
                              </ul>
                            </div>
                            <div className="entry__excerpt" dangerouslySetInnerHTML={{__html: item.excerpt}}>
                            </div>
                          </div>
                        </article>
                </div>)
        })
    }

    
    displayLatest(posts){
        if (this.state.posts == null){
            return <p>Data Incoming!</p>
        }
        this.latest = this.state.posts[0]
        return(
            <article className="entry card featured-posts-grid__entry">
               <div className="entry__img-holder card__img-holder">
                  <a href={this.latest.url}>
                    <img src={this.latest.post_thumbnail} alt="" className="entry__img"/>
                  </a>
                </div>
    
                <div className="entry__body card__body">   
                  <h2 className="entry__title">
                    <a href={this.latest.url}>{this.latest.title}</a>
                  </h2>
                  <ul className="entry__meta">
                    <li className="entry__meta-author">
                      <span>by</span>&nbsp;
                      <a href={this.latest.url}>{this.latest.name}</a>
                    </li>
                    <li className="entry__meta-date">
                      {this.created_at}
                    </li>
                  </ul>
              </div>
             </article>
        )}
    
    
    componentWillMount(){
        console.log("will mount")
        let link = document.createElement('link');
        link.rel = "stylesheet"
        link.href = process.env.PUBLIC_URL + "css/style.css";
        document.head.appendChild(link);
        
        let fontLink = document.createElement('link');
        fontLink.rel = "stylesheet"
        fontLink.href = "https://fonts.googleapis.com/css?family=Montserrat:400,600,700%7CSource+Sans+Pro:400,600,700";
        document.head.appendChild(fontLink);
                
        // appendScript can't be used since lazysizes must be in the head tag
        const script = document.createElement("script");
        script.src = process.env.PUBLIC_URL + "js/lazysizes.min.js";
        document.head.appendChild(script);
        
    }

    appendScript = (scriptToAppend) => {
        const script = document.createElement("script");
        script.src = scriptToAppend;
        document.body.appendChild(script);
    }    
    
    componentDidMount(){
        console.log("mounted")
        axios.get(API + "api/" + noFromEach)
          .then(result => this.setState({
                posts: result.data,
          }))
        
        this.appendScript("https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js")
        this.appendScript("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/easing.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/owl-carousel.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/flickity.pkgd.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/twitterFetcher_min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/jquery.newsTicker.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/modernizr.min.js")
        this.appendScript(process.env.PUBLIC_URL + "js/scripts.js")
        
    }
    
    render() {
        return (
        <body className="bg-light style-default style-rounded">
            <div className="loader-mask" style={{"display": "none"}}>
                <div className="loader" style={{"display": "none"}}>
                  <div></div>
                </div>
            </div>
            <div className="content-overlay"></div>
            <SideHeader />
            <main className="main oh" id="main">
                <NavHeader />
                <section className="featured-posts-grid">
                      <div className="container">
                        <div className="row row-8">                
                          <div>
                            <div className="featured-posts-grid__item featured-posts-grid__item--lg">
                                {this.displayLatest()}
                            </div>
                          </div>          
                
                        </div>
                      </div>
                    </section>
                <div className="main-container container pt-24" id="main-container">
                    {this.addPosts()}
                </div>
            </main>
        </body>
        );
    }
}
export default App;