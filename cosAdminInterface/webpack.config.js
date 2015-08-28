var webpack = require('webpack');
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

var root = path.join(__dirname, 'adminInterface', 'static');
/** Return the absolute path given a path relative to ./website/static */
var staticPath = function(dir) {
    return path.join(root, dir);
};
var nodePath = function(dir) {
    return path.join(__dirname, 'node_modules', dir);
};

/**
 * Each JS module for a page on the OSF is webpack entry point. These are built
 * to adminInterface/static/public
 */
var entry = {
    // JS
    'prereg-admin-page': staticPath('js/pages/prereg-admin-page.js'),
    'app.min': staticPath('js/app.min.js'),
    'registration-edit-page': staticPath('js/pages/registration-edit-page.js'),
    'file-page': staticPath('js/pages/file-page.js'),
    // Commons chunk
    'vendor': [
        // Vendor libraries
        'knockout',
        'knockout.validation',
        'bootstrap',
        'URIjs',
        'bootbox',
        'mithril',
        'moment',
        'raven-js',
        'mithril'
    ]
};

var plugins = [
    // Bundle common code between modules
    new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.js'),
    // Bower support
    new webpack.ResolverPlugin(
        new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin('bower.json', ['main'])
    ),
    // Make jQuery available in all modules without having to do require('jquery')
    new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery'
    }),
    // Slight hack to make sure that CommonJS is always used
    new webpack.DefinePlugin({
        'define.amd': false
    }),
    // for using webpack with Django
    new BundleTracker({filename: './webpack-stats.json'}),
];


var output = {
    path: './adminInterface/static/public/js/',
    // publicPath: '/static/', // used to generate urls to e.g. images
    filename: '[name].js',
    sourcePrefix: ''
};

var resolve = {
    extensions: ['', '.es6.js', '.js', '.min.js'],
    root: root,
    // Look for required files in bower and npm directories
    modulesDirectories: ['./adminInterface/static/vendor/bower_components', 'node_modules'],
    // Need to alias libraries that aren't managed by bower or npm
};

module.exports = {
    context: __dirname,
    entry: entry,
    plugins: plugins,
    output: output,
    resolve: resolve,
    module: {
        loaders: [
            {test: /\.es6\.js$/, exclude: [/node_modules/, /bower_components/, /vendor/], loader: 'babel-loader'},
            {test: /\.css$/, loaders: ['style', 'css']},
            // url-loader uses DataUrls; files-loader emits files
            {test: /\.png$/, loader: 'url-loader?limit=100000&mimetype=image/ng'},
            {test: /\.gif$/, loader: 'url-loader?limit=10000&mimetype=image/gif'},
            {test: /\.jpg$/, loader: 'url-loader?limit=10000&mimetype=image/jpg'},
            {test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader?mimetype=application/font-woff'},
            {test: /\.svg/, loader: 'file-loader'},
            {test: /\.eot/, loader: 'file-loader'},
            {test: /\.ttf/, loader: 'file-loader'},
            //Dirty hack because mime-type's json file is "special"
            {test: /db.json/, loader: 'json-loader'},
        ]
    }

};
