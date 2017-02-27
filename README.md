Safe Blog
=====================

Multi-user blogging platform for authorized users only.

Users register/sign in to have the ability to create/edits posts, give feedback and comment on other users's posts. All blog posts are public and can be viewed from the project's home page, but users's cannot interact with the posts until they've signed in.

This project delivers a simple and responsive user interface supported by [Bootstrap](http://getbootstrap.com/), and it is configured for deployment on Google App Engine. It makes use of the [wepapp2 framework](http://webapp2.readthedocs.io/en/latest/), the template library [Jinja2](http://jinja.pocoo.org/docs/2.9/) and [Google Cloud Datastore](https://cloud.google.com/appengine/docs/standard/python/datastore/) for storing and managing data. It supports **Python v2.7.10** and **Google Cloud SDK v143.0.1**.


## Setup

To run this project you will first need to [download and install the Google Cloud SDK](https://cloud.google.com/appengine/docs/standard/python/download).

Then, you may follow these 3 simple steps to get this project set up and running locally:

1. Clone the repository
```
$ git clone https://github.com/quiaro/safe-blog
```

2. Go to the project directory
```
$ cd safe-blog
```

3. Launch the [local development server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)
```
$ dev_appserver.py .
```

This project uses the CSS language extension Sass, which makes it easier to change the look of the app during development. If you wish to make changes to any of the stylesheets and see the changes applied with every browser refresh, you will need to follow 2 additional steps:

4. Install gulp, gulp-autoprefixer and gulp-sass
```
$ npm install
```

5. Ask gulp to watch for changes to any of the .scss files. On change, [gulp](http://gulpjs.com/) will update the project's stylesheet (`app/static/css/main.css`) and the changes will be reflected when the browser is refreshed (assuming that the local development server from step 3 is up and running).
```
$ gulp
```

---

## License

This project is licensed under the terms of the [**MIT**](https://opensource.org/licenses/MIT) license.
