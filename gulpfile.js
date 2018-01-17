/*!
 * gulpfile.js for Django
 */
const path = require('path');
const gulp = require('gulp');
// const imagemin = require('gulp-imagemin');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat-util');
const rename = require("gulp-rename");
const cleanCSS = require('gulp-clean-css');
const autoprefixer = require('gulp-autoprefixer');
const sourcemaps = require('gulp-sourcemaps');
const gutil = require('gulp-util');


/**
 |--------------------------------------------------------------------------
 | TABLE OF CONTENT
 |--------------------------------------------------------------------------
 |
 | 1. Constants - Anything variables/constants which are configurable are here.
 | 2. Registered Django apps - Define all the django app directories you want to be processed.
 | 3. Gulp tasks - The list of tasks we defined for our gulp.
 */



/**
  |--------------------------------------------------------------------------
  | 1. Constants
  |--------------------------------------------------------------------------
  */

let BUILD_DEST_PATH = 'static/build/';

// The options are here https://github.com/jakubpawlowicz/clean-css#compatibility-modes
const CLEAN_CSS_COMPATIBILITY = 'ie9';

let _apps = [];



/**
  |--------------------------------------------------------------------------
  | 2. Registered Django apps
  |--------------------------------------------------------------------------
  */

// Register your django apps here!
registerApp('apps/customer');
registerApp('apps/express');
registerApp('apps/member');
registerApp('apps/order');
registerApp('apps/product');
registerApp('apps/report');
registerApp('apps/schedule');
registerApp('apps/store');
registerApp('core/messageset');



/**
  |--------------------------------------------------------------------------
  | 3. Gulp tasks
  |--------------------------------------------------------------------------
  */

/**
 * Image optimization
 * Find the images and optimize it on spot.
 */
// const imagesSrc = getApps('images/**/*');
// gulp.task('images', () => {
//   gulp.src(imagesSrc)
//     .pipe(imagemin())
//     .pipe(gulp.dest(sourceAsDestination));
// });

/**
 * Minify JS
 * Mnimize all non-compressed js
 */
const scriptsSrc = getApps('!(*.min).js');
scriptsSrc.push('static/js/**/!(*.min).js');
scriptsSrc.push('static/django_js_reverse/js/!(*.min).js');
gulp.task('scripts:apps', () => {
  // Exclude .min file in this glob, to avoid double compress
  gulp.src(scriptsSrc)
    .pipe(uglify())
    .on('error', (err) => {
      gutil.log(gutil.colors.red('[Error]'), err.toString());
    })
    // .pipe(concat('apps_bundle.js'))
    // .pipe(gulp.dest(BUILD_DEST_PATH));
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(sourceAsDestination));
});
const coreScripts=[];
coreScripts.push('core/adminlte/static/plugins/jQuery/jQuery-2.1.4.min.js');
coreScripts.push('core/adminlte/static/plugins/bootstrap/js/bootstrap.min.js');
coreScripts.push('core/adminlte/static/plugins/underscore/underscore-min.js');
coreScripts.push('core/adminlte/static/plugins/underscore/underscore.string.min.js');
coreScripts.push('core/adminlte/static/adminlte/js/app.min.js');
coreScripts.push('core/adminlte/static/plugins/vue/dist/vue.min.js');
coreScripts.push('core/adminlte/static/plugins/jquery-chosen/chosen.jquery.min.js');
coreScripts.push('core/adminlte/static/plugins/sweetalert/dist/sweetalert.min.js');
coreScripts.push('core/adminlte/static/adminlte/js/config.js');
coreScripts.push('core/adminlte/static/adminlte/js/ajax.js');
coreScripts.push('static/django_js_reverse/js/reverse.js');
gulp.task('scripts:core', () => {
  // Exclude .min file in this glob, to avoid double compress
  gulp.src(coreScripts)
    .pipe(uglify())
    .on('error', (err) => {
      gutil.log(gutil.colors.red('[Error]'), err.toString());
    })
    .pipe(concat('core_bundle.js'))
    .pipe(gulp.dest(BUILD_DEST_PATH));
    // .pipe(rename({ suffix: '.min' }))
    // .pipe(gulp.dest(sourceAsDestination));
});

/**
 * Minify CSS
 * Minimize all non-compressed css
 */
const cssSrc = getApps('css/!(*.min).css');
cssSrc.push('static/css/style.css');
cssSrc.push('core/adminlte/static/plugins/sweetalert/1.1.3/sweetalert.min.css');
// cssSrc.push('core/adminlte/static/plugins/bootstrap/css/bootstrap.min.css');
// cssSrc.push('core/adminlte/static/plugins/jquery-chosen/chosen.min.css'); // lead problem
// cssSrc.push('core/adminlte/static/adminlte/css/font-awesome.min.css'); // lead problem
// cssSrc.push('core/adminlte/static/adminlte/css/AdminLTE.min.css');
cssSrc.push('core/adminlte/static/adminlte/css/skins/skin-blue.min.css');
gulp.task('styles:css', () => {
  gulp.src(cssSrc)
    .pipe(cleanCSS())
    .pipe(concat('bundle.css'))
    .pipe(gulp.dest(BUILD_DEST_PATH))
    // .pipe(rename({ suffix: '.min' }))
    // .pipe(gulp.dest(sourceAsDestination))
});


/**
 * Bundle task: Compile styles
 */
gulp.task('styles', ['styles:css']);
gulp.task('scripts', ['scripts:apps', 'scripts:core']);

/**
 * Bundle task: Build everything which need to be processed
 */
gulp.task('build', ['scripts', 'styles']);

/**
 * Bundle task: Auto compile styles and styles
 */
gulp.task('watch', ['scripts', 'styles'], () => {
  gulp.watch(scriptsSrc, ['scripts']);
  gulp.watch(cssSrc, ['styles:css']);
});

/**
 * Bundle task: Default
 */
gulp.task('default', ['watch']);



/**
  |--------------------------------------------------------------------------
  | Functions
  |--------------------------------------------------------------------------
  */

function registerApp(dir, options) {
  // Construct an object which contained the app properties
  const app = Object.assign({
    dir: dir,
  }, options);
  // Store in the _apps private variable
  _apps.push(app);
}

function getApps(globs) {
  // Function to convert multi-dimension array into single dimension
  const flattenArray = nestedArray => [].concat.apply([], nestedArray);
  // Function to get the full path
  const getPath = (app, glob) => path.join('.', app.dir, 'static','js', '**', glob);

  let sources;
  sources = _apps.map(app => {
    const paths = [];
    const excludes = app.excludes || [];

    // Add the full glob path
    paths.push(getPath(app, globs));

    // Add the exclude paths
    if (excludes.length) {
      paths.push('!' + getPath(app, '*(' + excludes.join('|') + ')/**/' + globs));
    }

    return paths;
  });

  sources = flattenArray(sources);
  return sources;
}

function sourceAsDestination(file) {
  return file.base;
}
