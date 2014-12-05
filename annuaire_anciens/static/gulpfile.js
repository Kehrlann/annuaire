//---------------------
//
// ONG TABLET - gulpfile.js
//
// Author : dgarnier@timsoft.com
//			pompé sur johann@timsoft.com
//----------------------


// include gulp
var gulp            = require('gulp'),
    plumber         = require('gulp-plumber'),
    rename          = require('gulp-rename'),
	browserify		= require('gulp-browserify'),
    del             = require('del');
	
	// Gulp plumber error handler
var onError = function(err)
{
    console.log("::::::::: Error");
    console.log(err);
//    console.log(event);
//    var msg = [
//            'Line: ' + event.error.line,
//            'Reason: ' + event.error.reason
//    ];
//
//    notify.onError(msg.join('\n'));
};

var jsAppSrc = ['./app/*.js', './app/*.jsx', './app/**/*.js', './app/**/*.jsx'];

gulp.task(  'clean',    [],
            function(cb)
            {
                return del(['./js/app-bundle.js'], cb);
            }
);

gulp.task(  'script',   ['clean'],
            function(){
                return gulp.src('./app/Router.js')
                    .pipe(plumber({errorHandler: onError}))
                    .pipe(browserify({transform: ['reactify'], debug: true}))
                    .pipe(rename('app-bundle.js'))
                    .pipe(gulp.dest('./js/'));

            }
);



gulp.task('default', ['script'], function(){

    gulp.watch(jsAppSrc, ['script']);
});