(function(){
  try {
    var s = document.createElement('script');
    s.src = '/__livereload.js';
    s.async = true;
    s.onerror = function() { /* dev server not present; ignore */ };
    document.head.appendChild(s);
  } catch(e) { /* ignore */ }
})();

