const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');

/*
 * Since this is mostly a back-end app, all that's needed from gulp is to
 * run preprocessors.
 */
gulp.task('default', [
  'styles'
], function defaultTask() {
    gulp.watch('static/sass/**/*.scss', ['styles']);
});

gulp.task('styles', function stylesTask() {
  gulp.src('static/sass/main.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(autoprefixer({
        browsers: ['last 2 versions']
      }))
      .pipe(gulp.dest('static/css'))
});
