var fs = require('fs');
var yaml = require('js-yaml');
var gulp = require('gulp');
var browserSync = require('browser-sync').create('My Server');

var jekyll_config = yaml.safeLoad(fs.readFileSync('../../_config.yml', 'utf8'));

gulp.task('default', function () {
  browserSync.init({
    proxy: 'http://localhost' + ((':' + jekyll_config.port) || '')
  });

  var bs = require('browser-sync').get('My Server');
  bs.watch(jekyll_config.destination + '/**/*.html').on('change', bs.reload);
});
