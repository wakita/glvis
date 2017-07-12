/ start this task with "gulp watch" command

var gulp = require('gulp')
var exec = require('gulp-exec')
var bs = require('browser-sync').create('My Server')

bs.init({
 server: { baseDir: "./", index: 't3d.html' }
});

var bs = require('browser-sync').get('My Server');

bs.watch('./**/*.html').on('change', bs.reload);

gulp.task('watch-symdoc', function () {
 gulp.watch('./**/*.py', [])
 .on('change', function (ev) {
   gulp.src(ev.path).pipe(exec('./x ' + ev.path));
 });
});

gulp.task('default', ['watch-symdoc']);
