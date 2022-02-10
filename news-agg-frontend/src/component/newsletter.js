import React, { Component } from 'react';

export default class NewsLetter extends Component{
    render(){
        return <aside className="col-lg-4 sidebar sidebar--right">
                <aside className="widget widget_mc4wp_form_widget">
                  <h4 className="widget-title">Newsletter</h4>
                  <p className="newsletter__text">
                    <i className="ui-email newsletter__icon"></i>
                    Subscribe for our daily news
                  </p>
                  <form className="mc4wp-form" method="post">
                    <div className="mc4wp-form-fields">
                      <div className="form-group">
                        <input type="email" name="EMAIL" placeholder="Your email" required=""/>
                      </div>
                      <div className="form-group">
                        <input type="submit" className="btn btn-lg btn-color" value="Sign Up"/>
                      </div>
                    </div>
                  </form>
                </aside>
            </aside>;             
        }
}