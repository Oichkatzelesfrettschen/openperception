(function(){
  function setVariant(v){
    if(!v) return;
    document.documentElement.setAttribute('data-cvd', v);
    var sel = document.getElementById('variant');
    if(sel){ sel.value = v; }
  }
  function setSimulatorMode(m){
    if(!m) return;
    var sel = document.getElementById('mode');
    if(sel){ sel.value = m; sel.dispatchEvent(new Event('change')); }
  }
  var p = new URLSearchParams(location.search);
  setVariant(p.get('variant'));
  setSimulatorMode(p.get('simulate'));
})();

