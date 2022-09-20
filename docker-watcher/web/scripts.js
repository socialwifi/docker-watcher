$( document ).ready(function() {
});


function addLogWidget(container) {
  if (!document.getElementById(container.id)) {
    var template = $('#widgets .log-box');
    var workspace = $('.logs');
    var copy = template.clone();
    copy.attr('id', container.id);
    copy.attr('data-container-name', container.name);

    var label = copy.find('.log-label span');
    label.text(container.name);

    var close = copy.find('.log-label button');
    close.click(function () {
      copy.remove();
    });
    workspace.append(copy);

    appendLog(container.name, {'text': 'Hello There!', 'debug': 'Start log'});
    if (typeof eel !== 'undefined') {
      eel.start_log_stream(container.name);
    }
  }
}

function buildMicroservicesMenu(microservices_list) {
  var workspace = $('.navbar .container-menu .menu-elements');

  microservices_list.forEach(function (microservice) {
    if (!document.getElementById(microservice.label) && microservice.containers.length > 0) {
      var template = $('#widgets .navbar-collapse');
      var copy = template.clone();
      var link = copy.find('.nav-link');

      link.text(microservice.label);
      link.attr('id', microservice.label);

      var dropDownContainer = copy.find('.dropdown-menu');
      dropDownContainer.text('');
      var dropTemplate = $('<li><a class="dropdown-item" href="#"></a></li>');
      microservice.containers.forEach(function (container) {
        var drop = dropTemplate.clone();
        drop.data('container-id', container.id);

        var link = drop.find('a');
        link.text(container.name);
        link.click(function () {
          addLogWidget(container);
        });

        dropDownContainer.append(drop);
      });

      workspace.append(copy);
    }
  });
}

function appendLog(containerName, log) {
  var logsWidget = $('div[data-container-name="' + containerName + '"]');
  var logsContainter = logsWidget.find('.log');
  var template = $('<p><b></b> <span></span></p>');
  template.find('b').text(log.text);
  if (log.debug && log.debug !== '{}') {
    template.find('span').text(log.debug);
  }
  logsContainter.append(template);
  logsContainter.scrollTop(logsContainter[0].scrollHeight);
}

if (typeof eel !== 'undefined') {
  eel.expose(push_microservices);
  eel.expose(push_container_log);
}

function push_microservices(microservices_list) {
  buildMicroservicesMenu(microservices_list);
}
function push_container_log(container_name, log) {
  appendLog(container_name, log);
}
