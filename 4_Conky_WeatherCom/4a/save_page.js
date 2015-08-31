var system = require('system');
var page = require('webpage').create();

page.open(system.args[1], function()
{
    page.evaluate(function(eventFire_fn) {
    eventFire_fn(document.getElementById('fahrButton'), 'click');
}, eventFire);
    console.log(page.content);
    phantom.exit();
});

function eventFire(el, etype){
  if (el.fireEvent) {
    el.fireEvent('on' + etype);
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}
